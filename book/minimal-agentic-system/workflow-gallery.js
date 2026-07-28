document.querySelectorAll("[data-workflow-gallery]").forEach((gallery) => {
  const tabList = gallery.querySelector('[role="tablist"]');
  const tabs = Array.from(gallery.querySelectorAll('[role="tab"]'));
  const panels = Array.from(gallery.querySelectorAll("[data-workflow-panel]"));
  const status = gallery.querySelector("[data-workflow-status]");
  const navigation = gallery.querySelector("[data-workflow-nav]");
  const previousButton = gallery.querySelector("[data-workflow-previous]");
  const nextButton = gallery.querySelector("[data-workflow-next]");
  const position = gallery.querySelector("[data-workflow-position]");

  if (!tabList || tabs.length !== panels.length) {
    return;
  }

  const selectPattern = (index, moveFocus = false) => {
    tabs.forEach((tab, tabIndex) => {
      const selected = tabIndex === index;
      tab.setAttribute("aria-selected", String(selected));
      tab.tabIndex = selected ? 0 : -1;
      panels[tabIndex].hidden = !selected;
    });

    if (status) {
      status.textContent = `Selected workflow pattern: ${tabs[index].textContent}.`;
    }

    if (previousButton) {
      previousButton.disabled = index === 0;
    }

    if (nextButton) {
      nextButton.disabled = index === tabs.length - 1;
    }

    if (position) {
      position.textContent = `${index + 1} of ${tabs.length}`;
    }

    if (moveFocus) {
      tabs[index].focus();
    }
  };

  panels.forEach((panel, index) => {
    panel.setAttribute("role", "tabpanel");
    panel.setAttribute("aria-labelledby", tabs[index].id);
    panel.tabIndex = 0;
  });

  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => selectPattern(index));
    tab.addEventListener("keydown", (event) => {
      let nextIndex = index;

      if (event.key === "ArrowRight" || event.key === "ArrowDown") {
        nextIndex = (index + 1) % tabs.length;
      } else if (event.key === "ArrowLeft" || event.key === "ArrowUp") {
        nextIndex = (index - 1 + tabs.length) % tabs.length;
      } else if (event.key === "Home") {
        nextIndex = 0;
      } else if (event.key === "End") {
        nextIndex = tabs.length - 1;
      } else {
        return;
      }

      event.preventDefault();
      selectPattern(nextIndex, true);
    });
  });

  previousButton?.addEventListener("click", () => {
    const selectedIndex = tabs.findIndex(
      (tab) => tab.getAttribute("aria-selected") === "true",
    );

    if (selectedIndex > 0) {
      selectPattern(selectedIndex - 1);
    }
  });

  nextButton?.addEventListener("click", () => {
    const selectedIndex = tabs.findIndex(
      (tab) => tab.getAttribute("aria-selected") === "true",
    );

    if (selectedIndex < tabs.length - 1) {
      selectPattern(selectedIndex + 1);
    }
  });

  tabList.hidden = false;
  if (navigation) {
    navigation.hidden = false;
  }
  selectPattern(0);
});
