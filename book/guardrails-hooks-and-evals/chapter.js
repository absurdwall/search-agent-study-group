(() => {
  'use strict';
  const timing = {
    pre: {
      steps: [
        ['Propose', 'The agent asks to move B onto A’s occupied destination.', ''],
        ['PreToolUse: inspect', 'The hook sees A at the destination and returns a denial.', 'blocked'],
        ['Tool not called', 'The runtime prevents this move from executing.', ''],
        ['Observe and revise', 'The agent receives the refusal reason and can choose another path.', '']
      ],
      title: 'Prevented before execution: the hook denied this call.',
      text: 'A remains at the destination; B remains at its source. The agent receives the reason and can choose another name.',
      tone: 'safe'
    },
    post: {
      steps: [
        ['Propose', 'The agent asks to move B onto A’s occupied destination.', ''],
        ['Replacing move executes', 'B moves to the destination, replacing A’s contents; B’s source is removed.', 'done'],
        ['PostToolUse: detect', 'The hook reports the violation after the operation has completed.', 'blocked'],
        ['Report and recover', 'Restoring A requires a backup or another real recovery source; the warning cannot restore it.', '']
      ],
      title: 'Detected after execution: A has already been overwritten.',
      text: 'B is now at the destination, and its source is gone. A’s original destination contents are lost in this scenario. Rejecting the result does not reverse the move; no backup or rollback is assumed.',
      tone: 'warning'
    },
    tool: {
      steps: [
        ['Propose', 'The agent asks to move B onto A’s occupied destination.', ''],
        ['Call the move tool', 'The tool receives the request without any Agent Hook.', ''],
        ['Enforce at the mutation', 'The storage operation refuses the occupied destination rather than replacing it.', 'blocked'],
        ['Return the refusal', 'The tool reports the conflict so the agent can choose another name.', '']
      ],
      title: 'Prevented inside the operation: no-replace refused the move.',
      text: 'A remains at the destination; B remains at its source. The storage condition is checked as part of the operation, even if no hook ran or another process occupied the path after an earlier check.',
      tone: 'safe'
    }
  };
  const cases = {
    valid: {
      rows: [['Receipts/printer.pdf', 'A'], ['Notes/planning.txt', 'B'], ['Notes/planning-copy.txt', 'B']],
      moved: true,
      title: 'The original contents and required paths are present.',
      text: 'These checks do not decide whether the chosen categories help the user.'
    },
    corrupt: {
      rows: [['Receipts/printer.pdf', 'A'], ['Notes/planning.txt', 'B'], ['Notes/planning-copy.txt', 'C']],
      moved: true,
      title: 'Three files remain, but one original’s contents changed.',
      text: 'One original B has become C. Counting three files would miss this change.'
    },
    duplicate: {
      rows: [['Receipts/printer.pdf', 'A'], ['Notes/planning.txt', 'B']],
      moved: false,
      title: 'One copy is missing, even though A and B are present.',
      text: 'There should be two copies of B. Checking only that A and B exist would miss the lost copy.'
    },
    untouched: {
      rows: [['Inbox/download.pdf', 'A'], ['Inbox/notes.txt', 'B'], ['Inbox/notes-copy.txt', 'B']],
      moved: false,
      title: 'All contents remain, but the requested moves are missing.',
      text: 'The originals survived, but the requested moves did not happen. Report safety and completion separately.'
    }
  };
  function node(tag, text, className) {
    const el = document.createElement(tag);
    if (text !== undefined) el.textContent = text;
    if (className) el.className = className;
    return el;
  }
  function selectButtons(selector, key, attribute) {
    document.querySelectorAll(selector).forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset[attribute] === key));
    });
  }
  function renderTiming(key) {
    const data = timing[key];
    if (!data) return;
    const list = node('ol', undefined, 'timeline');
    data.steps.forEach(([title, text, state], i) => {
      const li = node('li');
      if (state) li.dataset.state = state;
      li.append(node('span', String(i + 1), 'step-number'));
      const content = node('div');
      content.append(node('strong', title), node('p', text));
      li.append(content);
      list.append(li);
    });
    const verdict = node('div', undefined, 'verdict');
    verdict.dataset.tone = data.tone;
    verdict.append(node('strong', data.title), node('p', data.text));
    document.getElementById('timing-content').replaceChildren(list, verdict);
    selectButtons('[data-timing]', key, 'timing');
  }
  function renderEvidence(key) {
    const data = cases[key];
    if (!data) return;
    const rows = data.rows.map(([path, identity]) => {
      const tr = node('tr');
      const td = node('td');
      td.append(node('code', path));
      tr.append(td, node('td', identity));
      return tr;
    });
    document.getElementById('artifact-rows').replaceChildren(...rows);
    const counts = data.rows.reduce((acc, [, id]) => {
      acc[id] = (acc[id] || 0) + 1;
      return acc;
    }, {});
    const preserved = counts.A === 1 && counts.B === 2 && Object.keys(counts).length === 2;
    const countOK = data.rows.length === 3;
    const expectedPaths = ['Receipts/printer.pdf', 'Notes/planning.txt', 'Notes/planning-copy.txt'];
    const pathsOK = expectedPaths.every(path => data.rows.some(([p]) => p === path));
    const identityText = Object.entries(counts).map(([id, n]) => `${id} × ${n}`).join(', ');
    const checks = [
      [countOK ? 'PASS' : 'FAIL', `File count: ${data.rows.length} of 3.`, countOK ? 'pass' : 'fail'],
      [preserved ? 'PASS' : 'FAIL', `Contents and copies: ${identityText}. Expected A × 1, B × 2.`, preserved ? 'pass' : 'fail'],
      [pathsOK ? 'PASS' : 'FAIL', `Required paths: ${pathsOK ? 'intended paths are present' : 'the requested reorganization is incomplete'}.`, pathsOK ? 'pass' : 'fail'],
      ['REVIEW', 'A person or content-aware grader must judge whether the categories are useful.', 'review']
    ];
    const list = checks.map(([status, text, result]) => {
      const li = node('li');
      const label = node('span', status, 'check-status');
      label.dataset.result = result;
      li.append(label, document.createTextNode(' ' + text));
      return li;
    });
    document.getElementById('artifact-checks').replaceChildren(...list);
    const verdict = document.getElementById('artifact-verdict');
    verdict.dataset.tone = preserved && pathsOK ? 'safe' : 'warning';
    verdict.replaceChildren(node('strong', data.title), node('p', data.text));
    selectButtons('[data-evidence]', key, 'evidence');
  }
  document.querySelectorAll('[data-timing]').forEach(button => {
    button.addEventListener('click', () => renderTiming(button.dataset.timing));
  });
  document.querySelectorAll('[data-evidence]').forEach(button => {
    button.addEventListener('click', () => renderEvidence(button.dataset.evidence));
  });
  renderTiming('pre');
  renderEvidence('valid');
  document.querySelectorAll('[data-enhance]').forEach(el => { el.hidden = false; });
})();

