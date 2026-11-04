const app = document.querySelector("#app");
const scenarioSource = app.dataset.scenarioSource;
const storageKey = "phishguard-progress-v1";

const lessons = [
  ["Email Phishing", "Deceptive emails designed to make people click, open files, or reveal information.", "Check the sender, tone, request, links, and attachments before acting.", ["Unexpected requests", "Urgent language", "Suspicious sender", "Strange domain", "Unusual attachment"], "Do not click immediately. Verify through an independent channel."],
  ["Spear Phishing", "Targeted phishing that uses personal or workplace context.", "These messages feel specific because attackers research the victim.", ["Relevant names", "Workplace context", "Subtle pressure", "Payment or document request"], "Confirm requests through a known phone number or official workflow."],
  ["Smishing", "Phishing delivered through SMS or chat messages.", "Short mobile messages often hide suspicious links and create urgency.", ["Shortened links", "Delivery fees", "Unexpected alerts", "Unusual sender"], "Use the official app or website instead of message links."],
  ["Vishing", "Voice phishing that manipulates victims over calls.", "Attackers may impersonate support, banks, executives, or government offices.", ["Pressure to stay on call", "Requests for codes", "Threats", "Caller ID spoofing"], "Hang up and call the organization using a verified number."],
  ["Credential Phishing", "Attempts to steal usernames, passwords, MFA codes, or recovery details.", "A fake login page may look convincing but sends secrets to an attacker.", ["Fake login pages", "Password requests", "OTP requests", "Look-alike domains"], "Navigate independently to the service and never share MFA codes."],
  ["Social Engineering", "Manipulation that exploits trust, fear, curiosity, or helpfulness.", "The technique matters more than the channel.", ["Authority impersonation", "Emotional bait", "Too-good offers", "Secrecy"], "Pause, verify identity, and follow normal procedures."],
  ["Malicious Attachments", "Files that may contain malware, scripts, or credential prompts.", "Risky files often arrive with pressure or unexpected business context.", ["ZIP files", "Macro documents", "Unexpected invoices", "Download instructions"], "Do not open unexpected files. Report and verify with the sender."],
  ["Fake Websites", "Imitation sites built to steal credentials or payment details.", "The page may mimic branding while the domain tells the truth.", ["Typosquatting", "Odd certificate errors", "Link mismatch", "Unusual forms"], "Check the domain carefully and use trusted bookmarks."],
  ["Business Email Compromise", "Impersonation of executives, vendors, or internal teams to redirect money or data.", "These attacks often ask people to bypass checks.", ["Payment changes", "MFA code requests", "Urgent executive tone", "Procedure bypass"], "Verify using approved finance or IT workflows."]
];

let scenarios = [];
let state = {
  route: location.pathname,
  menuOpen: false,
  activeScenario: 0,
  feedback: null,
  challenge: null,
  progress: loadProgress()
};

function loadProgress() {
  try {
    return { completed: {}, challengeHistory: [], trainingProgress: [], ...(JSON.parse(localStorage.getItem(storageKey)) || {}) };
  } catch {
    return { completed: {}, challengeHistory: [], trainingProgress: [] };
  }
}

function saveProgress() {
  localStorage.setItem(storageKey, JSON.stringify(state.progress));
}

function navigate(path) {
  history.pushState(null, "", path);
  state.route = path;
  state.menuOpen = false;
  state.feedback = null;
  render();
}

function escapeText(value) {
  const span = document.createElement("span");
  span.textContent = value ?? "";
  return span.innerHTML;
}

function difficultyPoints(difficulty) {
  return difficulty === "hard" ? 200 : difficulty === "medium" ? 150 : 100;
}

function stats(records = Object.values(state.progress.completed)) {
  const total = records.length;
  const correct = records.filter((item) => item.correct).length;
  const incorrect = total - correct;
  const score = records.reduce((sum, item) => sum + item.points, 0);
  const phishing = records.filter((item) => item.answer === true).length;
  const legitimate = records.filter((item) => item.answer === false).length;
  const accuracy = total ? Math.round((correct / total) * 100) : 0;
  const categories = [...new Set(records.map((item) => item.category))];
  return { total, correct, incorrect, score, phishing, legitimate, accuracy, categories };
}

function recordAnswer(scenario, answer, challengeMode = false) {
  const correct = answer === scenario.isPhishing;
  const points = correct ? difficultyPoints(scenario.difficulty) : 0;
  const record = { id: scenario.id, title: scenario.title, answer, correct, points, category: scenario.category, indicators: scenario.indicators, at: new Date().toISOString() };
  if (!challengeMode) {
    state.progress.completed[scenario.id] = record;
    saveProgress();
  }
  return record;
}

