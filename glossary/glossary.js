(() => {
  "use strict";

  const state = {
    terms: [],
    query: "",
    category: "all",
    activeId: null,
    activeLevel: 0,
  };

  const list = document.querySelector("#glossary-list");
  const search = document.querySelector("#glossary-search");
  const filters = document.querySelector("#category-filters");
  const summary = document.querySelector("#results-summary");
  const noResults = document.querySelector("#no-results");
  const clearButton = document.querySelector("#clear-filters");
  const cardTransforms = [
    ["-0.55deg", "-1px"],
    ["0.35deg", "1px"],
    ["-0.2deg", "2px"],
    ["0.6deg", "-1px"],
    ["-0.4deg", "1px"],
    ["0.18deg", "-2px"],
  ];

  function labelForSlug(value) {
    return value
      .split("-")
      .map((part, index) => {
        if (index > 0 && ["and", "or", "of"].includes(part)) return part;
        return part.charAt(0).toUpperCase() + part.slice(1);
      })
      .join(" ");
  }

  function relationLabel(value) {
    return value.replaceAll("_", " ");
  }

  function weekLabel(value) {
    const match = /^week-(\d+)$/.exec(value);
    return match ? `Week ${Number(match[1])}` : labelForSlug(value);
  }

  function element(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function replaceHash(termId) {
    const url = new URL(window.location.href);
    url.hash = termId ? `#${termId}` : "";
    history.replaceState(null, "", url);
  }

  function resetActiveCard({ clearHash = true } = {}) {
    state.activeId = null;
    state.activeLevel = 0;
    if (clearHash) replaceHash(null);
  }

  function findTerm(termId) {
    return state.terms.find((term) => term.id === termId);
  }

  function matches(term) {
    if (state.category !== "all" && term.category !== state.category) return false;
    if (!state.query) return true;
    const searchable = [
      term.term,
      ...term.aliases,
      term.sections["Simple definition"],
      term.sections["Working definition"],
      term.sections["Why it matters"],
    ].join(" ").toLocaleLowerCase();
    return searchable.includes(state.query);
  }

  function visibleTerms() {
    return state.terms.filter(matches);
  }

  function keepActiveIfVisible() {
    if (!state.activeId) return;
    const activeTerm = findTerm(state.activeId);
    if (!activeTerm || !matches(activeTerm)) resetActiveCard();
  }

  function renderFilters() {
    const categories = [...new Set(state.terms.map((term) => term.category))].sort();
    filters.replaceChildren();
    [{ id: "all", label: "All" }, ...categories.map((id) => ({ id, label: labelForSlug(id) }))]
      .forEach(({ id, label }) => {
        const button = element("button", "filter-button", label);
        button.type = "button";
        button.dataset.category = id;
        button.setAttribute("aria-pressed", String(state.category === id));
        button.addEventListener("click", () => {
          state.category = id;
          keepActiveIfVisible();
          renderFilters();
          renderTerms();
        });
        filters.append(button);
      });
  }

  function detailSection(title, text) {
    const section = element("section", "term-detail-section");
    section.append(element("h3", "", title), element("p", "", text));
    return section;
  }

  function references(term) {
    const section = element("section", "term-detail-section term-reference-section");
    section.append(element("h3", "", "References"));
    const sourceList = element("ol", "term-sources");
    term.sources.forEach((source) => {
      const item = document.createElement("li");
      const link = element("a", "", source.title);
      link.href = source.url;
      link.rel = "noopener noreferrer";
      item.append(link, element("p", "", source.note));
      sourceList.append(item);
    });
    section.append(sourceList);
    return section;
  }

  function openFullTerm(termId, { updateHash = true, clearFiltersIfNeeded = true } = {}) {
    const term = findTerm(termId);
    if (!term) return;

    if (clearFiltersIfNeeded && !matches(term)) {
      state.query = "";
      state.category = "all";
      search.value = "";
      renderFilters();
    }

    state.activeId = termId;
    state.activeLevel = 2;
    if (updateHash) replaceHash(termId);
    renderTerms({ focusId: termId, scrollToCard: true });
  }

  function relatedConcepts(term) {
    const wrap = element("div", "term-relations");
    wrap.append(element("span", "term-relations-label", "Connections"));
    term.relations.forEach((relation) => {
      const target = findTerm(relation.target);
      const link = element("a", "relation-link");
      link.href = `#${relation.target}`;
      link.textContent = `${relationLabel(relation.type)} · ${target?.term ?? relation.target}`;
      link.addEventListener("click", (event) => {
        event.preventDefault();
        openFullTerm(relation.target);
      });
      wrap.append(link);
    });
    return wrap;
  }

  function expandedContent(term) {
    const content = element("div", "term-expanded-content");
    content.id = `${term.id}-content`;

    const meta = element("div", "term-meta");
    meta.append(
      element("span", "term-category", labelForSlug(term.category)),
      element("span", "term-week", weekLabel(term.introduced_in)),
      element("span", "term-aliases", `Also: ${term.aliases.join(" · ")}`),
    );

    const overview = element("div", "term-overview");
    overview.append(
      detailSection("Working definition", term.sections["Working definition"]),
      detailSection("Why it matters", term.sections["Why it matters"]),
      relatedConcepts(term),
    );

    const detailGrid = element("div", "term-detail-grid");
    detailGrid.append(
      detailSection("Example", term.sections.Example),
      detailSection("Common confusion", term.sections["Common confusion"]),
    );
    if (term.sections["Study-group notes"]) {
      detailGrid.append(detailSection("Study-group notes", term.sections["Study-group notes"]));
    }
    detailGrid.append(references(term));

    content.append(meta, overview, detailGrid);
    return content;
  }

  function cardState(term) {
    if (state.activeId !== term.id) return "collapsed";
    return state.activeLevel === 2 ? "expanded" : "preview";
  }

  function triggerLabel(term, currentState) {
    if (currentState === "collapsed") return `Show a simple definition for ${term.term}`;
    if (currentState === "preview") return `Show full details for ${term.term}`;
    return `Collapse ${term.term}`;
  }

  function advanceCard(termId) {
    if (state.activeId !== termId) {
      state.activeId = termId;
      state.activeLevel = 1;
      replaceHash(null);
    } else if (state.activeLevel === 1) {
      state.activeLevel = 2;
      replaceHash(termId);
    } else {
      resetActiveCard();
    }
    renderTerms({ focusId: termId, scrollToCard: state.activeLevel === 2 });
  }

  function termCard(term, index) {
    const currentState = cardState(term);
    const article = element("article", `term-card term-card--${currentState}`);
    article.id = term.id;
    article.dataset.category = term.category;
    article.dataset.state = currentState;
    const [tilt, shift] = cardTransforms[index % cardTransforms.length];
    article.style.setProperty("--card-tilt", tilt);
    article.style.setProperty("--card-shift", shift);

    const trigger = element("button", "term-card-trigger");
    trigger.type = "button";
    trigger.setAttribute("aria-expanded", String(currentState !== "collapsed"));
    trigger.setAttribute("aria-controls", `${term.id}-content`);
    trigger.setAttribute("aria-label", triggerLabel(term, currentState));
    trigger.append(element("span", "term-title", term.term));

    if (currentState === "preview") {
      const simpleDefinition = element(
        "span",
        "term-simple-definition",
        term.sections["Simple definition"],
      );
      simpleDefinition.id = `${term.id}-content`;
      trigger.append(
        simpleDefinition,
        element("span", "term-action-hint", "Click again for the full concept →"),
      );
    } else if (currentState === "expanded") {
      trigger.append(element("span", "term-action-hint", "Collapse concept ↑"));
    }
    trigger.addEventListener("click", () => advanceCard(term.id));
    article.append(trigger);

    if (currentState === "expanded") {
      article.append(expandedContent(term));
    } else if (currentState === "collapsed") {
      const controlledContent = document.createElement("div");
      controlledContent.id = `${term.id}-content`;
      controlledContent.hidden = true;
      article.append(controlledContent);
    }

    return article;
  }

  function restoreFocus(termId, scrollToCard) {
    const card = document.getElementById(termId);
    const trigger = card?.querySelector(".term-card-trigger");
    if (!card || !trigger) return;
    if (scrollToCard) {
      const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      card.scrollIntoView({ block: "start", behavior: reducedMotion ? "auto" : "smooth" });
    }
    trigger.focus({ preventScroll: true });
  }

  function renderTerms({ focusId = null, scrollToCard = false } = {}) {
    const visible = visibleTerms();
    list.replaceChildren(...visible.map(termCard));
    list.setAttribute("aria-busy", "false");
    noResults.hidden = visible.length !== 0;
    list.hidden = visible.length === 0;
    const qualifier = state.terms.length === visible.length ? "" : ` of ${state.terms.length}`;
    summary.textContent = `${visible.length}${qualifier} concept${visible.length === 1 ? "" : "s"} shown`;
    if (focusId) requestAnimationFrame(() => restoreFocus(focusId, scrollToCard));
  }

  function clearFilters() {
    state.query = "";
    state.category = "all";
    search.value = "";
    resetActiveCard();
    renderFilters();
    renderTerms();
    search.focus();
  }

  function openHashTarget() {
    const termId = decodeURIComponent(location.hash.slice(1));
    if (!termId) {
      if (state.activeLevel === 2) {
        resetActiveCard({ clearHash: false });
        renderTerms();
      }
      return;
    }
    openFullTerm(termId, { updateHash: false });
  }

  async function load() {
    try {
      const response = await fetch("terms.json");
      if (!response.ok) throw new Error(`Glossary data returned ${response.status}`);
      const payload = await response.json();
      if (!Array.isArray(payload.terms)) throw new Error("Glossary data has an invalid shape");
      state.terms = payload.terms.filter((term) => term.status === "published");
      renderFilters();
      renderTerms();
      requestAnimationFrame(openHashTarget);
    } catch (error) {
      list.setAttribute("aria-busy", "false");
      list.replaceChildren(
        element("p", "glossary-state glossary-error", "The glossary could not load. Please refresh the page or try again later."),
      );
      console.error(error);
    }
  }

  search.addEventListener("input", () => {
    state.query = search.value.trim().toLocaleLowerCase();
    keepActiveIfVisible();
    renderTerms();
  });
  clearButton.addEventListener("click", clearFilters);
  window.addEventListener("hashchange", openHashTarget);
  load();
})();
