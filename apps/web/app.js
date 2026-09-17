const state = {
  page: "overview",
  overview: null,
  board: null,
  diagnose: { sector: "metals", code: "GC", data: null, oracle: false },
  intel: { live: false, data: null, kind: "all" },
  review: null,
};

const $ = (id) => document.getElementById(id);

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => (
    { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]
  ));
}

async function getJson(url) {
  const response = await fetch(url);
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "请求失败");
  }
  return data;
}

function renderTape(rows) {
  $("tape").textContent = (rows || []).map((row) =>
    `${row.code} ${row.name} · ${row.exchange}`
  ).join("    |    ") || "关注品种未加载";
}

function renderIndices(sectors) {
  $("indices").innerHTML = (sectors || []).slice(0, 7).map((item) => `
    <div class="idx">
      <div class="muted">${esc(item.label)}</div>
      <b>${esc(item.product_count)}</b>
      <div class="muted">案例 ${esc(item.case_count)}</div>
    </div>
  `).join("");
}

async function ensureOverview() {
  if (!state.overview) {
    state.overview = await getJson("/api/overview");
  }
  $("snapTime").textContent = state.overview.generated_at;
  $("clock").textContent = state.overview.generated_at;
  renderTape(state.overview.tape);
  renderIndices(state.overview.sectors);
  return state.overview;
}

const views = {};

async function show(page) {
  state.page = page;
  document.querySelectorAll("#nav button").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.page === page);
  });
  await ensureOverview();
  const view = views[page];
  $("page").innerHTML = "<p class='muted'>加载中…</p>";
  await view();
}

document.querySelectorAll("#nav button").forEach((btn) => {
  btn.onclick = () => show(btn.dataset.page);
});

$("refreshBtn").onclick = async () => {
  state.overview = null;
  state.board = null;
  state.review = null;
  await show(state.page);
};

window.addEventListener("load", () => show("overview"));
