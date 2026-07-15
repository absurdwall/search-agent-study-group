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
  const apiErrorMessages = new Map([
    ["INVALID_REQUEST", "Request body must contain only a string message."],
    ["EMPTY_MESSAGE", "message must contain non-whitespace characters."],
    ["MESSAGE_TOO_LARGE", "message must be at most 2000 characters."],
    ["PROVIDER_UNAVAILABLE", "Spooky's model provider is unavailable. Try again later."],
    ["REQUEST_TIMEOUT", "Spooky did not respond before the timeout."],
    ["INTERNAL_ERROR", "Spooky could not complete the request."],
  ]);
  const isLocalhost = localHostnames.has(window.location.hostname);
  const requestedMock = new URLSearchParams(window.location.search).get("mock");
  const mockScenario = isLocalhost && mockScenarios.has(requestedMock) ? requestedMock : null;

  let lastMessage = "";
  let mockAttempt = 0;

  class SpookyApiError extends Error {
    constructor(statusCode, code, message, requestId = null) {
      super(message);
      this.name = "SpookyApiError";
      this.statusCode = statusCode;
      this.code = code;
      this.requestId = requestId;
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

  function isRecord(value) {
    return value !== null && typeof value === "object" && !Array.isArray(value);
  }

  function isSuccessPayload(payload) {
    return isRecord(payload)
      && typeof payload.answer === "string"
      && typeof payload.request_id === "string"
      && Array.isArray(payload.sources)
      && payload.sources.every(
        (source) => isRecord(source)
          && typeof source.title === "string"
          && typeof source.url === "string",
      );
  }

  function isErrorPayload(payload) {
    return isRecord(payload)
      && isRecord(payload.error)
      && apiErrorMessages.get(payload.error.code) === payload.error.message
      && typeof payload.request_id === "string";
  }

  function clientError(code, message) {
    return new SpookyApiError(null, code, message);
  }

  function parseApiResponse(statusCode, payload) {
    const succeeded = statusCode === 200;
    if (succeeded && isSuccessPayload(payload)) return payload;
    if (!succeeded && isErrorPayload(payload)) {
      throw new SpookyApiError(
        statusCode,
        payload.error.code,
        apiErrorMessages.get(payload.error.code),
        payload.request_id,
      );
    }
    throw clientError("INVALID_RESPONSE", "Spooky returned an unreadable response. Try again later.");
  }

  // This is the only network boundary. Explicit localhost mock scenarios stay
  // deterministic; the unparameterized localhost page calls the frozen API.
  async function askSpooky(message) {
    if (mockScenario !== null) {
      await new Promise((resolve) => window.setTimeout(resolve, 450));
      const mockResponse = selectedMockResponse();
      return parseApiResponse(mockResponse.status, mockResponse.payload);
    }
    if (!isLocalhost) {
      throw clientError("LOCAL_ONLY", "Spooky is available only from the local study-group site.");
    }
    if (requestedMock !== null) {
      throw clientError("INVALID_MOCK", "That local mock scenario is not available.");
    }

    let response;
    try {
      response = await fetch("http://127.0.0.1:8001/v1/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
    } catch (_error) {
      throw clientError(
        "NETWORK_ERROR",
        "The local Spooky API could not be reached. Make sure it is running and try again.",
      );
    }

    let payload;
    try {
      payload = await response.json();
    } catch (_error) {
      throw clientError("INVALID_RESPONSE", "Spooky returned an unreadable response. Try again later.");
    }
    return parseApiResponse(response.status, payload);
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
    result.append(actions);
    if (error.requestId) {
      result.append(element("p", "spooky-qa-request-id", `Reference: ${error.requestId}`));
    }
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
        renderError(clientError("BROWSER_ERROR", "Spooky could not complete the request."));
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