function layout(content) {
  const navItems = [["/dashboard", "Dashboard"], ["/training", "Training"], ["/simulation", "Simulation"], ["/challenge", "Challenge"], ["/results", "Results"], ["/about", "About"]];
  app.innerHTML = `
    <div class="shell">
      <aside class="sidebar ${state.menuOpen ? "open" : ""}">
        <a href="/dashboard" class="brand" data-link><span class="brand-mark">PG</span><span><strong>PhishGuard</strong><small>Cybersecurity Awareness Training</small></span></a>
        <nav aria-label="Primary">${navItems.map(([path, label]) => `<a href="${path}" data-link class="${state.route.startsWith(path) ? "active" : ""}">${label}</a>`).join("")}</nav>
        <p class="disclaimer">Educational Simulation. No real credentials are collected.</p>
      </aside>
      <div class="main">
        <header class="topbar">
          <button class="menu" type="button" data-action="menu" aria-label="Toggle navigation">☰</button>
          <div><strong>PhishGuard</strong><span>All links and login forms stay inside this training app.</span></div>
        </header>
        <main>${content}</main>
      </div>
    </div>`;
}

function progressBar(value) {
  return `<div class="progress" aria-label="Progress ${value}%"><span style="width:${Math.max(0, Math.min(100, value))}%"></span></div>`;
}

function statCard(label, value, note = "") {
  return `<section class="stat"><span>${label}</span><strong>${value}</strong><small>${note}</small></section>`;
}

function dashboard() {
  const s = stats();
  const recent = Object.values(state.progress.completed).sort((a, b) => b.at.localeCompare(a.at)).slice(0, 5);
  const completion = Math.round((s.total / scenarios.length) * 100);
  layout(`
    <section class="page-head"><p>Security Awareness Dashboard</p><h1>Training readiness overview</h1></section>
    <div class="stats">${statCard("Score", s.score, "difficulty based")}${statCard("Accuracy", `${s.accuracy}%`, `${s.correct} correct`)}${statCard("Solved", s.total, `${s.incorrect} missed`)}${statCard("Identified", `${s.phishing}/${s.legitimate}`, "phishing / legitimate")}</div>
    <section class="panel">
      <div class="panel-title"><h2>Training Progress</h2><strong>${completion}%</strong></div>${progressBar(completion)}
      <div class="chips">${(s.categories.length ? s.categories : ["No categories completed yet"]).map((c) => `<span>${escapeText(c)}</span>`).join("")}</div>
    </section>
    <section class="panel">
      <div class="panel-title"><h2>Recent Performance</h2><button data-nav="/challenge">Start Challenge</button></div>
      ${recent.length ? `<div class="table">${recent.map((r) => `<div><span>${escapeText(r.title)}</span><b class="${r.correct ? "good" : "bad"}">${r.correct ? "Correct" : "Review"}</b><small>${escapeText(r.category)}</small></div>`).join("")}</div>` : `<p class="muted">Complete a scenario to populate recent performance.</p>`}
    </section>`);
}

function training() {
  layout(`
    <section class="page-head"><p>Training</p><h1>Core phishing techniques</h1></section>
    <div class="lesson-grid">${lessons.map((lesson) => `
      <article class="lesson">
        <h2>${lesson[0]}</h2><p>${lesson[1]}</p><p>${lesson[2]}</p>
        <h3>Common signs</h3><ul>${lesson[3].map((i) => `<li>${i}</li>`).join("")}</ul>
        <h3>Recommended response</h3><p>${lesson[4]}</p>
      </article>`).join("")}</div>`);
}

function scenarioViewer(scenario, mode = "practice") {
  const feedback = state.feedback;
  return `
    <article class="scenario">
      <div class="message-head">
        <span>${escapeText(scenario.type)}</span><span>${escapeText(scenario.category)}</span><span>${escapeText(scenario.difficulty)}</span>
      </div>
      <div class="message">
        <div><b>From:</b> ${escapeText(scenario.sender)}</div>
        <div><b>To:</b> ${escapeText(scenario.recipient)}</div>
        <div><b>Subject:</b> ${escapeText(scenario.subject)}</div>
        <p>${escapeText(scenario.message)}</p>
        ${scenario.attachment ? `<p class="attachment">Attachment: ${escapeText(scenario.attachment)}</p>` : ""}
        <button class="link-button" data-link-warning="${scenario.id}" type="button">${escapeText(scenario.linkText)}<small>${escapeText(scenario.simulatedUrl)}</small></button>
      </div>
      <section class="decision" aria-labelledby="decision-title">
        <h2 id="decision-title">Is this message phishing?</h2>
        <button ${feedback ? "disabled" : ""} data-answer="true" data-mode="${mode}" class="danger">🔴 Phishing</button>
        <button ${feedback ? "disabled" : ""} data-answer="false" data-mode="${mode}" class="success">🟢 Legitimate</button>
      </section>
      ${feedback ? resultFeedback(scenario, feedback, mode) : ""}
    </article>`;
}

