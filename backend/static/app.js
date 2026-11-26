"use strict";

/* ---------- Translations (Kannada default, English toggle) ---------- */
const T = {
  kn: {
    appTitle: "ಆದಾಯ ಪ್ರಮಾಣಪತ್ರ ಅರ್ಜಿಗಳು",
    appSub: "ಅಧಿಕಾರಿಗಳಿಗಾಗಿ",
    login: "ಲಾಗಿನ್",
    username: "ಬಳಕೆದಾರ ಹೆಸರು",
    password: "ಪಾಸ್‌ವರ್ಡ್",
    signIn: "ಒಳಗೆ ಹೋಗಿ",
    signOut: "ಲಾಗ್ ಔಟ್",
    wrongLogin: "ಬಳಕೆದಾರ ಹೆಸರು ಅಥವಾ ಪಾಸ್‌ವರ್ಡ್ ತಪ್ಪಾಗಿದೆ",
    demoHint: "ಡೆಮೊ ಬಳಕೆದಾರರು (ಪಾಸ್‌ವರ್ಡ್: demo123)",
    queueTitle: "ನಿಮ್ಮ ಬಾಕಿ ಅರ್ಜಿಗಳು",
    pending: "ಬಾಕಿ",
    urgent: "ತುರ್ತು",
    noPending: "ಯಾವುದೇ ಬಾಕಿ ಅರ್ಜಿಗಳಿಲ್ಲ",
    waiting: (n) => `ಈ ಹಂತದಲ್ಲಿ ${n} ದಿನ`,
    totalDays: (n) => `ಒಟ್ಟು ${n} ದಿನ`,
    back: "← ಹಿಂದೆ",
    village: "ಗ್ರಾಮ",
    income: "ಘೋಷಿತ ವಾರ್ಷಿಕ ಆದಾಯ",
    occupation: "ವೃತ್ತಿ",
    family: "ಕುಟುಂಬದ ಸದಸ್ಯರು",
    status: "ಈಗಿನ ಹಂತ",
    documents: "ದಾಖಲೆಗಳು",
    missing: "ಇಲ್ಲ",
    history: "ಇತಿಹಾಸ",
    noHistory: "ಇನ್ನೂ ಯಾವುದೇ ಕ್ರಮ ಆಗಿಲ್ಲ",
    decision: "ನಿಮ್ಮ ತೀರ್ಮಾನ",
    noActions: "ಈ ಹಂತದಲ್ಲಿ ನಿಮಗೆ ಯಾವುದೇ ಕ್ರಮ ಇಲ್ಲ",
    reason: "ಕಾರಣ / ಟಿಪ್ಪಣಿ",
    reasonRequired: "ಹಿಂದಕ್ಕೆ ಕಳುಹಿಸಲು ಅಥವಾ ತಿರಸ್ಕರಿಸಲು ಕಾರಣ ಬರೆಯಿರಿ",
    done: "ಕ್ರಮ ದಾಖಲಾಗಿದೆ",
    aiTitle: "AI ಸಹಾಯ",
    aiDisclaimer: "ಇದು ಕೇವಲ ಸಲಹೆ. ಅಂತಿಮ ತೀರ್ಮಾನ ನಿಮ್ಮದು.",
    aiButton: "AI ಸಲಹೆ ಪಡೆಯಿರಿ",
    aiLoading: "ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ…",
    aiFlags: "ಗಮನಿಸಿ",
    aiNone: "ಯಾವುದೇ ಸಮಸ್ಯೆ ಕಂಡುಬಂದಿಲ್ಲ",
    aiError: "AI ಸಲಹೆ ಈಗ ಲಭ್ಯವಿಲ್ಲ",
    aiUseReason: "ಕಾರಣವಾಗಿ ಬಳಸಿ",
    errorGeneric: "ಏನೋ ತಪ್ಪಾಗಿದೆ",
    statusNames: {
      submitted: "ಹೊಸ ಅರ್ಜಿ",
      field_verification: "ಸ್ಥಳ ಪರಿಶೀಲನೆ",
      ri_review: "ಕಂದಾಯ ನಿರೀಕ್ಷಕರ ಪರಿಶೀಲನೆ",
      final_decision: "ಅಂತಿಮ ತೀರ್ಮಾನ",
      approved: "ಅನುಮೋದಿತ",
      rejected: "ತಿರಸ್ಕೃತ",
    },
    actionNames: {
      forward: "ಮುಂದಕ್ಕೆ ಕಳುಹಿಸಿ",
      return: "ಹಿಂದಕ್ಕೆ ಕಳುಹಿಸಿ",
      reject: "ತಿರಸ್ಕರಿಸಿ",
      approve: "ಅನುಮೋದಿಸಿ",
    },
    actionPast: {
      forward: "ಮುಂದಕ್ಕೆ ಕಳುಹಿಸಲಾಗಿದೆ",
      return: "ಹಿಂದಕ್ಕೆ ಕಳುಹಿಸಲಾಗಿದೆ",
      reject: "ತಿರಸ್ಕರಿಸಲಾಗಿದೆ",
      approve: "ಅನುಮೋದಿಸಲಾಗಿದೆ",
    },
    roleNames: {
      village_accountant: "ಗ್ರಾಮ ಲೆಕ್ಕಾಧಿಕಾರಿ",
      revenue_inspector: "ಕಂದಾಯ ನಿರೀಕ್ಷಕ",
      tahsildar: "ತಹಶೀಲ್ದಾರ್",
    },
  },
  en: {
    appTitle: "Income Certificate Applications",
    appSub: "For officers",
    login: "Login",
    username: "Username",
    password: "Password",
    signIn: "Sign in",
    signOut: "Sign out",
    wrongLogin: "Wrong username or password",
    demoHint: "Demo users (password: demo123)",
    queueTitle: "Your pending applications",
    pending: "Pending",
    urgent: "Urgent",
    noPending: "No pending applications",
    waiting: (n) => `${n} days at this step`,
    totalDays: (n) => `${n} days in total`,
    back: "← Back",
    village: "Village",
    income: "Declared annual income",
    occupation: "Occupation",
    family: "Family members",
    status: "Current step",
    documents: "Documents",
    missing: "missing",
    history: "History",
    noHistory: "No action taken yet",
    decision: "Your decision",
    noActions: "You have no action at this step",
    reason: "Reason / note",
    reasonRequired: "Please write a reason to return or reject",
    done: "Action recorded",
    aiTitle: "AI assistance",
    aiDisclaimer: "This is only a suggestion. The final decision is yours.",
    aiButton: "Get AI suggestion",
    aiLoading: "Checking…",
    aiFlags: "Please note",
    aiNone: "No issues found",
    aiError: "AI suggestion is not available right now",
    aiUseReason: "Use as reason",
    errorGeneric: "Something went wrong",
    statusNames: {
      submitted: "New application",
      field_verification: "Field verification",
      ri_review: "Revenue Inspector review",
      final_decision: "Final decision",
      approved: "Approved",
      rejected: "Rejected",
    },
    actionNames: {
      forward: "Forward",
      return: "Return",
      reject: "Reject",
      approve: "Approve",
    },
    actionPast: {
      forward: "Forwarded",
      return: "Returned",
      reject: "Rejected",
      approve: "Approved",
    },
    roleNames: {
      village_accountant: "Village Accountant",
      revenue_inspector: "Revenue Inspector",
      tahsildar: "Tahsildar",
    },
  },
};

