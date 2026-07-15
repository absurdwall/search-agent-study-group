(() => {
  "use strict";

  const panel = document.querySelector("[data-spooky-qa]");
  const form = document.querySelector("[data-spooky-form]");
  const question = document.querySelector("#spooky-question");
  const submitButton = document.querySelector("[data-spooky-submit]");
  const status = document.querySelector("[data-spooky-status]");
  const result = document.querySelector("[data-spooky-result]");

  if (!panel || !form || !question || !submitButton || !status || !result) return;

  const localHostnames = new Set(["localhost", "127.0.0.1"]);
  const mockScenarios = new Set([
    "answer",
    "insufficient",
    "provider-unavailable",
    "error",
    "retry",
  ]);
  const isLocalhost = localHostnames.has(window.location.hostname);
  const requestedMock = new URLSearchParams(window.location.search).get("mock");
  const mockScenario = isLocalhost && mockScenarios.has(requestedMock)
    ? requestedMock
    : isLocalhost
      ? "answer"
      : "provider-unavailable";

  let lastMessage = "";
  let mockAttempt = 0;

  class SpookyApiError extends Error {
    constructor(statusCode, payload) {
      super(payload.error.message);
      this.name = "SpookyApiError";
      this.statusCode = statusCode;
      this.code = payload.error.code;
      this.requestId = payload.request_id;
    }
  }

  function element(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function mockSuccess({ withSources = true } = {}) {
    return {
      status: 200,
      payload: {
        answer: withSources
          ? "A tool is a callable capability an agent can use to interact with systems or retrieve information."
          : "I could not find a published glossary record that supports an answer to that question.",
        sources: withSources
          ? [{ title: "Tool", url: "../glossary/#tool" }]
          : [],
        request_id: withSources ? "req_mock_answer" : "req_mock_insufficient",
      },
    };
  }

  function mockError(statusCode, code, message, requestId) {
    return {
      status: statusCode,
      payload: {
        error: { code, message },
        request_id: requestId,
      },
    };
  }

  function selectedMockResponse() {
    mockAttempt += 1;
    if (mockScenario === "insufficient") return mockSuccess({ withSources: false });
    if (mockScenario === "provider-unavailable") {
      return mockError(
        503,
        "PROVIDER_UNAVAILABLE",
        "Spooky's model provider is unavailable. Try again later.",
        "req_mock_provider_unavailable",
      );
    }
    if (mockScenario === "error") {
      return mockError(
        500,
        "INTERNAL_ERROR",
        "Spooky could not complete the request.",
        "req_mock_internal_error",
      );
    }
    if (mockScenario === "retry" && mockAttempt === 1) {
      return mockError(
        504,
        "REQUEST_TIMEOUT",
        "Spooky did not respond before the timeout.",
        "req_mock_timeout",
      );
    }
    return mockSuccess();
  }

  // This is the only request boundary. Replace its deterministic mock body with
  // the frozen POST /v1/chat integration after the public API origin is decided.
  async function askSpooky(message) {
    void message;
    await new Promise((resolve) => window.setTimeout(resolve, 450));
    const response = selectedMockResponse();
    if (response.status !== 200) {
      throw new SpookyApiError(response.status, response.payload);
    }
    return response.payload;
  }

  function setBusy(stateName) {
    const busy = stateName === "loading" || stateName === "retrying";
    panel.dataset.state = stateName;
    panel.setAttribute("aria-busy", String(busy));
    question.readOnly = busy;
    submitButton.disabled = busy || !question.value.trim();
    submitButton.textContent = busy
      ? stateName === "retrying" ? "Retrying…" : "Asking…"
      : "Ask Spooky";
  }

  function resetResult() {
    result.hidden = true;
    result.removeAttribute("data-kind");
    result.replaceChildren();
  }

  function focusResult() {
    requestAnimationFrame(() => result.focus({ preventScroll: true }));
  }

  function safeSourceUrl(value) {
    try {
      const url = new URL(value, document.baseURI);
      return url.protocol === "http:" || url.protocol === "https:" ? value : null;
    } catch (_error) {
      return null;
    }
  }

  function renderSources(sources) {
    const heading = element("h4", "", "Sources");
    const list = element("ul", "spooky-qa-sources");
    sources.forEach((source) => {
      const href = safeSourceUrl(source.url);
      if (!href) return;
      const item = document.createElement("li");
      const link = element("a", "", source.title);
      link.href = href;
      item.append(link);
      list.append(item);
    });
    return list.childElementCount ? [heading, list] : [];
  }

  function askAnotherButton() {
    const button = element("button", "spooky-qa-secondary-button", "Ask another question");
    button.type = "button";
    button.addEventListener("click", () => {
      question.focus();
      question.select();
    });
    return button;
  }

  function renderSuccess(payload) {
    const hasCoverage = payload.sources.length > 0;
    const kind = hasCoverage ? "answer" : "insufficient";
    setBusy(kind);
    status.textContent = hasCoverage ? "Answer ready." : "No supporting source was found.";
    result.dataset.kind = kind;
    result.replaceChildren(
      element("h3", "", hasCoverage ? "Spooky says" : "Insufficient coverage"),
      element("p", "", payload.answer),
    );
    if (hasCoverage) {
      result.append(...renderSources(payload.sources));
    } else {
      result.append(
        element(
          "p",
          "spooky-qa-result-note",
          "Try asking about a concept that appears in the published glossary.",
        ),
        element("div", "spooky-qa-actions"),
      );
      result.querySelector(".spooky-qa-actions").append(askAnotherButton());
    }
    result.hidden = false;
    focusResult();
  }

  function renderError(error) {
    const isProviderUnavailable = error.code === "PROVIDER_UNAVAILABLE";
    const kind = isProviderUnavailable ? "provider-unavailable" : "error";
    setBusy(kind);
    status.textContent = isProviderUnavailable ? "Provider unavailable." : "Request failed.";
    result.dataset.kind = kind;
    result.replaceChildren(
      element("h3", "", isProviderUnavailable ? "Provider unavailable" : "Spooky could not answer"),
      element("p", "", error.message),
    );

    const actions = element("div", "spooky-qa-actions");
    const retryButton = element("button", "spooky-qa-secondary-button", "Retry last question");
    retryButton.type = "button";
    retryButton.addEventListener("click", () => submitQuestion({ isRetry: true }));
    actions.append(retryButton);
    result.append(
      actions,
      element("p", "spooky-qa-request-id", `Reference: ${error.requestId}`),
    );
    result.hidden = false;
    focusResult();
  }

  async function submitQuestion({ isRetry = false } = {}) {
    const message = isRetry ? lastMessage : question.value.trim();
    if (!message) {
      question.setCustomValidity("Enter a question for Spooky.");
      question.reportValidity();
      question.focus();
      return;
    }

    question.setCustomValidity("");
    lastMessage = message;
    resetResult();
    setBusy(isRetry ? "retrying" : "loading");
    status.textContent = isRetry
      ? "Retrying your last question…"
      : "Spooky is looking through the published study materials…";

    try {
      renderSuccess(await askSpooky(message));
    } catch (error) {
      if (error instanceof SpookyApiError) {
        renderError(error);
      } else {
        renderError(
          new SpookyApiError(500, {
            error: { code: "INTERNAL_ERROR", message: "Spooky could not complete the request." },
            request_id: "req_browser_error",
          }),
        );
      }
    }
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    submitQuestion();
  });

  question.addEventListener("input", () => {
    question.setCustomValidity("");
    if (panel.getAttribute("aria-busy") !== "true") {
      submitButton.disabled = !question.value.trim();
    }
  });

  question.addEventListener("keydown", (event) => {
    if (event.key !== "Enter" || (!event.metaKey && !event.ctrlKey)) return;
    event.preventDefault();
    if (panel.getAttribute("aria-busy") !== "true") form.requestSubmit();
  });
})();
