const form = document.getElementById("topic-form");
const topicInput = document.getElementById("topic");
const charCounter = document.getElementById("counter");
const wordCounter = document.getElementById("word-counter");
const errorEl = document.getElementById("error");
const statusEl = document.getElementById("status");
const previewEl = document.getElementById("preview");
const submitBtn = document.getElementById("submit-btn");

const MAX_CHARS = 120;
const MAX_WORDS = 20;

function getWordCount(text) {
  const clean = text.trim();
  if (!clean) return 0;
  return clean.split(/\s+/).length;
}

function updateCounters() {
  const text = topicInput.value;
  const words = getWordCount(text);
  charCounter.textContent = `${text.length} / ${MAX_CHARS} chars`;
  wordCounter.textContent = `${words} / ${MAX_WORDS} words`;
}

function setError(message) {
  if (!message) {
    errorEl.hidden = true;
    errorEl.textContent = "";
    return;
  }
  errorEl.hidden = false;
  errorEl.textContent = message;
}

async function submitTopic(topic) {
  const response = await fetch("/api/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ topic })
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(payload.detail || "Request failed");
  }

  const markdown = await response.text();
  return markdown;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  setError("");

  const topic = topicInput.value.trim();
  const words = getWordCount(topic);

  if (!topic) {
    setError("Topic is required.");
    return;
  }

  if (topic.length > MAX_CHARS) {
    setError("Topic must be 120 characters or fewer.");
    return;
  }

  if (words > MAX_WORDS) {
    setError("Topic must be 20 words or fewer.");
    return;
  }

  submitBtn.disabled = true;
  statusEl.textContent = "Generating blog...";

  try {
    const markdown = await submitTopic(topic);
    previewEl.innerHTML = marked.parse(markdown);
    statusEl.textContent = "Done.";
  } catch (error) {
    statusEl.textContent = "Failed.";
    previewEl.innerHTML = "";
    setError(error.message || "Something went wrong");
  } finally {
    submitBtn.disabled = false;
  }
});

topicInput.addEventListener("input", updateCounters);
updateCounters();