const NEEDS_REASON = ["return", "reject"];
const DEMO_USERS = ["suresh", "meena", "rao"];
const URGENT_DAYS = 5; // days at the current step before a case is marked urgent
let aiSuggestion = ""; // the last AI draft reason shown, used to record how it was used

/* ---------- Small helpers ---------- */
let lang = safeGet("lang") || "kn";
const t = (key) => T[lang][key];
const $ = (sel) => document.querySelector(sel);

function safeGet(key) {
  try { return localStorage.getItem(key); } catch { return null; }
}
function safeSet(key, value) {
  try { localStorage.setItem(key, value); } catch { /* storage unavailable */ }
}
function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
function daysSince(iso) {
  return Math.max(0, Math.floor((Date.now() - new Date(iso).getTime()) / 86400000));
}
function formatDate(iso) {
  return new Date(iso).toLocaleString(lang === "kn" ? "kn-IN" : "en-IN", {
    day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit",
  });
}
function formatIncome(n) {
  return "₹" + Number(n).toLocaleString("en-IN");
}
let toastTimer;
function toast(message) {
  const el = $("#toast");
  el.textContent = message;
  el.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.remove("show"), 2800);
}

/* ---------- Session + API ---------- */
const session = {
  get token() { return sessionStorage.getItem("token"); },
  get name() { return sessionStorage.getItem("name"); },
  get role() { return sessionStorage.getItem("role"); },
  save(data) {
    sessionStorage.setItem("token", data.token);
    sessionStorage.setItem("name", data.name);
    sessionStorage.setItem("role", data.role);
  },
  clear() { sessionStorage.clear(); },
};

