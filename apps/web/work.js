views.diagnose = async function diagnose() {
  const sectors = await getJson("/api/sectors");
  const products = await getJson("/api/products?sector=" + encodeURIComponent(state.diagnose.sector));
  if (!products.products.some((item) => item.code === state.diagnose.code) && products.products[0]) {
    state.diagnose.code = products.products[0].code;
  }
  const extra = `
    <label class="muted"><input type="checkbox" id="oracleToggle" ${state.diagnose.oracle ? "checked" : ""}/> 拉取市场信号</label>
    <button class="btn" id="runDiagnose">生成诊断</button>
  `;
  $("page").innerHTML = `
    ${pageHead("品种诊断", "按六段分析模式填写；信号来自 digital-oracle")}
    <div class="card" style="margin-bottom:12px">
      <div class="tabs">
        ${sectors.sectors.map((item) => `<button data-sector="${esc(item.id)}" class="${item.id === state.diagnose.sector ? "active" : ""}">${esc(item.id)}</button>`).join("")}
      </div>
      <select id="codeSelect">${products.products.map((item) =>
        `<option value="${esc(item.code)}" ${item.code === state.diagnose.code ? "selected" : ""}>${esc(item.code)} ${esc(item.name)}</option>`
      ).join("")}</select>
      ${extra}
    </div>
    <div id="diagnoseBody" class="muted">选择品种后生成诊断。</div>
  `;
  $("page").querySelectorAll("[data-sector]").forEach((btn) => {
    btn.onclick = () => {
      state.diagnose.sector = btn.dataset.sector;
      views.diagnose();
    };
  });
  $("codeSelect").onchange = (event) => { state.diagnose.code = event.target.value; };
  $("runDiagnose").onclick = runDiagnose;
  if (state.diagnose.data) {
    renderDiagnose(state.diagnose.data);
  }
};

async function runDiagnose() {
  state.diagnose.oracle = $("oracleToggle").checked;
  state.diagnose.code = $("codeSelect").value;
  const url = `/api/desk/${encodeURIComponent(state.diagnose.code)}?oracle=${state.diagnose.oracle}&sector=${encodeURIComponent(state.diagnose.sector)}`;
  $("diagnoseBody").textContent = "生成中…";
  try {
    state.diagnose.data = await getJson(url);
    renderDiagnose(state.diagnose.data);
  } catch (err) {
    $("diagnoseBody").innerHTML = `<span class="err">${esc(err.message)}</span>`;
  }
}

function renderDiagnose(data) {
  $("diagnoseBody").innerHTML = `
    <div class="split">
      <div class="card">
        <h2>${esc(data.product.code)} ${esc(data.product.name)}</h2>
        <p class="muted">${esc(data.knowledge_disclaimer)}</p>
        ${(data.report || []).map((section) => `
          <h2>${esc(section.title)}</h2>
          <ul>${(section.body || []).map((item) => `<li>${esc(item)}</li>`).join("")}</ul>
        `).join("")}
      </div>
      <div class="card">
        <h2>综合备注</h2>
        <ul>${(data.notes || []).map((item) => `<li>${esc(item)}</li>`).join("")}</ul>
        <h2>Oracle</h2>
        <pre class="muted">${esc(JSON.stringify(data.oracle ? { results: Object.keys(data.oracle.results || {}), errors: data.oracle.errors } : "未拉取", null, 2))}</pre>
      </div>
    </div>
  `;
}

views.intel = async function intel() {
  const kind = state.intel.kind;
  if (!state.intel.data) {
    state.intel.data = await getJson("/api/intel?live=" + state.intel.live);
  }
  const items = (state.intel.data.items || []).filter((item) => kind === "all" || item.kind === kind);
  $("page").innerHTML = `
    ${pageHead("市场资讯", "模式日历 + 可抓取的 digital-oracle 交易数据")}
    <div class="page-head">
      <div class="tabs">
        <button data-kind="all" class="${kind === "all" ? "active" : ""}">全部</button>
        <button data-kind="oracle" class="${kind === "oracle" ? "active" : ""}">市场信号</button>
        <button data-kind="calendar" class="${kind === "calendar" ? "active" : ""}">时间窗口</button>
        <button data-kind="focus" class="${kind === "focus" ? "active" : ""}">分析焦点</button>
      </div>
      <button class="btn" id="fetchIntel">抓取</button>
    </div>
    <div class="muted">条目 ${esc(state.intel.data.count)} · live=${esc(state.intel.live)}</div>
    <div class="news">
      ${items.map((item) => `
        <div class="card news-item">
          <div class="muted">${esc(item.source)} · ${esc(item.related)}</div>
          <h3>${esc(item.title)}</h3>
          <div>${esc(stripMd(item.body))}</div>
        </div>`).join("")}
    </div>
  `;
  $("page").querySelectorAll("[data-kind]").forEach((btn) => {
    btn.onclick = () => {
      state.intel.kind = btn.dataset.kind;
      views.intel();
    };
  });
  $("fetchIntel").onclick = async () => {
    state.intel.live = true;
    state.intel.data = null;
    await views.intel();
  };
};

views.review = async function review() {
  if (!state.review) {
    state.review = await getJson("/api/review");
  }
  const data = state.review;
  $("page").innerHTML = `
    ${pageHead("每日简报", data.disclaimer, `
      <button class="btn ghost" id="copyMd">复制 Markdown</button>
      <button class="btn" id="dlMd">下载 .md</button>
    `)}
    ${kpiGrid(data.kpis)}
    <div class="split">
      <div class="card"><h2>模块品种数</h2><canvas id="attrChart"></canvas></div>
      <div class="card">
        <h2>观察池备注</h2>
        <ul>${(data.briefs || []).slice(0, 8).map((item) =>
          `<li><strong>${esc(item.code)}</strong> ${esc(item.notes[0] || "")}</li>`
        ).join("")}</ul>
      </div>
    </div>
  `;
  const ctx = document.getElementById("attrChart");
  if (ctx && window.Chart) {
    new Chart(ctx, {
      type: "bar",
      indexAxis: "y",
      data: {
        labels: (data.attribution || []).map((item) => item.label),
        datasets: [{ label: "品种", data: (data.attribution || []).map((item) => item.value), backgroundColor: "#8b9bb0" }],
      },
      options: { plugins: { legend: { display: false } }, scales: { x: { ticks: { color: "#8b9bb0" } }, y: { ticks: { color: "#8b9bb0" } } } },
    });
  }
  $("copyMd").onclick = async () => {
    await navigator.clipboard.writeText(data.markdown);
  };
  $("dlMd").onclick = () => {
    const blob = new Blob([data.markdown], { type: "text/markdown" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "daily-review.md";
    link.click();
  };
};
