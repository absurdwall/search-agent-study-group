"""POSIX scoped file operations. Hook policy is not required for enforcement."""
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
from datetime import datetime, timezone


class Refusal(ValueError):
    pass


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(path, value):
    temp = path.with_suffix('.new')
    with temp.open('w') as stream:
        json.dump(value, stream, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)


class Store:
    def __init__(self, config):
        self.config = json.loads(Path(config).read_text())
        raw = Path(self.config['workspace'])
        if raw.is_symlink():
            raise Refusal('Workspace root must not be a symlink.')
        self.root = raw.resolve(strict=True)
        self.state = Path(self.config['state']).resolve(strict=True)
        if self.state == self.root or self.state.is_relative_to(self.root):
            raise Refusal('State and backups must be outside the working data.')
        self.categories = self.config.get('categories', ['Notes', 'Reports', 'Images', 'Review'])
        if not self.categories or any(not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]{0,40}', x) for x in self.categories):
            raise Refusal('Invalid category names.')

    @contextlib.contextmanager
    def locked(self):
        with (self.state/'lock').open('a') as stream:
            fcntl.flock(stream, fcntl.LOCK_EX)
            yield

    def log(self, file, **record):
        with (self.state/file).open('a') as stream:
            stream.write(json.dumps({'at': datetime.now(timezone.utc).isoformat(), **record})+'\n')
            stream.flush()
            os.fsync(stream.fileno())

    def parts(self, path):
        if not isinstance(path, str) or not path or '\\' in path or '\x00' in path:
            raise Refusal('Use POSIX workspace-relative file paths.')
        parts = path.split('/')
        if path.startswith('/') or any(p in ('', '.', '..') for p in parts):
            raise Refusal('Absolute paths and dot components are outside the authorized workspace.')
        return parts

    @contextlib.contextmanager
    def parent(self, path):
        parts = self.parts(path)
        fd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            for part in parts[:-1]:
                nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                os.close(fd)
                fd = nxt
            yield fd, parts[-1]
        finally:
            os.close(fd)

    def read(self, path):
        with self.parent(path) as (parent, name):
            fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
            try:
                info = os.fstat(fd)
                if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                    raise Refusal('Only regular files with one link are supported.')
                if info.st_size > 10*1024*1024:
                    raise Refusal('File exceeds the 10 MiB operation limit; leave it for review.')
                with os.fdopen(os.dup(fd), 'rb') as stream:
                    data = stream.read(10*1024*1024+1)
                if len(data) > 10*1024*1024:
                    raise Refusal('File grew beyond the operation limit.')
                return data, info
            finally:
                os.close(fd)

    def check(self, source, destination, expected_sha256):
        sp, dp = self.parts(source), self.parts(destination)
        if len(sp) < 2 or sp[0] != 'Inbox':
            raise Refusal('Source must be a regular file under Inbox.')
        if len(dp) != 3 or dp[0] != 'Organized' or dp[1] not in self.categories:
            raise Refusal('Destination must be Organized/<configured category>/<filename>.')
        data, info = self.read(source)
        if sha(data) != expected_sha256:
            raise Refusal('Source contents changed since inspection. Inspect again before replanning.')
        with self.parent(destination) as (fd, name):
            try:
                os.stat(name, dir_fd=fd, follow_symlinks=False)
            except FileNotFoundError:
                return data, info
        raise Refusal(f'Destination {destination} already exists. Preserve both files; inspect again and choose a new name.')

    def inspect(self):
        files = []
        for base in ['Inbox', 'Organized']:
            if (self.root/base).is_symlink():
                files.append({'path':base, 'unsupported':'symlink root'})
                continue
            # Never recurse through symlinks. Each read reopens components with O_NOFOLLOW.
            for path, dirs, names in os.walk(self.root/base, followlinks=False):
                for name in dirs[:]:
                    p = Path(path)/name
                    if p.is_symlink():
                        dirs.remove(name)
                        files.append({'path':str(p.relative_to(self.root)), 'unsupported':'symlink directory'})
                for name in sorted(names):
                    rel = str((Path(path)/name).relative_to(self.root))
                    try:
                        data, _ = self.read(rel)
                        try:
                            preview = data.decode('utf-8')[:12000]
                            if '\x00' in preview:
                                raise UnicodeError()
                        except UnicodeError:
                            preview = '[binary data; classify cautiously or use Review]'
                        files.append({'path':rel, 'sha256':sha(data), 'bytes':len(data), 'preview':preview, 'truncated':len(data)>12000})
                    except (OSError, Refusal) as error:
                        files.append({'path':rel, 'unsupported':str(error)})
        return {'workspace':str(self.root), 'categories':self.categories, 'files':files}

    def record_path(self, operation_id):
        if not isinstance(operation_id, str) or not re.fullmatch(r'[a-zA-Z0-9_-]{1,64}', operation_id):
            raise Refusal('Invalid operation ID.')
        return self.state/'operations'/f'{operation_id}.json'

    def move(self, operation_id, source, destination, expected_sha256, _interrupt=False):
        args = {'source':source, 'destination':destination, 'expected_sha256':expected_sha256}
        record_path = self.record_path(operation_id)
        with self.locked():
            if record_path.exists():
                record = json.loads(record_path.read_text())
                if record['arguments'] != args:
                    raise Refusal('Operation ID already belongs to different arguments.')
                if record['status'] == 'completed':
                    return {'status':'completed', 'operation_id':operation_id, 'idempotent':True, **args}
                raise Refusal('Operation is pending. Use recover_move with this exact operation ID.')
            data, info = self.check(**args)
            backup = self.state/'backups'/f'{operation_id}.bin'
            with backup.open('xb') as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            record = {'operation_id':operation_id, 'arguments':args, 'status':'intent', 'source_identity':[info.st_dev, info.st_ino]}
            save(record_path, record)
            # Same-filesystem exclusive creation; an intervening collision cannot replace a file.
            with self.parent(source) as (sfd, sname), self.parent(destination) as (dfd, dname):
                current = os.stat(sname, dir_fd=sfd, follow_symlinks=False)
                if [current.st_dev, current.st_ino] != record['source_identity']:
                    raise Refusal('Source identity changed; preserve both paths for review.')
                os.link(sname, dname, src_dir_fd=sfd, dst_dir_fd=dfd, follow_symlinks=False)
                linked = os.stat(dname, dir_fd=dfd, follow_symlinks=False)
                if [linked.st_dev, linked.st_ino] != record['source_identity']:
                    raise Refusal('Source raced during linking; preserve both paths for review.')
                if _interrupt:
                    raise InterruptedError('Injected test interruption after exclusive link.')
                # Validate current bytes using the open destination before removing source.
                fd = os.open(dname, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dfd)
                with os.fdopen(fd, 'rb') as stream:
                    if sha(stream.read()) != expected_sha256:
                        raise Refusal('Contents changed during move; preserve both paths for review.')
                if os.stat(sname, dir_fd=sfd, follow_symlinks=False).st_ino != info.st_ino:
                    raise Refusal('Source identity changed before completion.')
                os.unlink(sname, dir_fd=sfd)
            record['status'] = 'completed'
            save(record_path, record)
            self.log('operations.jsonl', **record)
            return {'status':'completed', 'operation_id':operation_id, **args}

    def recover(self, operation_id):
        path = self.record_path(operation_id)
        with self.locked():
            record = json.loads(path.read_text())
            args = record['arguments']
            if record['status'] == 'completed':
                return {'status':'completed', 'operation_id':operation_id, 'idempotent':True}
            with self.parent(args['source']) as (sfd, sname), self.parent(args['destination']) as (dfd, dname):
                dest = os.stat(dname, dir_fd=dfd, follow_symlinks=False)
                if not stat.S_ISREG(dest.st_mode) or [dest.st_dev, dest.st_ino] != record['source_identity']:
                    raise Refusal('Pending destination identity differs; manual review required.')
                fd = os.open(dname, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dfd)
                with os.fdopen(fd, 'rb') as stream:
                    if sha(stream.read()) != args['expected_sha256']:
                        raise Refusal('Pending destination bytes changed; backup retained for manual review.')
                try:
                    src = os.stat(sname, dir_fd=sfd, follow_symlinks=False)
                except FileNotFoundError:
                    src = None
                if src:
                    if [src.st_dev, src.st_ino] != record['source_identity']:
                        raise Refusal('Pending source identity differs; manual review required.')
                    os.unlink(sname, dir_fd=sfd)
            record['status'] = 'completed'
            record['recovered'] = True
            save(path, record)
            self.log('operations.jsonl', **record)
            return {'status':'completed', 'operation_id':operation_id, 'recovered':True, **args}