async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json" };
  if (session.token) headers.Authorization = "Bearer " + session.token;
  const res = await fetch(path, { ...options, headers });
  if (res.status === 401 && session.token) {
    logout();
    throw new Error("401");
  }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(typeof data.detail === "string" ? data.detail : t("errorGeneric"));
  return data;
}

function logout() {
  session.clear();
  location.hash = "#/";
  route();
}

/* ---------- Top bar ---------- */
function renderTopbar() {
  const bar = $("#topbar");
  bar.hidden = !session.token;
  $("#brand-title").textContent = t("appTitle");
  $("#brand-sub").textContent = t("appSub");
  $("#who-text").textContent = session.token
    ? `${session.name} · ${t("roleNames")[session.role] || ""}`
    : "";
  $("#lang-btn").textContent = lang === "kn" ? "English" : "ಕನ್ನಡ";
  $("#logout-btn").textContent = t("signOut");
  document.documentElement.lang = lang;
  document.title = t("appTitle");
}

/* ---------- Views ---------- */
function viewLogin() {
  $("#app").innerHTML = `
    <section class="panel login-card">
      <h1>${esc(t("appTitle"))}</h1>
      <p class="hint">${esc(t("appSub"))}</p>
      <form id="login-form">
        <label for="u">${esc(t("username"))}</label>
        <input id="u" autocomplete="username" required>
        <label for="p">${esc(t("password"))}</label>
        <input id="p" type="password" autocomplete="current-password" required>
        <p class="error" id="login-error" role="alert"></p>
        <button class="primary" type="submit" style="width:100%">${esc(t("signIn"))}</button>
      </form>
      <p class="hint" style="margin-top:16px">${esc(t("demoHint"))}:
        ${DEMO_USERS.map((u) => `<code>${u}</code>`).join(", ")}</p>
      <p style="text-align:right;margin:0">
        <button id="login-lang" class="chip" type="button">${lang === "kn" ? "English" : "ಕನ್ನಡ"}</button>
      </p>
    </section>`;

  $("#login-lang").onclick = toggleLang;
  $("#login-form").onsubmit = async (event) => {
    event.preventDefault();
    const button = event.target.querySelector("button[type=submit]");
    button.disabled = true;
    try {
      const data = await api("/login", {
        method: "POST",
        body: JSON.stringify({ username: $("#u").value.trim(), password: $("#p").value }),
      });
      session.save(data);
      location.hash = "#/";
      route();
    } catch {
      $("#login-error").textContent = t("wrongLogin");
      button.disabled = false;
    }
  };
}

