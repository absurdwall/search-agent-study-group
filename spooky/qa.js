(() => {
  "use strict";

  if (!window.SpookyQa) return;

  window.SpookyQa.mount({
    panel: document.querySelector("[data-spooky-qa]"),
    form: document.querySelector("[data-spooky-form]"),
    question: document.querySelector("#spooky-question"),
    submitButton: document.querySelector("[data-spooky-submit]"),
    status: document.querySelector("[data-spooky-status]"),
    result: document.querySelector("[data-spooky-result]"),
  });
})();
