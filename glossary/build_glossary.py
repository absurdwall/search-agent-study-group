#!/usr/bin/env python3
"""Validate Markdown glossary sources and deterministically build terms.json."""
import argparse,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SECTIONS=['Simple definition','Working definition','Why it matters','Example','Common confusion','Study-group notes']
def build():
 terms=[]
 for path in sorted((ROOT/'terms').glob('*.md')):
  _,meta,body=path.read_text().split('---',2)
  t={}
  for m in re.finditer(r'^([a-z_]+):\s*(.*?)(?=\n[a-z_]+:|\Z)',meta,re.M|re.S):
   key,value=m.groups();value=value.strip();t[key]=json.loads(value) if value.startswith(('[','{')) else value
  pieces=re.split(r'^## (.+)\n',body,flags=re.M)
  t['sections']={pieces[i]:pieces[i+1].strip() for i in range(1,len(pieces),2)}
  assert set(t['sections'])==set(SECTIONS),path
  assert all(t['sections'][s] for s in SECTIONS[:-1]),path
  assert len(t['sections']['Simple definition'])<=180,path
  assert t['status'] in ['published','deprecated','draft','needs-review'],path
  assert t['id']==path.stem,path
  assert t['sources'] and all(s['title'] and s['note'] and s['url'].startswith('https://') for s in t['sources']),path
  terms.append(t)
 ids={t['id'] for t in terms};assert len(ids)==len(terms)
 for t in terms:
  assert all(r['target'] in ids for r in t['relations']),t['id']
 return json.dumps({'schema_version':1,'generated_from':'glossary/terms/*.md','terms':terms},ensure_ascii=False,indent=2)+'\n'
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args();output=build();target=ROOT/'terms.json'
 if args.check: assert target.read_text()==output,'terms.json is stale'
 else:target.write_text(output)
 print('Glossary sources and generated index validated.')
