const state = {
  payload: null,
  selectedScenario: 'failed-imaging',
  selectedDevice: 'device-003',
  selectedSeverity: 'all',
};

const scenarioIds = [
  'failed-imaging',
  'disabled-user-device-assignment',
  'privileged-user-missing-mfa',
  'endpoint-compliance-queue',
];

const severityOrder = { critical: 4, high: 3, medium: 2, low: 1 };

async function boot() {
  const response = await fetch('demo-data.json');
  state.payload = await response.json();
  renderSummary();
  renderScenarios();
  renderScenarioDetail();
  renderDeviceQueue();
  renderDeviceDetail();
  renderSeverityFilters();
  renderFindings();
}

function renderSummary() {
  const { summary } = state.payload;
  document.querySelector('#total-devices').textContent = summary.total_devices;
  document.querySelector('#total-users').textContent = summary.total_users;
  document.querySelector('#total-findings').textContent = summary.total_findings;
}

function renderScenarios() {
  const list = document.querySelector('#scenario-list');
  list.innerHTML = state.payload.scenarios.map((scenario) => `
    <button class="scenario-button ${scenario.id === state.selectedScenario ? 'active' : ''}"
      data-scenario-id="${scenario.id}">
      <strong>${escapeHtml(scenario.title)}</strong>
      <span>${escapeHtml(scenario.job_relevance)}</span>
    </button>
  `).join('');

  list.querySelectorAll('button').forEach((button) => {
    button.addEventListener('click', () => {
      state.selectedScenario = button.dataset.scenarioId;
      renderScenarios();
      renderScenarioDetail();
    });
  });
}

function renderScenarioDetail() {
  const scenario = state.payload.scenarios.find((item) => item.id === state.selectedScenario);
  const report = scenario.report;
  const target = document.querySelector('#scenario-detail');
  target.innerHTML = `
    <p class="eyebrow">Scenario ID: ${escapeHtml(report.scenario_id)}</p>
    <h3>${escapeHtml(report.title)}</h3>
    <div class="detail-grid">
      <div class="detail-box"><span>Ticket</span><strong>${escapeHtml(report.ticket)}</strong></div>
      <div class="detail-box"><span>Affected assets</span><strong>${report.affected_assets.map(escapeHtml).join(', ')}</strong></div>
    </div>
    <h3>Findings</h3>
    ${renderList(report.findings)}
    <h3>Technician actions</h3>
    ${renderOrderedList(report.technician_actions)}
    <h3>Verification</h3>
    ${renderOrderedList(report.verification_steps)}
  `;
}

function renderDeviceQueue() {
  const devicesById = new Map(state.payload.devices.map((device) => [device.id, device]));
  const list = document.querySelector('#device-list');
  list.innerHTML = state.payload.top_risky_assets
    .filter((asset) => asset.asset_type === 'device')
    .map((asset) => {
      const device = devicesById.get(asset.asset_id);
      return `
        <button class="device-card ${device.id === state.selectedDevice ? 'active' : ''}"
          data-device-id="${device.id}">
          <strong>${escapeHtml(device.hostname)}</strong>
          <span>${asset.finding_count} findings · highest ${asset.highest_severity}</span>
        </button>
      `;
    })
    .join('');

  list.querySelectorAll('button').forEach((button) => {
    button.addEventListener('click', () => {
      state.selectedDevice = button.dataset.deviceId;
      renderDeviceQueue();
      renderDeviceDetail();
    });
  });
}

function renderDeviceDetail() {
  const device = state.payload.devices.find((item) => item.id === state.selectedDevice);
  const user = state.payload.users.find((item) => item.id === device.assigned_user_id);
  const findings = state.payload.findings.filter((finding) => finding.asset_id === device.id);
  const target = document.querySelector('#device-detail');
  target.innerHTML = `
    <p class="eyebrow">Endpoint record</p>
    <h3>${escapeHtml(device.hostname)}</h3>
    <div class="detail-grid">
      <div class="detail-box"><span>Assigned user</span><strong>${escapeHtml(user.username)}</strong></div>
      <div class="detail-box"><span>OS baseline</span><strong>${escapeHtml(device.os_name)} ${escapeHtml(device.os_version)}</strong></div>
      <div class="detail-box"><span>Compliance</span><strong>${escapeHtml(device.compliance_state)}</strong></div>
      <div class="detail-box"><span>Imaging</span><strong>${escapeHtml(device.imaging_state)}</strong></div>
      <div class="detail-box"><span>Patch status</span><strong>${escapeHtml(device.patch_status)}</strong></div>
      <div class="detail-box"><span>Local admins</span><strong>${device.local_admin_count}</strong></div>
    </div>
    <h3>Device findings</h3>
    ${renderList(findings.map((finding) => `${finding.severity.toUpperCase()} ${finding.category}: ${finding.title} — ${finding.recommendation}`))}
  `;
}

function renderSeverityFilters() {
  const severities = ['all', ...new Set(state.payload.findings.map((finding) => finding.severity))]
    .sort((a, b) => (severityOrder[b] ?? 99) - (severityOrder[a] ?? 99));
  const filters = document.querySelector('#severity-filters');
  filters.innerHTML = severities.map((severity) => `
    <button class="${severity === state.selectedSeverity ? 'active' : ''}" data-severity="${severity}">
      ${severity}
    </button>
  `).join('');

  filters.querySelectorAll('button').forEach((button) => {
    button.addEventListener('click', () => {
      state.selectedSeverity = button.dataset.severity;
      renderSeverityFilters();
      renderFindings();
    });
  });
}

function renderFindings() {
  const findings = state.payload.findings
    .filter((finding) => state.selectedSeverity === 'all' || finding.severity === state.selectedSeverity)
    .sort((a, b) => (severityOrder[b.severity] - severityOrder[a.severity]) || a.id.localeCompare(b.id));
  const grid = document.querySelector('#findings-grid');
  grid.innerHTML = findings.map((finding) => `
    <article class="finding-card">
      <header>
        <span class="severity ${finding.severity}">${finding.severity}</span>
        <span class="category">${finding.category}</span>
      </header>
      <h3>${escapeHtml(finding.title)}</h3>
      <p>${escapeHtml(finding.recommendation)}</p>
      <p class="codeish">Asset: ${escapeHtml(finding.asset_type)} / ${escapeHtml(finding.asset_id)}</p>
      <p class="codeish">Control: ${escapeHtml(finding.control_mapping)}</p>
    </article>
  `).join('');
}

function renderList(items) {
  if (!items.length) return '<p class="codeish">No findings for this asset.</p>';
  return `<ul>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul>`;
}

function renderOrderedList(items) {
  return `<ol>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ol>`;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

boot().catch((error) => {
  document.body.innerHTML = `<main class="shell panel"><h1>Demo failed to load</h1><p>${escapeHtml(error.message)}</p></main>`;
});