// Product references are parallel alternatives. The tutorial itself remains sequential.
(() => {
  'use strict';
  const groups = new Map();
  document.querySelectorAll('[data-tabs]').forEach(group => {
    const bar = group.querySelector('[data-tab-controls]');
    const tabs = Array.from(bar.querySelectorAll('button[aria-controls]'));
    const activate = (tab, moveFocus = false) => {
      tabs.forEach(item => {
        const selected = item === tab;
        item.setAttribute('aria-selected', String(selected));
        item.setAttribute('tabindex', selected ? '0' : '-1');
        document.getElementById(item.getAttribute('aria-controls')).hidden = !selected;
      });
      if (moveFocus) tab.focus();
    };
    bar.setAttribute('role', 'tablist');
    tabs.forEach((tab, index) => {
      tab.setAttribute('role', 'tab');
      const panel = document.getElementById(tab.getAttribute('aria-controls'));
      panel.setAttribute('role', 'tabpanel');
      panel.setAttribute('aria-labelledby', tab.id);
      panel.setAttribute('tabindex', '0');
      tab.addEventListener('click', () => activate(tab));
      tab.addEventListener('focus', () => activate(tab));
      tab.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        if (next !== undefined) {
          event.preventDefault();
          activate(tabs[next], true);
        }
      });
    });
    groups.set(group, { tabs, activate });
    activate(tabs[0]);
    bar.hidden = false;
  });

  // Existing and new fragment links reveal their target even inside closed details or another tab.
  function revealFragment(hash, scroll = false) {
    if (!hash || hash === '#') return;
    let id;
    try { id = decodeURIComponent(hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (!target) return;
    for (let item = target; item; item = item.parentElement) {
      if (item.tagName === 'DETAILS') item.setAttribute('open', '');
      if (item.hasAttribute('data-tab-panel')) {
        const group = item.closest('[data-tabs]');
        const state = groups.get(group);
        const tab = state && state.tabs.find(t => t.getAttribute('aria-controls') === item.id);
        if (tab) state.activate(tab);
      }
    }
    if (scroll && typeof target.scrollIntoView === 'function') target.scrollIntoView({ block: 'start' });
  }
  document.addEventListener('click', event => {
    const anchor = event.target.closest && event.target.closest('a[href^="#"]');
    if (anchor) revealFragment(anchor.getAttribute('href'));
  });
  window.addEventListener('hashchange', () => revealFragment(window.location.hash, true));
  revealFragment(window.location.hash, true);

  // Printing exposes optional reference text, then restores the reader's disclosure choices.
  let closedForPrint = null;
  window.addEventListener('beforeprint', () => {
    if (closedForPrint) return;
    closedForPrint = Array.from(document.querySelectorAll('main details:not([open])'));
    closedForPrint.forEach(item => { item.setAttribute('open', ''); });
  });
  window.addEventListener('afterprint', () => {
    if (!closedForPrint) return;
    closedForPrint.forEach(item => { item.removeAttribute('open'); });
    closedForPrint = null;
  });
})();