async function viewQueue() {
  $("#app").innerHTML = `<p class="hint">…</p>`;
  const apps = await api(`/applications?lang=${lang}`);
  const urgentCount = apps.filter((a) => daysSince(a.stage_entered_at) >= URGENT_DAYS).length;

  const cards = apps.map((a) => {
    const days = daysSince(a.stage_entered_at);
    const level = days >= URGENT_DAYS ? "high" : days >= 3 ? "mid" : "low";
    const chips = (a.flags || []).map((f) => `<span class="flag-chip">⚠ ${esc(f)}</span>`).join("");
    return `
      <a class="card ${level}" href="#/case/${a.id}">
        <div class="row">
          <span class="name">${esc(a.applicant_name)}</span>
          <span class="badge ${level}">${esc(t("waiting")(days))}</span>
        </div>
        <div class="row meta">
          <span>${esc(a.village)} · ${esc(a.occupation)}</span>
          <span class="badge">${esc(t("statusNames")[a.status] || a.status)}</span>
        </div>
        <div class="meta">${esc(t("totalDays")(daysSince(a.created_at)))}</div>
        ${chips ? `<div class="chips">${chips}</div>` : ""}
      </a>`;
  }).join("");

  $("#app").innerHTML = `
    <h1>${esc(t("queueTitle"))}</h1>
    <div class="summary">
      <div class="stat"><b>${apps.length}</b>${esc(t("pending"))}</div>
      <div class="stat urgent"><b>${urgentCount}</b>${esc(t("urgent"))}</div>
    </div>
    ${cards || `<p class="panel">${esc(t("noPending"))}</p>`}`;
}

async function viewCase(id) {
  $("#app").innerHTML = `<p class="hint">…</p>`;
  aiSuggestion = "";
  const data = await api(`/applications/${id}?lang=${lang}`);
  const a = data.application;

  const docs = data.documents.map((d) => d.present
    ? `<li class="ok">${esc(d.name)}</li>`
    : `<li class="missing">${esc(d.name)} (${esc(t("missing"))})</li>`).join("");

  const timeline = data.history.length
    ? data.history.map((h) => `
        <li>
          <div class="t-main">${esc(t("actionPast")[h.action] || h.action)} →
            ${esc(t("statusNames")[h.to_state] || h.to_state)}</div>
          <div class="t-meta">${esc(h.actor_name)} (${esc(t("roleNames")[h.role] || h.role)}) · ${esc(formatDate(h.created_at))}</div>
          ${h.reason ? `<div class="t-reason">${esc(h.reason)}</div>` : ""}
        </li>`).join("")
    : `<li class="t-meta">${esc(t("noHistory"))}</li>`;

  const buttons = data.allowed_actions.map((act) => {
    const cls = act === "reject" ? "danger" : act === "return" ? "secondary" : "primary";
    return `<button class="${cls}" data-action="${esc(act)}" type="button">${esc(t("actionNames")[act] || act)}</button>`;
  }).join("");

  const decision = data.allowed_actions.length
    ? `<section class="panel">
         <h2>${esc(t("decision"))}</h2>
         <label for="reason">${esc(t("reason"))}</label>
         <textarea id="reason"></textarea>
         <p class="error" id="action-error" role="alert"></p>
         <div class="actions">${buttons}</div>
       </section>`
    : `<section class="panel"><p class="hint">${esc(t("noActions"))}</p></section>`;

  const aiPanel = data.allowed_actions.length
    ? `<section class="panel ai">
         <h2>${esc(t("aiTitle"))}</h2>
         <p class="disclaimer">${esc(t("aiDisclaimer"))}</p>
         <button id="ai-btn" type="button">${esc(t("aiButton"))}</button>
         <div id="ai-out"></div>
       </section>`
    : "";

  $("#app").innerHTML = `
    <a class="back" href="#/">${esc(t("back"))}</a>
    <h1>${esc(a.applicant_name)}</h1>
    <section class="panel">
      <dl class="facts">
        <dt>${esc(t("status"))}</dt><dd>${esc(t("statusNames")[a.status] || a.status)}</dd>
        <dt>${esc(t("village"))}</dt><dd>${esc(a.village)}</dd>
        <dt>${esc(t("occupation"))}</dt><dd>${esc(a.occupation)}</dd>
        <dt>${esc(t("family"))}</dt><dd>${esc(a.family_members)}</dd>
        <dt>${esc(t("income"))}</dt><dd>${esc(formatIncome(a.declared_income))}</dd>
      </dl>
    </section>
    <section class="panel"><h2>${esc(t("documents"))}</h2><ul class="docs">${docs}</ul></section>
    ${aiPanel}
    ${decision}
    <section class="panel"><h2>${esc(t("history"))}</h2><ol class="timeline">${timeline}</ol></section>`;

  document.querySelectorAll("[data-action]").forEach((btn) => {
    btn.onclick = () => submitAction(id, btn.dataset.action, btn);
  });
  const aiBtn = $("#ai-btn");
  if (aiBtn) aiBtn.onclick = () => runAssist(id, aiBtn);
}

