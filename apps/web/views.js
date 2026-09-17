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
    ${pageHead("工作台总览", "用 Futures 的报告结构观察品种；数据来自 digital-oracle，不是知识库摘录")}
    ${kpiGrid(data.kpis)}
    <div class="split">
      <div class="card">
        <h2>分析模式覆盖</h2>
        <canvas id="sectorChart"></canvas>
      </div>
      <div class="card">
        <h2>报告结构</h2>
        <ol>${(data.template || []).map((item) => `<li>${esc(item.title)}</li>`).join("")}</ol>
        <p class="muted">${esc(data.disclaimer)}</p>
      </div>
    </div>
  `;
  const ctx = document.getElementById("sectorChart");
  if (ctx && window.Chart) {
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: data.sectors.map((item) => item.label),
        datasets: [{ label: "观察品种", data: data.sectors.map((item) => item.product_count), backgroundColor: "#e3920f" }],
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
            <th>名称 / 代码</th><th>分析模式</th><th>交易所</th><th>信号路由</th><th>操作</th>
          </tr>
        </thead>
        <tbody>
          ${(data.rows || []).map((row) => `
            <tr>
              <td><strong>${esc(row.name)}</strong><div class="muted">${esc(row.code)}</div></td>
              <td>${esc(row.sector_label)}</td>
              <td>${esc(row.exchange)}</td>
              <td>${(row.signals || []).map((item) => `<span class="chip">${esc(item)}</span>`).join("")}</td>
              <td class="row-actions">
                <button class="btn ghost" data-go="diagnose" data-code="${esc(row.code)}" data-sector="${esc(row.sector)}">诊断</button>
                <button class="btn ghost" data-go="research" data-code="${esc(row.code)}" data-sector="${esc(row.sector)}">模式</button>
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
  const current = state.diagnose.sector;
  const mode = (data.sectors || []).find((item) => item.id === current) || data.sectors[0];
  const products = await getJson("/api/products?sector=" + encodeURIComponent(mode.id));
  $("page").innerHTML = `
    ${pageHead("分析模式", "Futures 透镜：问什么、看什么窗口；不粘贴该仓库文档")}
    <div class="tabs">
      ${data.sectors.map((item) => `<button data-sector="${esc(item.id)}" class="${item.id === mode.id ? "active" : ""}">${esc(item.label)}</button>`).join("")}
    </div>
    <div class="split">
      <div class="card">
        ${(products.products || []).map((item) => `
          <div class="news-item">
            <strong>${esc(item.code)}</strong> ${esc(item.name)}
            <div class="muted">${esc(item.exchange)}</div>
          </div>`).join("")}
      </div>
      <div class="card">
        <h2>${esc(mode.title)}</h2>
        <p>${esc(mode.summary)}</p>
        <h2>分析焦点</h2>
        <ul>${(mode.questions || []).map((item) => `<li>${esc(item)}</li>`).join("")}</ul>
        <h2>时间窗口</h2>
        <ul>${(mode.calendars || []).map((item) => `<li>${esc(item)}</li>`).join("")}</ul>
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
    ${pageHead("报告模板", "固定六段结构，对应 Futures 的合约分析模式")}
    <div class="news">
      ${(data.template || []).map((item, index) => `
        <div class="card news-item">
          <div class="muted">第 ${index + 1} 段</div>
          <h3>${esc(item.title)}</h3>
        </div>`).join("")}
    </div>
  `;
};
