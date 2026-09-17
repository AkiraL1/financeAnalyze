function kpiGrid(kpis) {
  return `<div class="kpis">${(kpis || []).map((item) => `
    <div class="card">
      <div class="muted">${esc(item.label)}</div>
      <div class="kpi-value">${esc(item.value)}</div>
      <div class="muted">${esc(item.sub)}</div>
    </div>`).join("")}</div>`;
}

function pageHead(title, sub, extra = "") {
  return `<div class="page-head">
    <div><h1>${esc(title)}</h1><div class="muted">${esc(sub)}</div></div>
    <div>${extra}</div>
  </div>`;
}

views.overview = async function overview() {
  const data = await ensureOverview();
  $("page").innerHTML = `
    ${pageHead("工作台总览", "Futures 知识模块覆盖 + 默认观察池，不是持仓盈亏")}
    ${kpiGrid(data.kpis)}
    <div class="split">
      <div class="card">
        <h2>模块覆盖</h2>
        <canvas id="sectorChart"></canvas>
      </div>
      <div class="card">
        <h2>研究摘录</h2>
        ${(data.cases || []).slice(0, 3).map((item) => `
          <div class="news-item">
            <h3>${esc(item.title)}</h3>
            <pre class="muted">${esc(item.excerpt)}</pre>
          </div>`).join("") || "<p class='muted'>暂无 cases</p>"}
      </div>
    </div>
  `;
  const ctx = document.getElementById("sectorChart");
  if (ctx && window.Chart) {
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: data.sectors.map((item) => item.label),
        datasets: [{ label: "品种数", data: data.sectors.map((item) => item.product_count), backgroundColor: "#e3920f" }],
      },
      options: { plugins: { legend: { display: false } }, scales: { x: { ticks: { color: "#8b9bb0" } }, y: { ticks: { color: "#8b9bb0" } } } },
    });
  }
};

views.board = async function board() {
  state.board = state.board || await getJson("/api/board");
  const data = state.board;
  $("page").innerHTML = `
    ${pageHead("关注品种", data.disclaimer)}
    ${kpiGrid(data.kpis)}
    <div class="card">
      <table>
        <thead>
          <tr>
            <th>名称 / 代码</th><th>模块</th><th>交易所</th><th>信号路由</th><th>案例</th><th>操作</th>
          </tr>
        </thead>
        <tbody>
          ${(data.rows || []).map((row) => `
            <tr>
              <td><strong>${esc(row.name)}</strong><div class="muted">${esc(row.code)}</div></td>
              <td>${esc(row.sector_label)}</td>
              <td>${esc(row.exchange)}</td>
              <td>${(row.signals || []).map((item) => `<span class="chip">${esc(item)}</span>`).join("")}</td>
              <td>${esc(row.case_count)}</td>
              <td class="row-actions">
                <button class="btn ghost" data-go="diagnose" data-code="${esc(row.code)}" data-sector="${esc(row.sector)}">诊断</button>
                <button class="btn ghost" data-go="research" data-code="${esc(row.code)}" data-sector="${esc(row.sector)}">研究</button>
              </td>
            </tr>`).join("")}
        </tbody>
      </table>
    </div>
  `;
  $("page").querySelectorAll("[data-go]").forEach((btn) => {
    btn.onclick = () => {
      state.diagnose.sector = btn.dataset.sector;
      state.diagnose.code = btn.dataset.code;
      show(btn.dataset.go);
    };
  });
};

views.research = async function research() {
  const data = await ensureOverview();
  const sectors = await getJson("/api/sectors");
  const current = state.diagnose.sector;
  const products = await getJson("/api/products?sector=" + encodeURIComponent(current));
  $("page").innerHTML = `
    ${pageHead("标的研究", "按 Futures 模块阅读品种清单与要点")}
    <div class="tabs">
      ${sectors.sectors.map((item) => `<button data-sector="${esc(item.id)}" class="${item.id === current ? "active" : ""}">${esc(item.id)}</button>`).join("")}
    </div>
    <div class="split">
      <div class="card">
        ${(products.products || []).map((item) => `
          <div class="news-item">
            <strong>${esc(item.code)}</strong> ${esc(item.name)}
            <div class="muted">${esc(item.exchange)} ${esc(item.note)}</div>
          </div>`).join("")}
      </div>
      <div class="card">
        <h2>模块摘录</h2>
        ${(data.sectors.find((item) => item.id === current) || {}).summary
          ? `<p>${esc((data.sectors.find((item) => item.id === current) || {}).summary)}</p>`
          : "<p class='muted'>无摘要</p>"}
      </div>
    </div>
  `;
  $("page").querySelectorAll("[data-sector]").forEach((btn) => {
    btn.onclick = () => {
      state.diagnose.sector = btn.dataset.sector;
      views.research();
    };
  });
};

views.notes = async function notes() {
  const data = await ensureOverview();
  $("page").innerHTML = `
    ${pageHead("研究摘录", "来自 Futures modules/*/cases，原文仍以知识库为准")}
    <div class="news">
      ${(data.cases || []).map((item) => `
        <div class="card news-item">
          <div class="muted">${esc(item.sector)} · ${esc(item.relpath)}</div>
          <h3>${esc(item.title)}</h3>
          <pre class="muted">${esc(item.excerpt)}</pre>
        </div>`).join("") || "<div class='card muted'>尚无案例</div>"}
    </div>
  `;
};
