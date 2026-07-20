(() => {
  "use strict";

  const chatEndpoint = "https://spooky-api-jcysmpnqda-ue.a.run.app/v1/chat";
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

  function readableAnswerText(markdown) {
    return markdown
      .replace(/\[([^\]\n]+)\]\([^)\n]+\)/g, "$1")
      .replace(/\*\*([^\n]+?)\*\*/g, "$1")
      .replace(/__([^\n]+?)__/g, "$1")
      .split("\n")
      .map((line) => line
        .replace(/^\s*#{1,6}\s+/, "")
        .replace(/^\s*[-+*]\s+/, "• "))
      .join("\n")
      .replace(/\*([^*\n]+)\*/g, "$1")
      .replace(/_([^_\n]+)_/g, "$1")
      .replace(/`([^`\n]+)`/g, "$1")
      .trim();
  }

  function mockSuccess(glossaryUrl, { withSources = true } = {}) {
    return {
      status: 200,
      payload: {
        answer: withSources
          ? [
              "A **Tool** is a callable capability an agent can use to interact with systems.",
              "",
              "* It can retrieve information.",
              "* It can perform an *action*.",
            ].join("\n")
          : "I could not find a published glossary record that supports an answer to that question.",
        sources: withSources
          ? [{ title: "Tool", url: glossaryUrl }]
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
    if (statusCode === 200 && isSuccessPayload(payload)) return payload;
    if (statusCode !== 200 && isErrorPayload(payload)) {
      throw new SpookyApiError(
        statusCode,
        payload.error.code,
        apiErrorMessages.get(payload.error.code),
        payload.request_id,
      );
    }
    throw clientError("INVALID_RESPONSE", "Spooky returned an unreadable response. Try again later.");
  }

  function createClient() {
    const isLocalhost = localHostnames.has(window.location.hostname);
    const requestedMock = new URLSearchParams(window.location.search).get("mock");
    const mockScenario = isLocalhost && mockScenarios.has(requestedMock) ? requestedMock : null;
    const assetScript = document.currentScript;
    const glossaryUrl = assetScript
      ? new URL("../glossary/#tool", assetScript.src).href
      : new URL("glossary/#tool", document.baseURI).href;
    let mockAttempt = 0;

    function selectedMockResponse() {
      mockAttempt += 1;
      if (mockScenario === "insufficient") return mockSuccess(glossaryUrl, { withSources: false });
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
      return mockSuccess(glossaryUrl);
    }

    async function ask(message) {
      if (mockScenario !== null) {
        await new Promise((resolve) => window.setTimeout(resolve, 450));
        const mockResponse = selectedMockResponse();
        return parseApiResponse(mockResponse.status, mockResponse.payload);
      }
      if (requestedMock !== null) {
        throw clientError("INVALID_MOCK", "That local mock scenario is not available.");
      }

      let response;
      try {
        response = await fetch(chatEndpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message }),
        });
      } catch (_error) {
        throw clientError(
          "NETWORK_ERROR",
          "The Spooky service could not be reached. Check your connection and try again.",
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

    return { ask };
  }

  function mount(options) {
    const {
      panel,
      form,
      question,
      submitButton,
      status,
      result,
    } = options;
    if (!panel || !form || !question || !submitButton || !status || !result) return null;

    const client = createClient();
    let lastMessage = "";

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
        return url.protocol === "http:" || url.protocol === "https:" ? url.href : null;
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
        element("p", "", readableAnswerText(payload.answer)),
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
        renderSuccess(await client.ask(message));
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

    return { submitQuestion };
  }

  window.SpookyQa = Object.freeze({ mount });
})();
