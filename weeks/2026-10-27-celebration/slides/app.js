(() => {
  const slides = [...document.querySelectorAll('.slide')];
  const dotsEl = document.getElementById('dots');
  const counter = document.getElementById('counter');
  const bar = document.getElementById('bar');
  const overview = document.getElementById('overview');
  const grid = document.getElementById('overview-grid');
  let cur = 0;

  slides.forEach((s, i) => {
    const d = document.createElement('button');
    d.className = 'dot';
    d.setAttribute('aria-label', `Go to slide ${i + 1}: ${s.dataset.title}`);
    d.addEventListener('click', () => go(i));
    dotsEl.appendChild(d);

    const c = document.createElement('button');
    c.className = 'ov-card';
    c.innerHTML = `<small>${String(i + 1).padStart(2, '0')}</small><strong>${s.dataset.title}</strong>`;
    c.addEventListener('click', () => { toggleOverview(false); go(i); });
    grid.appendChild(c);
  });

  const dots = [...dotsEl.children];
  const cards = [...grid.children];

  function countUp(slide) {
    slide.querySelectorAll('[data-count]').forEach(el => {
      const target = +el.dataset.count;
      if (!target) return;
      const dec = (el.dataset.count.split('.')[1] || '').length;
      const t0 = performance.now(), dur = 900;
      const tick = now => {
        const p = Math.min((now - t0) / dur, 1);
        el.textContent = (target * (1 - Math.pow(1 - p, 3))).toFixed(dec);
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
  }

  function confetti(slide) {
    const box = slide.querySelector('.confetti');
    if (!box || box.childElementCount) return;
    const colors = ['#eda91b', '#078c8f', '#df7427', '#07394a'];
    for (let i = 0; i < 40; i++) {
      const p = document.createElement('i');
      p.style.left = Math.random() * 100 + '%';
      p.style.background = colors[i % colors.length];
      p.style.animationDuration = 4 + Math.random() * 5 + 's';
      p.style.animationDelay = -Math.random() * 6 + 's';
      box.appendChild(p);
    }
  }

  function go(i, push = true) {
    cur = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach((s, k) => {
      s.classList.toggle('active', k === cur);
      s.setAttribute('aria-hidden', k === cur ? 'false' : 'true');
    });
    dots.forEach((d, k) => d.classList.toggle('active', k === cur));
    cards.forEach((c, k) => c.classList.toggle('active', k === cur));
    counter.textContent = `${cur + 1} / ${slides.length}`;
    bar.style.width = ((cur + 1) / slides.length * 100) + '%';
    if (push) history.replaceState(null, '', '#s' + (cur + 1));
    countUp(slides[cur]);
    confetti(slides[cur]);
  }

  const next = () => go(cur + 1);
  const prev = () => go(cur - 1);
  function toggleOverview(force) {
    overview.hidden = force === undefined ? !overview.hidden : !force;
  }
  function toggleFull() {
    if (document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen?.();
  }

  document.getElementById('next').addEventListener('click', next);
  document.getElementById('prev').addEventListener('click', prev);
  document.getElementById('btn-overview').addEventListener('click', () => toggleOverview());
  document.getElementById('btn-full').addEventListener('click', toggleFull);
  document.querySelectorAll('[data-next]').forEach(b => b.addEventListener('click', next));
  document.querySelectorAll('[data-first]').forEach(b => b.addEventListener('click', () => go(0)));

  document.addEventListener('keydown', e => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    if (document.body.classList.contains('g-open')) return;
    if (e.target.closest && e.target.closest('input, textarea, select, [contenteditable]')) return;
    switch (e.key) {
      case 'ArrowRight': case 'PageDown': case ' ': case 'Enter':
        if (e.target.closest && e.target.closest('button, a, summary') && (e.key === 'Enter' || e.key === ' ')) return;
        e.preventDefault(); next(); break;
      case 'ArrowLeft': case 'PageUp': e.preventDefault(); prev(); break;
      case 'Home': go(0); break;
      case 'End': go(slides.length - 1); break;
      case 'o': case 'O': toggleOverview(); break;
      case 'f': case 'F': toggleFull(); break;
      case 'Escape': toggleOverview(false); break;
    }
  });

  let x0 = null;
  document.addEventListener('touchstart', e => { x0 = e.target.closest('[data-noswipe], .g-modal') ? null : e.touches[0].clientX; }, { passive: true });
  document.addEventListener('touchend', e => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 60) dx < 0 ? next() : prev();
    x0 = null;
  });

  window.addEventListener('hashchange', () => {
    const n = parseInt(location.hash.replace('#s', ''), 10);
    if (n) go(n - 1, false);
  });

  const track = document.querySelector('.marquee-track');
  if (track) track.innerHTML += track.innerHTML;

  document.querySelectorAll('.tilt').forEach(el => {
    el.addEventListener('mousemove', e => {
      const r = el.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      el.style.transform = `perspective(900px) rotateY(${x * 8}deg) rotateX(${-y * 8}deg) translateY(-3px)`;
    });
    el.addEventListener('mouseleave', () => { el.style.transform = ''; });
  });

  const start = parseInt(location.hash.replace('#s', ''), 10);
  go(start ? start - 1 : 0, false);
})();
