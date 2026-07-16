(() => {
  "use strict";

  if (!window.SpookyQa || document.querySelector("[data-spooky-launcher]")) return;

  const launcher = document.createElement("div");
  launcher.className = "spooky-launcher";
  launcher.dataset.spookyLauncher = "";
  launcher.innerHTML = `
    <button
      class="spooky-launcher-toggle"
      type="button"
      aria-label="Ask Spooky"
      aria-haspopup="dialog"
      aria-expanded="false"
      aria-controls="spooky-launcher-dialog"
      data-spooky-launcher-toggle
    >
      <span aria-hidden="true">👻</span>
      <span>Ask Spooky</span>
    </button>
    <section
      class="spooky-launcher-dialog"
      id="spooky-launcher-dialog"
      role="dialog"
      aria-modal="false"
      aria-labelledby="spooky-launcher-title"
      data-spooky-launcher-dialog
      hidden
    >
      <header class="spooky-launcher-header">
        <div>
          <h2 id="spooky-launcher-title">Ask Spooky <span aria-hidden="true">👻</span></h2>
          <p>One question about the published glossary.</p>
        </div>
        <button
          class="spooky-launcher-close"
          type="button"
          aria-label="Close Ask Spooky"
          data-spooky-launcher-close
        >×</button>
      </header>
      <div class="spooky-qa spooky-launcher-qa" data-spooky-qa data-state="idle" aria-busy="false">
        <form class="spooky-qa-form" data-spooky-form>
          <label class="spooky-qa-label" for="spooky-launcher-question">Your question</label>
          <textarea
            id="spooky-launcher-question"
            name="message"
            rows="3"
            maxlength="2000"
            required
            aria-describedby="spooky-launcher-help"
            placeholder="What is a tool in an agent system?"
          ></textarea>
          <div class="spooky-qa-form-footer">
            <p class="spooky-qa-hint" id="spooky-launcher-help">
              <kbd>⌘</kbd>/<kbd>Ctrl</kbd> + <kbd>Enter</kbd> to submit.
            </p>
            <button class="spooky-qa-button" type="submit" data-spooky-submit disabled>
              Ask Spooky
            </button>
          </div>
        </form>
        <p class="spooky-qa-status" data-spooky-status role="status" aria-live="polite"></p>
        <div class="spooky-qa-result" data-spooky-result tabindex="-1" hidden></div>
      </div>
    </section>
  `;

  document.body.append(launcher);

  const toggle = launcher.querySelector("[data-spooky-launcher-toggle]");
  const dialog = launcher.querySelector("[data-spooky-launcher-dialog]");
  const closeButton = launcher.querySelector("[data-spooky-launcher-close]");
  const panel = launcher.querySelector("[data-spooky-qa]");
  const question = launcher.querySelector("#spooky-launcher-question");

  window.SpookyQa.mount({
    panel,
    form: launcher.querySelector("[data-spooky-form]"),
    question,
    submitButton: launcher.querySelector("[data-spooky-submit]"),
    status: launcher.querySelector("[data-spooky-status]"),
    result: launcher.querySelector("[data-spooky-result]"),
  });

  function openDialog() {
    dialog.hidden = false;
    toggle.setAttribute("aria-expanded", "true");
    requestAnimationFrame(() => question.focus());
  }

  function closeDialog() {
    dialog.hidden = true;
    toggle.setAttribute("aria-expanded", "false");
    toggle.focus();
  }

  toggle.addEventListener("click", () => {
    if (dialog.hidden) openDialog();
    else closeDialog();
  });
  closeButton.addEventListener("click", closeDialog);
  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape" || dialog.hidden) return;
    event.preventDefault();
    closeDialog();
  });
})();