function resultFeedback(scenario, feedback, mode) {
  return `<section class="feedback ${feedback.correct ? "correct" : "incorrect"}">
    <h2>${feedback.correct ? "Correct decision" : "Review this one"}</h2>
    <p><b>Correct classification:</b> ${scenario.isPhishing ? "Phishing" : "Legitimate"}</p>
    <p>${escapeText(scenario.explanation)}</p>
    <h3>Indicators</h3><ul class="indicator-list">${scenario.indicators.map((i) => `<li>${escapeText(i)}</li>`).join("")}</ul>
    <h3>Safe action</h3><p>${escapeText(scenario.recommendedAction)}</p>
    <button data-action="${mode === "challenge" ? "challenge-next" : "next-scenario"}">${mode === "challenge" ? "Continue Challenge" : "Continue"}</button>
  </section>`;
}

function simulation() {
  const scenario = scenarios[state.activeScenario % scenarios.length];
  layout(`
    <section class="page-head"><p>Simulation</p><h1>${escapeText(scenario.title)}</h1></section>
    <div class="panel-title"><span>Scenario ${state.activeScenario + 1} / ${scenarios.length}</span><span>${Object.keys(state.progress.completed).length} completed</span></div>
    ${scenarioViewer(scenario, "practice")}`);
}

function shuffle(items) {
  return [...items].sort(() => Math.random() - 0.5);
}

function startChallenge() {
  const phishing = shuffle(scenarios.filter((s) => s.isPhishing)).slice(0, 5);
  const legitimate = shuffle(scenarios.filter((s) => !s.isPhishing)).slice(0, 5);
  state.challenge = { ids: shuffle([...phishing, ...legitimate]).map((s) => s.id), index: 0, records: [], finished: false };
  state.feedback = null;
}

function challenge() {
  if (!state.challenge || state.challenge.finished) startChallenge();
  const ch = state.challenge;
  const scenario = scenarios.find((item) => item.id === ch.ids[ch.index]);
  const chStats = stats(ch.records);
  const percent = Math.round((ch.index / ch.ids.length) * 100);
  layout(`
    <section class="page-head"><p>Challenge Mode</p><h1>Scenario ${ch.index + 1} / ${ch.ids.length}</h1></section>
    <section class="panel compact"><div class="panel-title"><span>Score: ${chStats.score}</span><span>Accuracy: ${chStats.accuracy}%</span></div>${progressBar(percent)}</section>
    ${scenarioViewer(scenario, "challenge")}`);
}

function results(records = null) {
  const source = records || Object.values(state.progress.completed);
  const s = stats(source);
  const grade = s.accuracy >= 90 ? "Excellent" : s.accuracy >= 75 ? "Good" : s.accuracy >= 50 ? "Needs Improvement" : "Additional Training Recommended";
  const mistakes = source.filter((r) => !r.correct);
  const missedCategories = [...new Set(mistakes.map((r) => r.category))];
  const missedIndicators = [...new Set(mistakes.flatMap((r) => r.indicators || []))].slice(0, 8);
  layout(`
    <section class="page-head"><p>Results</p><h1>${grade}</h1></section>
    <div class="stats">${statCard("Final Score", s.score)}${statCard("Accuracy", `${s.accuracy}%`)}${statCard("Correct", s.correct)}${statCard("Incorrect", s.incorrect)}</div>
    <section class="panel"><h2>Review Focus</h2>
      <p><b>Total scenarios:</b> ${s.total}</p>
      <p><b>Categories where mistakes occurred:</b> ${missedCategories.length ? missedCategories.map(escapeText).join(", ") : "None recorded"}</p>
      <p><b>Common indicators missed:</b> ${missedIndicators.length ? missedIndicators.map(escapeText).join(", ") : "None recorded"}</p>
      <p><b>Key lessons:</b> slow down when a message creates pressure, inspect domains carefully, and use independent verification for sensitive requests.</p>
      <p><b>Recommendations:</b> review Credential Phishing, Smishing, and Business Email Compromise lessons before the next challenge.</p>
      <div class="actions"><button data-action="retry">Try Again</button><button data-nav="/dashboard">Return to Dashboard</button></div>
    </section>`);
}

function linkWarning(id) {
  const scenario = scenarios.find((item) => item.id === id);
  if (!scenario) return layout(`<section class="panel"><h1>Scenario not found</h1><button data-nav="/simulation">Back to Scenario</button></section>`);
  layout(`<section class="warning-page">
    <p class="simulation-label">⚠ SIMULATED PHISHING LINK</p>
    <h1>This link stayed inside PhishGuard.</h1>
    <p>This was part of the training simulation. The app never navigates to <b>${escapeText(scenario.simulatedUrl)}</b>.</p>
    <h2>Why it was suspicious</h2><ul>${scenario.indicators.map((i) => `<li>${escapeText(i)}</li>`).join("")}</ul>
    <h2>Safe action</h2><p>${escapeText(scenario.recommendedAction)}</p>
    ${scenario.isPhishing ? `<button data-nav="/simulation/login/${scenario.id}">View Safe Login Simulation</button>` : ""}
    <button data-nav="/simulation">Back to Scenario</button>
  </section>`);
}

