(() => {
  const G = window.GLOSSARY;
  const slide = document.querySelector('.gloss-slide');
  if (!G || !slide) return;

  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const byId = new Map(G.terms.map(t => [t.id, t]));
  const catById = new Map(G.cats.map(c => [c.id, c]));
  const wall = document.getElementById('g-wall');
  const chipsEl = document.getElementById('g-chips');
  const input = document.getElementById('g-q');
  const countEl = document.getElementById('g-count');
  const emptyEl = document.getElementById('g-empty');
  const modal = document.getElementById('g-modal');
  const card = modal.querySelector('.g-card');
  const state = { cat: 'all', q: '', view: 'stars' };
  const views = {};
  const tiles = new Map();
  let current = null;
  let opener = null;

  const el = (tag, cls, text) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined) n.textContent = text;
    return n;
  };
  const svg = (tag, attrs = {}) => {
    const n = document.createElementNS('http://www.w3.org/2000/svg', tag);
    for (const k in attrs) n.setAttribute(k, attrs[k]);
    return n;
  };
  const pad = n => String(n).padStart(2, '0');
  const clip = (s, n) => (s.length > n ? s.slice(0, n - 1).trimEnd() + '…' : s);
  const tint = cat => ({ '--c': cat.c, '--ct': cat.ct });
  const setVars = (node, cat) => { const v = tint(cat); for (const k in v) node.style.setProperty(k, v[k]); };

  // ---------- adjacency (outbound first, then inbound)
  const out = new Map(), inn = new Map();
  G.terms.forEach(t => { out.set(t.id, []); inn.set(t.id, []); });
  G.terms.forEach(t => t.rel.forEach(([to, type]) => {
    out.get(t.id).push([to, type]);
    inn.get(to).push([t.id, type]);
  }));
  const neighbours = id => {
    const seen = new Set(), list = [];
    [...out.get(id), ...inn.get(id)].forEach(([n, type]) => {
      if (!seen.has(n) && n !== id) { seen.add(n); list.push([n, type]); }
    });
    return list;
  };

  G.terms.forEach(t => {
    t._h = [t.term, t.id, t.aliases.join(' '), t.simple, t.weeks.map(w => 'week ' + w + ' wk' + w).join(' ')]
      .join(' ').toLowerCase();
  });

  // ---------- chips
  const chipAll = (() => {
    const b = el('button', 'g-chip on');
    b.type = 'button';
    b.dataset.cat = 'all';
    b.append(el('i'), document.createTextNode('All '), el('b', '', String(G.terms.length)));
    b.querySelector('i').style.background = 'var(--ink)';
    return b;
  })();
  chipsEl.appendChild(chipAll);
  G.cats.forEach(c => {
    const b = el('button', 'g-chip');
    b.type = 'button';
    b.dataset.cat = c.id;
    const dot = el('i');
    dot.style.background = c.c;
    b.append(dot, document.createTextNode(c.name + ' '), el('b', '', String(c.count)));
    chipsEl.appendChild(b);
  });
  chipsEl.addEventListener('click', e => {
    const b = e.target.closest('.g-chip');
    if (!b) return;
    state.cat = state.cat === b.dataset.cat && b.dataset.cat !== 'all' ? 'all' : b.dataset.cat;
    apply();
  });

  // ---------- wall
  G.terms.forEach((t, i) => {
    const cat = catById.get(t.cat);
    const b = el('button', 'tile');
    b.type = 'button';
    b.dataset.id = t.id;
    b.style.setProperty('--i', i);
    setVars(b, cat);
    b.setAttribute('aria-label', `${t.term}, ${cat.name}`);
    b.append(el('span', 't-n', pad(t.n)), el('span', 't-sym', t.sym), el('span', 't-name', t.term.replace(/\s*\(.*?\)/, '')));
    wall.appendChild(b);
    tiles.set(t.id, b);
  });

  function matches(t) {
    if (state.cat !== 'all' && t.cat !== state.cat) return false;
    if (!state.q) return true;
    return state.q.split(/\s+/).every(tok => t._h.includes(tok));
  }
  const visibleIds = () => G.terms.filter(matches).map(t => t.id);

  function apply() {
    let n = 0;
    G.terms.forEach(t => {
      const ok = matches(t);
      const tile = tiles.get(t.id);
      tile.classList.toggle('dim', !ok);
      tile.classList.toggle('hit', ok && !!state.q);
      tile.tabIndex = ok ? 0 : -1;
      if (ok) n++;
    });
    [...chipsEl.children].forEach(c => c.classList.toggle('on', c.dataset.cat === state.cat));
    countEl.textContent = n === G.terms.length ? `${n} terms` : `${n} of ${G.terms.length} terms`;
    emptyEl.hidden = n > 0;
    const set = new Set(G.terms.filter(matches).map(t => t.id));
    Object.values(views).forEach(v => v.built && v.update(set));
  }
  input.addEventListener('input', () => { state.q = input.value.trim().toLowerCase(); apply(); });
  input.addEventListener('keydown', e => {
    if (e.key === 'Escape') { input.value = ''; state.q = ''; apply(); input.blur(); e.stopPropagation(); }
  });
  document.getElementById('g-clear').addEventListener('click', () => {
    input.value = ''; state.q = ''; state.cat = 'all'; apply();
  });
  apply();

  // ---------- hover effects
  const tip = el('div', 'g-tip');
  tip.setAttribute('role', 'tooltip');
  tip.hidden = true;
  document.body.appendChild(tip);

  function showTip(tile) {
    if (modal.hidden === false) return;
    const t = byId.get(tile.dataset.id), cat = catById.get(t.cat);
    tip.replaceChildren();
    const h = el('strong', '', t.term);
    const c = el('em', '', cat.name);
    c.style.color = cat.ct;
    tip.append(c, h, el('span', '', clip(t.simple, 150)));
    tip.hidden = false;
    const r = tile.getBoundingClientRect();
    const tw = tip.offsetWidth, th = tip.offsetHeight;
    let x = Math.min(Math.max(8, r.left + r.width / 2 - tw / 2), window.innerWidth - tw - 8);
    let y = r.top - th - 12;
    if (y < 70) y = r.bottom + 12;
    tip.style.left = x + 'px';
    tip.style.top = y + 'px';
  }
  const hideTip = () => { tip.hidden = true; };

  wall.addEventListener('pointermove', e => {
    const t = e.target.closest('.tile');
    if (!t) return;
    const r = t.getBoundingClientRect();
    t.style.setProperty('--mx', (e.clientX - r.left) + 'px');
    t.style.setProperty('--my', (e.clientY - r.top) + 'px');
  });
  wall.addEventListener('pointerover', e => {
    const t = e.target.closest('.tile');
    if (t && e.pointerType === 'mouse' && !t.classList.contains('dim')) showTip(t);
  });
  wall.addEventListener('pointerout', e => { if (e.target.closest('.tile')) hideTip(); });
  wall.addEventListener('focusin', e => { const t = e.target.closest('.tile'); if (t) showTip(t); });
  wall.addEventListener('focusout', hideTip);

  // idle glint
  if (!reduce) {
    setInterval(() => {
      if (!slide.classList.contains('active') || !modal.hidden || state.view !== 'table') return;
      const live = [...tiles.values()].filter(t => !t.classList.contains('dim'));
      if (!live.length) return;
      const t = live[Math.floor(Math.random() * live.length)];
      t.classList.add('glint');
      setTimeout(() => t.classList.remove('glint'), 800);
    }, 900);
  }

  // ---------- views: Stars, Table
  const SW = 1200, SH = 470;
  const rng = seed => () => {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  const degOf = new Map(G.terms.map(t => [t.id, neighbours(t.id).length]));
  const edges = [];
  {
    const seenE = new Set();
    G.terms.forEach(t => out.get(t.id).forEach(([to]) => {
      const k = [t.id, to].sort().join('|');
      if (!seenE.has(k)) { seenE.add(k); edges.push([t.id, to]); }
    }));
  }
  const centers = {};
  G.cats.forEach((c, i) => {
    const a = -Math.PI / 2 + (i * 2 * Math.PI) / G.cats.length;
    centers[c.id] = [SW / 2 + Math.cos(a) * SW * 0.36, SH / 2 + Math.sin(a) * SH * 0.32];
  });
  const shortName = t => t.term.replace(/\s*\(.*?\)/, '');
  const currentSet = () => new Set(G.terms.filter(matches).map(t => t.id));
  const pickRandom = () => { const v = visibleIds(); return v.length ? v[Math.floor(Math.random() * v.length)] : null; };

  views.table = { el: wall, built: true, update() {} };

  // ===== Stars (constellation) =====
  const STAR = { foundations: '#3fd0d4', 'agent-systems': '#ff9a4d', 'frameworks-and-protocols': '#6fb0ff',
    'control-and-quality': '#c791e8', 'lab-tools': '#86d982', codex: '#ffd15c', beyond: '#e6f3f7' };

  let simIx = null;
  function stepSim(P, a, pinned) {
    if (!simIx) simIx = new Map(P.map((p, i) => [p.id, i]));
    for (let i = 0; i < P.length; i++) {
      for (let j = i + 1; j < P.length; j++) {
        const dx = P[j].x - P[i].x, dy = P[j].y - P[i].y;
        const d2 = dx * dx + dy * dy + 0.5, d = Math.sqrt(d2);
        const f = (7000 / d2) * a;
        const fx = (dx / d) * f, fy = (dy / d) * f;
        P[i].vx -= fx; P[i].vy -= fy; P[j].vx += fx; P[j].vy += fy;
      }
    }
    edges.forEach(([a1, b1]) => {
      const p = P[simIx.get(a1)], q = P[simIx.get(b1)];
      const dx = q.x - p.x, dy = q.y - p.y, d = Math.sqrt(dx * dx + dy * dy) + 0.01;
      const f = (d - 80) * 0.012;
      p.vx += (dx / d) * f; p.vy += (dy / d) * f; q.vx -= (dx / d) * f; q.vy -= (dy / d) * f;
    });
    P.forEach(p => {
      if (p === pinned || p.fixed) { p.vx = p.vy = 0; return; }
      const c = centers[p.cat];
      p.vx += (c[0] - p.x) * 0.01; p.vy += (c[1] - p.y) * 0.01;
      p.vx *= 0.82; p.vy *= 0.82;
      p.x = Math.min(SW - 46, Math.max(46, p.x + p.vx));
      p.y = Math.min(SH - 34, Math.max(30, p.y + p.vy));
    });
  }

  function layoutStars() {
    const rand = rng(11);
    const P = G.terms.map(t => {
      const c = centers[t.cat];
      return { id: t.id, cat: t.cat, x: c[0] + (rand() - .5) * 140, y: c[1] + (rand() - .5) * 100, vx: 0, vy: 0,
        r: 5 + Math.min(degOf.get(t.id), 10) * 0.9 };
    });
    const N = 420;
    for (let it = 0; it < N; it++) stepSim(P, 1 - it / N);
    const xs = P.map(p => p.x), ys = P.map(p => p.y);
    const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
    P.forEach(p => {
      p.x = 70 + (p.x - x0) / (x1 - x0 || 1) * (SW - 140);
      p.y = 45 + (p.y - y0) / (y1 - y0 || 1) * (SH - 100);
    });
    return P;
  }

  views.stars = (() => {
    const el = document.getElementById('g-stars');
    let suppressClick = false;
    const hideTipSafe = () => { try { hideTip(); } catch (_) {} };
    let root, nodes = new Map(), edgeEls = [], P = [], pos = new Map(), drag = null, raf = 0, alpha = 0;
    const clearHl = () => {
      root.classList.remove('lit');
      root.querySelectorAll('.on, .nb').forEach(n => n.classList.remove('on', 'nb'));
    };
    const hl = id => {
      clearHl();
      root.classList.add('lit');
      nodes.get(id).classList.add('on');
      neighbours(id).forEach(([n]) => nodes.get(n)?.classList.add('nb'));
      edgeEls.forEach(e => { if (e.dataset.a === id || e.dataset.b === id) e.classList.add('on'); });
    };
    return {
      el, built: false,
      build() {
        P = layoutStars();
        root = svg('svg', { viewBox: `0 0 ${SW} ${SH}`, preserveAspectRatio: 'xMidYMid meet', role: 'group', 'aria-label': 'Constellation of glossary terms' });
        const defs = svg('defs');
        G.cats.forEach(c => {
          const g = svg('radialGradient', { id: 'halo-' + c.id });
          g.append(svg('stop', { offset: '0%', 'stop-color': STAR[c.id], 'stop-opacity': '.75' }),
                   svg('stop', { offset: '100%', 'stop-color': STAR[c.id], 'stop-opacity': '0' }));
          defs.append(g);
        });
        root.append(defs);
        const bg = svg('g', { class: 'bgstars' });
        const rand = rng(3);
        for (let i = 0; i < 90; i++) {
          const s = svg('circle', { cx: rand() * SW, cy: rand() * SH, r: (0.5 + rand() * 1.1).toFixed(2), class: 'tw' });
          s.style.animationDelay = (-rand() * 4).toFixed(2) + 's';
          s.style.animationDuration = (2.4 + rand() * 3).toFixed(2) + 's';
          bg.append(s);
        }
        root.append(bg);
        const shoot = svg('line', { x1: 90, y1: 40, x2: 150, y2: 66, class: 'shoot' });
        root.append(shoot);
        pos = new Map(P.map(p => [p.id, p]));
        const eg = svg('g', { class: 'edges' });
        edges.forEach(([a, b]) => {
          const p = pos.get(a), q = pos.get(b);
          const ln = svg('line', { x1: p.x, y1: p.y, x2: q.x, y2: q.y, class: 'e' });
          ln.dataset.a = a; ln.dataset.b = b;
          eg.append(ln); edgeEls.push(ln);
        });
        root.append(eg);
        const ng = svg('g', { class: 'nodes' });
        const rand2 = rng(9);
        G.terms.forEach((t, i) => {
          const p = pos.get(t.id), col = STAR[t.cat];
          const g = svg('g', { class: 'n' + (degOf.get(t.id) >= 5 ? ' big' : ''), transform: `translate(${p.x.toFixed(1)} ${p.y.toFixed(1)})`, tabindex: '0', role: 'button', 'aria-label': `${t.term}, ${catById.get(t.cat).name}` });
          g.dataset.id = t.id;
          const dr = svg('g', { class: 'drift' });
          dr.style.setProperty('--i', i);
          dr.style.setProperty('--dx', ((rand2() - .5) * 9).toFixed(1) + 'px');
          dr.style.setProperty('--dy', ((rand2() - .5) * 9).toFixed(1) + 'px');
          dr.style.setProperty('--dur', (4 + rand2() * 4).toFixed(1) + 's');
          dr.style.setProperty('--del', (-rand2() * 6).toFixed(1) + 's');
          dr.append(svg('circle', { r: p.r * 3.4, fill: `url(#halo-${t.cat})`, class: 'halo' }),
                    svg('circle', { r: p.r, fill: col, class: 'core' }));
          const lab = svg('text', { y: p.r + 13, 'text-anchor': 'middle', class: 'lab' });
          lab.textContent = shortName(t);
          dr.append(lab);
          g.append(dr);
          ng.append(g);
          nodes.set(t.id, g);
        });
        root.append(ng);
        el.append(root);
        root.addEventListener('pointerover', e => { if (drag && drag.moved) return; const n = e.target.closest('.n'); if (n && !n.classList.contains('dim')) hl(n.dataset.id); });
        root.addEventListener('pointerout', e => { if (drag && drag.moved) return; if (e.target.closest('.n')) clearHl(); });
        root.addEventListener('focusin', e => { const n = e.target.closest('.n'); if (n) hl(n.dataset.id); });
        root.addEventListener('focusout', clearHl);
        root.addEventListener('click', e => { if (suppressClick) return; const n = e.target.closest('.n'); if (n && !n.classList.contains('dim')) open(n.dataset.id); });
        root.addEventListener('keydown', e => {
          const n = e.target.closest && e.target.closest('.n');
          if (n && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); e.stopPropagation(); open(n.dataset.id); }
        });
        const hint = document.createElement('p');
        hint.className = 's-hint';
        hint.textContent = 'drag a star · click to open · double-click empty space to reset';
        hint.setAttribute('aria-hidden', 'true');
        el.append(hint);
        const toSvg = e => {
          const m = root.getScreenCTM();
          return m ? new DOMPoint(e.clientX, e.clientY).matrixTransform(m.inverse()) : null;
        };
        const paint = () => {
          P.forEach(p => nodes.get(p.id).setAttribute('transform', `translate(${p.x.toFixed(1)} ${p.y.toFixed(1)})`));
          edgeEls.forEach(l => {
            const p = pos.get(l.dataset.a), q = pos.get(l.dataset.b);
            l.setAttribute('x1', p.x.toFixed(1)); l.setAttribute('y1', p.y.toFixed(1));
            l.setAttribute('x2', q.x.toFixed(1)); l.setAttribute('y2', q.y.toFixed(1));
          });
        };
        const tick = () => {
          raf = 0;
          stepSim(P, Math.max(alpha, 0.05), drag && drag.moved ? drag.p : null);
          paint();
          alpha *= 0.985;
          const live = P.some(p => Math.abs(p.vx) + Math.abs(p.vy) > 0.03);
          if (drag || (alpha > 0.02 && live)) raf = requestAnimationFrame(tick);
        };
        const kick = a => { alpha = Math.max(alpha, a); if (!raf) raf = requestAnimationFrame(tick); };
        root.addEventListener('pointerdown', e => {
          const n = e.target.closest('.n');
          if (!n || n.classList.contains('dim') || e.button > 0) return;
          drag = { p: pos.get(n.dataset.id), n, x0: e.clientX, y0: e.clientY, moved: false, id: e.pointerId };
        });
        root.addEventListener('mousedown', e => { if (e.target.closest('.n')) e.preventDefault(); });
        root.addEventListener('mousedown', e => { if (e.target.closest('.n')) e.preventDefault(); });
        root.addEventListener('pointermove', e => {
          if (!drag || e.pointerId !== drag.id) return;
          if (!drag.moved) {
            if (Math.hypot(e.clientX - drag.x0, e.clientY - drag.y0) < 5) return;
            drag.moved = true;
            drag.n.setPointerCapture(e.pointerId);
            root.classList.add('dragging');
            hl(drag.p.id);
            hideTipSafe();
          }
          const s = toSvg(e);
          if (!s) return;
          drag.p.x = Math.min(SW - 30, Math.max(30, s.x));
          drag.p.y = Math.min(SH - 24, Math.max(24, s.y));
          kick(0.35);
        });
        const endDrag = e => {
          if (!drag || (e.pointerId !== undefined && e.pointerId !== drag.id)) return;
          const was = drag.moved, p0 = drag.p;
          drag = null;
          root.classList.remove('dragging');
          if (was) {
            p0.fixed = true;
            suppressClick = true;
            setTimeout(() => { suppressClick = false; }, 0);
            clearHl();
            kick(0.15);
          }
        };
        root.addEventListener('pointerup', endDrag);
        root.addEventListener('pointercancel', endDrag);
        root.addEventListener('dblclick', e => {
          if (e.target.closest('.n')) return;
          P = layoutStars(); pos = new Map(P.map(p => [p.id, p])); paint();
        });
        this.built = true;
      },
      update(set) {
        nodes.forEach((n, id) => {
          const ok = set.has(id);
          n.classList.toggle('dim', !ok);
          n.classList.toggle('hit', ok && !!state.q);
          n.setAttribute('tabindex', ok ? '0' : '-1');
        });
        edgeEls.forEach(e => e.classList.toggle('dim', !(set.has(e.dataset.a) && set.has(e.dataset.b))));
      },
    };
  })();

  // ===== view switcher =====
  const switchEl = document.getElementById('g-switch');
  function setView(name) {
    if (!views[name]) return;
    state.view = name;
    Object.entries(views).forEach(([k, v]) => { v.el.hidden = k !== name; });
    const v = views[name];
    if (!v.built) { v.build(); v.update(currentSet()); }
    [...switchEl.children].forEach(b => {
      const on = b.dataset.view === name;
      b.classList.toggle('on', on);
      b.setAttribute('aria-selected', String(on));
    });
    slide.dataset.view = name;
  }
  switchEl.addEventListener('click', e => {
    const b = e.target.closest('button[data-view]');
    if (b) setView(b.dataset.view);
  });

  // ---------- entry overlay
  function section(title, text, cls) {
    if (!text) return null;
    const s = el('section', 'g-sec' + (cls ? ' ' + cls : ''));
    s.append(el('h4', '', title), el('p', '', text));
    return s;
  }

  function renderMap(t, cat) {
    const box = document.getElementById('g-map');
    box.replaceChildren();
    const nb = neighbours(t.id).slice(0, 9);
    const W = 340, H = 320, cx = W / 2, cy = H / 2, R = 102;
    const s = svg('svg', { viewBox: `0 0 ${W} ${H}`, role: 'group', 'aria-label': 'Connected terms' });
    const lines = svg('g'), nodes = svg('g');
    s.append(lines, nodes);
    const place = (id, x, y, r, main, label) => {
      const term = byId.get(id), c = catById.get(term.cat);
      const g = svg('g', { class: 'm-node' + (main ? ' main' : ''), tabindex: main ? '-1' : '0', role: main ? 'img' : 'button', 'aria-label': term.term });
      g.style.setProperty('--c', c.c);
      g.style.setProperty('--ct', c.ct);
      g.append(svg('circle', { cx: x, cy: y, r }));
      const sym = svg('text', { x, y: y + (main ? 6 : 4.5), 'text-anchor': 'middle', class: 'm-sym' });
      sym.textContent = term.sym;
      g.append(sym);
      if (label) g.append(label);
      if (!main) {
        g.addEventListener('click', () => open(id));
        g.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(id); } });
      }
      return g;
    };
    nb.forEach(([id, type], i) => {
      const a = -Math.PI / 2 + (i * 2 * Math.PI) / nb.length;
      const x = cx + R * Math.cos(a), y = cy + R * Math.sin(a);
      const ln = svg('line', { x1: cx, y1: cy, x2: x, y2: y, class: 'm-line' });
      ln.style.setProperty('--d', (i * 60) + 'ms');
      const ti = svg('title'); ti.textContent = type; ln.append(ti);
      lines.append(ln);
      const cs = Math.cos(a), sn = Math.sin(a);
      const lab = svg('text', {
        x: x + cs * 26, y: y + sn * 26 + 3.5,
        'text-anchor': cs > 0.3 ? 'start' : cs < -0.3 ? 'end' : 'middle', class: 'm-label'
      });
      lab.textContent = clip(byId.get(id).term.replace(/\s*\(.*?\)/, ''), 17);
      const g = place(id, x, y, 17, false, lab);
      g.style.setProperty('--d', (120 + i * 60) + 'ms');
      nodes.append(g);
    });
    const mainNode = place(t.id, cx, cy, 27, true);
    nodes.append(mainNode);
    box.append(s);
    if (!nb.length) box.append(el('p', 'g-hint', 'No linked terms yet.'));
    return nb;
  }

  function render(id) {
    const t = byId.get(id), cat = catById.get(t.cat);
    current = id;
    setVars(card, cat);
    const main = document.getElementById('g-main');
    main.replaceChildren();

    const top = el('div', 'g-top');
    const sym = el('div', 'g-sym', t.sym);
    const head = el('div', 'g-head');
    const chip = el('span', 'g-cat', `${cat.icon} ${cat.name}`);
    const title = el('h3', '', t.term);
    title.id = 'g-title';
    head.append(chip, title);
    if (t.aliases.length) head.append(el('p', 'g-alias', 'Also: ' + t.aliases.join(', ')));
    top.append(sym, head);
    main.append(top);

    if (t.weeks.length) {
      const w = el('div', 'g-weeks');
      t.weeks.forEach(n => w.append(el('span', '', 'Week ' + n)));
      main.append(w);
    }
    main.append(el('p', 'g-simple', t.simple));
    [section('Why it matters', t.why), section('Example', t.example),
     section('Common confusion', t.confusion), section('In our sessions', t.notes, 'notes')]
      .forEach(s => s && main.append(s));
    if (t.working) {
      const d = el('details', 'g-more');
      d.append(el('summary', '', 'Working definition'), el('p', '', t.working));
      main.append(d);
    }
    if (t.url) {
      const a = el('a', 'g-src', (t.src || 'Read more') + ' →');
      a.href = t.url; a.target = '_blank'; a.rel = 'noopener';
      main.append(a);
    }

    const nb = renderMap(t, cat);
    const list = document.getElementById('g-rel');
    list.replaceChildren();
    nb.forEach(([nid, type]) => {
      const b = el('button', 'g-rchip', byId.get(nid).term.replace(/\s*\(.*?\)/, ''));
      b.type = 'button';
      b.title = type;
      b.style.setProperty('--c', catById.get(byId.get(nid).cat).c);
      b.addEventListener('click', () => open(nid));
      list.append(b);
    });
    document.getElementById('g-pos').textContent = (() => {
      const v = visibleIds(); const i = v.indexOf(id);
      return i < 0 ? '' : `${i + 1} / ${v.length}`;
    })();
    main.scrollTop = 0;
    card.classList.remove('swap'); void card.offsetWidth; card.classList.add('swap');
  }

  function open(id) {
    if (!byId.has(id)) return;
    if (modal.hidden) {
      opener = document.activeElement;
      modal.hidden = false;
      document.body.classList.add('g-open');
      hideTip();
    }
    render(id);
    modal.querySelector('.g-x').focus({ preventScroll: true });
  }
  function close() {
    if (modal.hidden) return;
    modal.hidden = true;
    document.body.classList.remove('g-open');
    const back = tiles.get(current);
    (opener && document.contains(opener) ? opener : back)?.focus({ preventScroll: true });
  }
  function step(d) {
    const v = visibleIds();
    if (!v.length) return;
    let i = v.indexOf(current);
    i = i < 0 ? 0 : (i + d + v.length) % v.length;
    open(v[i]);
  }

  wall.addEventListener('click', e => {
    const t = e.target.closest('.tile');
    if (t) open(t.dataset.id);
  });
  modal.addEventListener('click', e => { if (e.target.closest('[data-close]')) close(); });
  document.getElementById('g-prev').addEventListener('click', () => step(-1));
  document.getElementById('g-next').addEventListener('click', () => step(1));
  document.getElementById('g-random').addEventListener('click', () => {
    const v = visibleIds().filter(i => i !== current);
    if (v.length) open(v[Math.floor(Math.random() * v.length)]);
  });
  document.getElementById('g-surprise').addEventListener('click', () => {
    const v = views[state.view];
    if (v && v.surprise) { v.surprise(); return; }
    const id = pickRandom();
    if (id) open(id);
  });
  setView(state.view);

  document.addEventListener('keydown', e => {
    if (!modal.hidden) {
      if (e.key === 'Escape') { e.preventDefault(); close(); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); step(1); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); step(-1); }
      else if (e.key === 'Tab') {
        const f = [...modal.querySelectorAll('button, a[href], [tabindex="0"], summary')].filter(n => n.offsetParent !== null || n.closest('svg'));
        if (!f.length) return;
        const first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
      return;
    }
    if (e.key === '/' && slide.classList.contains('active') && !e.target.closest('input, textarea')) {
      e.preventDefault();
      input.focus();
    }
  });
})();