async function submitAction(id, action, button) {
  const reason = $("#reason").value.trim();
  const error = $("#action-error");
  error.textContent = "";
  if (NEEDS_REASON.includes(action) && !reason) {
    error.textContent = t("reasonRequired");
    $("#reason").focus();
    return;
  }
  document.querySelectorAll("[data-action]").forEach((b) => (b.disabled = true));
  // none = AI draft not used, used = used as written, edited = used then changed
  const aiUse = !aiSuggestion ? "none" : reason === aiSuggestion ? "used" : reason ? "edited" : "none";
  try {
    await api(`/applications/${id}/action`, {
      method: "POST",
      body: JSON.stringify({ action, reason, ai_reason_use: aiUse }),
    });
    toast(t("done"));
    location.hash = "#/";
  } catch (err) {
    error.textContent = err.message;
    document.querySelectorAll("[data-action]").forEach((b) => (b.disabled = false));
  }
}

async function runAssist(id, button) {
  const out = $("#ai-out");
  button.disabled = true;
  out.innerHTML = `<p class="hint">${esc(t("aiLoading"))}</p>`;
  try {
    const r = await api(`/applications/${id}/assist?lang=${lang}`, { method: "POST" });
    const flags = (r.flags || []).map((f) => `<div class="ai-flag">⚠ ${esc(f)}</div>`).join("");
    out.innerHTML = `
      ${r.summary ? `<div class="ai-summary">${esc(r.summary)}</div>` : ""}
      ${flags || `<p class="hint">${esc(t("aiNone"))}</p>`}
      ${r.suggested_reason ? `<button id="ai-use" class="chip" type="button">${esc(t("aiUseReason"))}</button>` : ""}`;
    const use = $("#ai-use");
    if (use) use.onclick = () => { $("#reason").value = r.suggested_reason; aiSuggestion = r.suggested_reason.trim(); };
  } catch (err) {
    if (err.message !== "401") out.innerHTML = `<p class="error">${esc(t("aiError"))}</p>`;
  } finally {
    button.disabled = false;
  }
}

/* ---------- Router ---------- */
async function route() {
  renderTopbar();
  if (!session.token) return viewLogin();
  const match = location.hash.match(/^#\/case\/(\d+)$/);
  try {
    if (match) await viewCase(Number(match[1]));
    else await viewQueue();
  } catch (err) {
    if (err.message !== "401") {
      $("#app").innerHTML = `<p class="panel error">${esc(err.message)}</p>`;
    }
  }
}

function toggleLang() {
  lang = lang === "kn" ? "en" : "kn";
  safeSet("lang", lang);
  route();
}

$("#lang-btn").onclick = toggleLang;
$("#logout-btn").onclick = logout;
window.addEventListener("hashchange", route);
route();