function loginSimulation(id) {
  const scenario = scenarios.find((item) => item.id === id) || scenarios[0];
  layout(`<section class="login-sim">
    <form data-safe-login>
      <strong>${escapeText(scenario.title)}</strong>
      <p>SIMULATION ONLY. Dummy fields are never submitted, stored, logged, or sent.</p>
      <label>Username<input value="training-user" autocomplete="off"></label>
      <label>Password<input value="example-password" type="text" autocomplete="off"></label>
      <button type="submit">Sign In</button>
      <output id="login-warning"></output>
    </form>
  </section>`);
}

function about() {
  layout(`<section class="page-head"><p>About / Safety</p><h1>Educational phishing-awareness simulator</h1></section>
    <section class="panel">
      <p>This platform is designed for cybersecurity awareness training. All organizations, identities, domains, messages, and login forms are fictional and contained within the application.</p>
      <div class="safety-grid">
        ${["Does not collect credentials", "Does not send phishing emails", "Does not contact external users", "Does not redirect to malicious websites", "Does not execute malicious code", "Does not track users for phishing purposes"].map((item) => `<span>${item}</span>`).join("")}
      </div>
      <p class="disclaimer strong">This application is an educational phishing-awareness simulator. All scenarios are fictional and contained within the application.</p>
    </section>`);
}

function render() {
  const path = state.route === "/" ? "/dashboard" : state.route;
  if (path.startsWith("/training")) training();
  else if (path.startsWith("/simulation/link-warning/")) linkWarning(path.split("/").pop());
  else if (path.startsWith("/simulation/login/")) loginSimulation(path.split("/").pop());
  else if (path.startsWith("/simulation")) simulation();
  else if (path.startsWith("/challenge")) challenge();
  else if (path.startsWith("/results")) results();
  else if (path.startsWith("/about")) about();
  else dashboard();
}

document.addEventListener("click", (event) => {
  const link = event.target.closest("[data-link]");
  const nav = event.target.closest("[data-nav]");
  const menu = event.target.closest("[data-action='menu']");
  const warning = event.target.closest("[data-link-warning]");
  const answer = event.target.closest("[data-answer]");
  const action = event.target.closest("[data-action]");
  if (link) { event.preventDefault(); navigate(link.getAttribute("href")); }
  if (nav) navigate(nav.dataset.nav);
  if (menu) { state.menuOpen = !state.menuOpen; render(); }
  if (warning) navigate(`/simulation/link-warning/${warning.dataset.linkWarning}`);
  if (answer) {
    const isChallenge = answer.dataset.mode === "challenge";
    const scenario = isChallenge ? scenarios.find((item) => item.id === state.challenge.ids[state.challenge.index]) : scenarios[state.activeScenario % scenarios.length];
    const record = recordAnswer(scenario, answer.dataset.answer === "true", isChallenge);
    if (isChallenge) state.challenge.records.push(record);
    state.feedback = record;
    render();
  }
  if (action?.dataset.action === "next-scenario") {
    state.activeScenario = (state.activeScenario + 1) % scenarios.length;
    state.feedback = null;
    render();
  }
  if (action?.dataset.action === "challenge-next") {
    state.feedback = null;
    state.challenge.index += 1;
    if (state.challenge.index >= state.challenge.ids.length) {
      state.challenge.finished = true;
      state.progress.challengeHistory.unshift({ at: new Date().toISOString(), records: state.challenge.records });
      state.progress.challengeHistory = state.progress.challengeHistory.slice(0, 5);
      saveProgress();
      results(state.challenge.records);
    } else render();
  }
  if (action?.dataset.action === "retry") {
    startChallenge();
    navigate("/challenge");
  }
});

document.addEventListener("submit", (event) => {
  if (event.target.matches("[data-safe-login]")) {
    event.preventDefault();
    document.querySelector("#login-warning").textContent = "Stop! In a real attack, entering credentials here could expose your account. Always verify the domain before signing in.";
    event.target.reset();
  }
});

window.addEventListener("popstate", () => {
  state.route = location.pathname;
  render();
});

fetch(scenarioSource)
  .then((response) => response.json())
  .then((data) => {
    scenarios = data;
    render();
  })
  .catch(() => {
    app.innerHTML = "<main class='noscript'><h1>Could not load scenario data</h1><p>Check public/data/scenarios.json.</p></main>";
  });
