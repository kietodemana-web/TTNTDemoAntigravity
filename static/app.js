// Antigravity AI - Computer Troubleshooting Diagnostic System
// Naive Bayes Classifier Demo on Real Data (ORA & Hugging Face)

let BENCHMARK_CACHE = null;
let currentDatasetPage = 1;
const datasetPageSize = 15;
let charts = {};

// Color palette for 7 categories
const CATEGORY_COLORS = {
  "Nguồn": "#f59e0b",
  "Màn hình": "#3b82f6",
  "Quá nhiệt": "#ef4444",
  "Ổ cứng": "#8b5cf6",
  "RAM": "#ec4899",
  "Mạng": "#06b6d4",
  "Phần mềm": "#10b981"
};

document.addEventListener("DOMContentLoaded", () => {
  initNavigation();
  loadSymptomTags();
  initDiagnosticEvents();
  initDatasetExplorer();
  loadBenchmarkData();
});

/* ===================================================================
   NAVIGATION TABS
=================================================================== */
function initNavigation() {
  const tabs = document.querySelectorAll(".nav-tab");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");

      const tabId = tab.getAttribute("data-tab");
      document.querySelectorAll(".tab-pane").forEach(pane => {
        pane.classList.remove("active");
      });

      const activePane = document.getElementById(`tab-${tabId}`);
      if (activePane) {
        activePane.classList.add("active");
      }

      // If switching to benchmark tab, render charts
      if (tabId === "benchmark" && BENCHMARK_CACHE) {
        setTimeout(renderBenchmarkCharts, 50);
      }
    });
  });
}

/* ===================================================================
   SYMPTOM TAGS & QUICK SCENARIOS
=================================================================== */
async function loadSymptomTags() {
  try {
    const res = await fetch("/api/symptom-tags");
    const tags = await res.json();
    const container = document.getElementById("symptom-tags-container");
    container.innerHTML = "";

    tags.forEach(tag => {
      const item = document.createElement("label");
      item.className = "tag-checkbox-item";
      item.innerHTML = `
        <input type="checkbox" value="${tag.label}" data-id="${tag.id}" id="tag-${tag.id}">
        <span class="tag-label-text">${tag.label}</span>
      `;

      const checkbox = item.querySelector("input");
      checkbox.addEventListener("change", () => {
        if (checkbox.checked) {
          item.classList.add("checked");
        } else {
          item.classList.remove("checked");
        }
        updateSelectedTagsCount();
      });

      container.appendChild(item);
    });
  } catch (err) {
    console.error("Failed to load symptom tags:", err);
  }
}

function updateSelectedTagsCount() {
  const checked = document.querySelectorAll("#symptom-tags-container input:checked");
  document.getElementById("selected-tags-count").textContent = `Đã chọn: ${checked.length}`;
}

function initDiagnosticEvents() {
  // Clear button
  document.getElementById("btn-clear-input").addEventListener("click", () => {
    document.getElementById("symptom-input").value = "";
    document.querySelectorAll("#symptom-tags-container input").forEach(cb => {
      cb.checked = false;
      cb.closest(".tag-checkbox-item").classList.remove("checked");
    });
    updateSelectedTagsCount();
    document.getElementById("result-container").classList.add("hidden");
    document.getElementById("result-placeholder").classList.remove("hidden");
  });

  // Quick scenarios buttons
  document.querySelectorAll(".scenario-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const text = btn.getAttribute("data-symptom");
      const tagIds = (btn.getAttribute("data-tags") || "").split(",");

      document.getElementById("symptom-input").value = text;

      // Clear existing checkboxes
      document.querySelectorAll("#symptom-tags-container input").forEach(cb => {
        cb.checked = false;
        cb.closest(".tag-checkbox-item").classList.remove("checked");
      });

      // Check matched tags
      tagIds.forEach(id => {
        const cb = document.getElementById(`tag-${id.trim()}`);
        if (cb) {
          cb.checked = true;
          cb.closest(".tag-checkbox-item").classList.add("checked");
        }
      });

      updateSelectedTagsCount();

      // Automatically trigger diagnosis
      performDiagnosis();
    });
  });

  // Submit diagnosis button
  document.getElementById("btn-submit-diag").addEventListener("click", performDiagnosis);
}

/* ===================================================================
   DIAGNOSIS EXECUTION & RENDERING
=================================================================== */
async function performDiagnosis() {
  const symptoms = document.getElementById("symptom-input").value.trim();
  const checkedBoxes = document.querySelectorAll("#symptom-tags-container input:checked");
  const selectedTags = Array.from(checkedBoxes).map(cb => cb.value);

  if (!symptoms && selectedTags.length === 0) {
    alert("Vui lòng nhập mô tả sự cố hoặc tick chọn ít nhất 1 dấu hiệu triệu chứng!");
    return;
  }

  const btn = document.getElementById("btn-submit-diag");
  const spinner = document.getElementById("diag-spinner");
  btn.disabled = true;
  spinner.classList.remove("hidden");

  try {
    const res = await fetch("/api/diagnose", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        symptoms: symptoms,
        selected_tags: selectedTags
      })
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || "Có lỗi xảy ra khi chẩn đoán.");
    }

    renderDiagnosisResult(data);
  } catch (err) {
    alert("Lỗi chẩn đoán: " + err.message);
  } finally {
    btn.disabled = false;
    spinner.classList.add("hidden");
  }
}

function renderDiagnosisResult(data) {
  document.getElementById("result-placeholder").classList.add("hidden");
  const resultCard = document.getElementById("result-container");
  resultCard.classList.remove("hidden");

  // Inference time
  document.getElementById("inference-time-badge").textContent = `⚡ ${data.inference_time_ms} ms (Naive Bayes α=1)`;

  // Top 3 list
  const listContainer = document.getElementById("top-predictions-list");
  listContainer.innerHTML = "";

  data.top_predictions.forEach((pred, idx) => {
    const card = document.createElement("div");
    card.className = `prediction-card rank-${pred.rank}`;

    let subCausesHtml = "";
    if (pred.sub_causes && pred.sub_causes.length > 0) {
      subCausesHtml = `
        <div class="sub-causes-box">
          <div class="sub-cause-title">🔍 Chi tiết các nguyên nhân cụ thể:</div>
          ${pred.sub_causes.map(sc => `
            <div class="sub-cause-item">
              <span class="sub-cause-name">${sc.name}</span>
              <span class="sub-cause-pct">${sc.probability}%</span>
            </div>
          `).join("")}
        </div>
      `;
    }

    card.innerHTML = `
      <div class="pred-top-row">
        <div class="pred-left">
          <div class="rank-circle">#${pred.rank}</div>
          <span class="pred-icon">${pred.icon}</span>
          <span class="pred-name">${pred.category}</span>
        </div>
        <div class="pred-prob" style="color: ${pred.color}">${pred.probability}%</div>
      </div>
      <div class="prob-bar-track">
        <div class="prob-bar-fill" style="width: 0%; background: ${pred.color}"></div>
      </div>
      <div class="pred-desc">${pred.description}</div>
      ${subCausesHtml}
    `;

    listContainer.appendChild(card);

    // Animate progress bar fill
    setTimeout(() => {
      const fill = card.querySelector(".prob-bar-fill");
      if (fill) fill.style.width = `${Math.min(pred.probability, 100)}%`;
    }, 50);
  });

  // All 7 classes probability distribution
  const allProbContainer = document.getElementById("all-prob-bars");
  allProbContainer.innerHTML = "";

  for (const [cat, prob] of Object.entries(data.all_probabilities)) {
    const color = CATEGORY_COLORS[cat] || "#94a3b8";
    const row = document.createElement("div");
    row.className = "prob-bar-row";
    row.innerHTML = `
      <span class="prob-bar-label">${cat}</span>
      <div class="prob-bar-track" style="margin: 0; height: 6px;">
        <div class="prob-bar-fill" style="width: 0%; background: ${color}"></div>
      </div>
      <span class="prob-bar-val">${prob}%</span>
    `;
    allProbContainer.appendChild(row);

    setTimeout(() => {
      const fill = row.querySelector(".prob-bar-fill");
      if (fill) fill.style.width = `${Math.min(prob, 100)}%`;
    }, 50);
  }

  // Recommendation & Safety steps (using Rank 1 primary category)
  const primary = data.top_predictions[0];
  const recBox = document.getElementById("recommendation-box");

  recBox.innerHTML = `
    <h4 class="rec-section-title">
      <span>🛡️</span> Các Bước Kiểm Tra An Toàn Ban Đầu (${primary.category})
    </h4>
    <ul class="safety-list">
      ${primary.safety_steps.map(step => `<li>${step}</li>`).join("")}
    </ul>

    <h4 class="rec-section-title">
      <span>🔧</span> Quy Trình Khắc Phục Khuyến Nghị
    </h4>
    <ul class="resolution-list">
      ${primary.resolution_steps.map(step => `<li>${step}</li>`).join("")}
    </ul>
  `;
}

/* ===================================================================
   BENCHMARK & EVALUATION RESULTS (SLIDES 8, 9, 10)
=================================================================== */
async function loadBenchmarkData() {
  try {
    const res = await fetch("/api/benchmark");
    BENCHMARK_CACHE = await res.json();
    populateBenchmarkKPIs(BENCHMARK_CACHE);
    populatePerClassTable(BENCHMARK_CACHE);
    populateConfusionMatrix(BENCHMARK_CACHE);
  } catch (err) {
    console.error("Failed to load benchmark data:", err);
  }
}

function populateBenchmarkKPIs(data) {
  const total = data.dataset_info.total_samples.toLocaleString();
  const nbModel = data.models["Naive Bayes (MultinomialNB)"];

  document.getElementById("kpi-total-samples").textContent = total;
  document.getElementById("kpi-nb-acc").textContent = `${nbModel.accuracy}%`;
  document.getElementById("kpi-top3-acc").textContent = `${nbModel.top3_accuracy}%`;
  document.getElementById("kpi-latency").textContent = `${nbModel.latency_ms} ms`;

  document.getElementById("donut-acc-val").textContent = `${nbModel.accuracy}%`;
  document.getElementById("donut-top3-val").textContent = `${nbModel.top3_accuracy}%`;
}

function populatePerClassTable(data) {
  const tbody = document.getElementById("per-class-tbody");
  tbody.innerHTML = "";

  const nbModel = data.models["Naive Bayes (MultinomialNB)"];
  for (const [cat, metrics] of Object.entries(nbModel.per_class)) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><strong style="color: ${CATEGORY_COLORS[cat] || '#fff'}">${cat}</strong></td>
      <td>${metrics.precision}%</td>
      <td>${metrics.recall}%</td>
      <td><strong>${metrics.f1_score}%</strong></td>
      <td>${metrics.support}</td>
    `;
    tbody.appendChild(tr);
  }
}

function renderBenchmarkCharts() {
  if (!BENCHMARK_CACHE) return;

  const nbModel = BENCHMARK_CACHE.models["Naive Bayes (MultinomialNB)"];
  const categories = Object.keys(nbModel.per_class);

  // 1. Chart per class: Precision, Recall, F1 (Slide 9)
  const ctxPerClass = document.getElementById("chart-per-class");
  if (ctxPerClass) {
    if (charts.perClass) charts.perClass.destroy();

    const precisions = categories.map(c => nbModel.per_class[c].precision);
    const recalls = categories.map(c => nbModel.per_class[c].recall);
    const f1s = categories.map(c => nbModel.per_class[c].f1_score);

    charts.perClass = new Chart(ctxPerClass, {
      type: "bar",
      data: {
        labels: categories,
        datasets: [
          {
            label: "Precision (%)",
            data: precisions,
            backgroundColor: "#06b6d4"
          },
          {
            label: "Recall (%)",
            data: recalls,
            backgroundColor: "#6366f1"
          },
          {
            label: "F1-Score (%)",
            data: f1s,
            backgroundColor: "#10b981"
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: { color: "#cbd5e1", font: { family: "'Plus Jakarta Sans', sans-serif" } }
          }
        },
        scales: {
          x: {
            ticks: { color: "#94a3b8" },
            grid: { color: "rgba(255, 255, 255, 0.05)" }
          },
          y: {
            min: 0,
            max: 100,
            ticks: { color: "#94a3b8" },
            grid: { color: "rgba(255, 255, 255, 0.05)" }
          }
        }
      }
    });
  }

  // 2. Accuracy Donut chart
  const ctxDonut = document.getElementById("chart-accuracy-donut");
  if (ctxDonut) {
    if (charts.donut) charts.donut.destroy();

    const correct = nbModel.accuracy;
    const incorrect = +(100 - correct).toFixed(2);

    charts.donut = new Chart(ctxDonut, {
      type: "doughnut",
      data: {
        labels: ["Chính xác", "Chưa đúng"],
        datasets: [{
          data: [correct, incorrect],
          backgroundColor: ["#10b981", "#f43f5e"],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "70%",
        plugins: { legend: { display: false } }
      }
    });
  }

  // 3. Model Comparison Chart (Slide 10)
  const ctxComp = document.getElementById("chart-model-comparison");
  if (ctxComp) {
    if (charts.comp) charts.comp.destroy();

    const modelNames = Object.keys(BENCHMARK_CACHE.models);
    const accuracies = modelNames.map(m => BENCHMARK_CACHE.models[m].accuracy);
    const top3s = modelNames.map(m => BENCHMARK_CACHE.models[m].top3_accuracy);

    charts.comp = new Chart(ctxComp, {
      type: "bar",
      data: {
        labels: modelNames.map(m => m.replace(" (MultinomialNB)", "").replace(" (BernoulliNB)", " (Bernoulli)")),
        datasets: [
          {
            label: "Accuracy (Top-1 %)",
            data: accuracies,
            backgroundColor: "#6366f1"
          },
          {
            label: "Top-3 Accuracy (%)",
            data: top3s,
            backgroundColor: "#06b6d4"
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: "#cbd5e1" } }
        },
        scales: {
          x: { ticks: { color: "#94a3b8" }, grid: { display: false } },
          y: { min: 70, max: 100, ticks: { color: "#94a3b8" }, grid: { color: "rgba(255, 255, 255, 0.05)" } }
        }
      }
    });
  }

  // 4. Learning curve chart (Slide 10)
  const ctxCurve = document.getElementById("chart-learning-curve");
  if (ctxCurve) {
    if (charts.curve) charts.curve.destroy();

    const sizes = BENCHMARK_CACHE.learning_curve.sample_sizes.map(s => s >= 1000 ? `${(s/1000).toFixed(1)}k` : s);
    const accs = BENCHMARK_CACHE.learning_curve.nb_accuracies;

    charts.curve = new Chart(ctxCurve, {
      type: "line",
      data: {
        labels: sizes,
        datasets: [{
          label: "Naive Bayes Test Accuracy (%)",
          data: accs,
          borderColor: "#06b6d4",
          backgroundColor: "rgba(6, 182, 212, 0.15)",
          fill: true,
          tension: 0.3,
          pointRadius: 5,
          pointBackgroundColor: "#06b6d4"
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: "#cbd5e1" } }
        },
        scales: {
          x: { title: { display: true, text: "Số lượng mẫu huấn luyện (Train Size)", color: "#94a3b8" }, ticks: { color: "#94a3b8" }, grid: { color: "rgba(255, 255, 255, 0.05)" } },
          y: { min: 80, max: 96, ticks: { color: "#94a3b8" }, grid: { color: "rgba(255, 255, 255, 0.05)" } }
        }
      }
    });
  }
}

function populateConfusionMatrix(data) {
  const container = document.getElementById("confusion-matrix-wrapper");
  const categories = data.dataset_info.categories;
  const cm = data.models["Naive Bayes (MultinomialNB)"].confusion_matrix;

  let tableHtml = `
    <table class="cm-table">
      <thead>
        <tr>
          <th>Thực tế \\ Dự đoán</th>
          ${categories.map(c => `<th>${c}</th>`).join("")}
        </tr>
      </thead>
      <tbody>
  `;

  cm.forEach((row, rIdx) => {
    tableHtml += `<tr><th>${categories[rIdx]}</th>`;
    row.forEach((val, cIdx) => {
      const isDiagonal = (rIdx === cIdx);
      let bg = "rgba(255, 255, 255, 0.02)";
      let textColor = "#94a3b8";

      if (isDiagonal) {
        bg = "rgba(16, 185, 129, 0.28)";
        textColor = "#6ee7b7";
      } else if (val > 10) {
        bg = "rgba(244, 63, 94, 0.25)";
        textColor = "#fca5a5";
      } else if (val > 0) {
        bg = "rgba(245, 158, 11, 0.12)";
        textColor = "#fde68a";
      }

      tableHtml += `<td class="cm-cell" style="background: ${bg}; color: ${textColor}">${val}</td>`;
    });
    tableHtml += `</tr>`;
  });

  tableHtml += `</tbody></table>`;
  container.innerHTML = tableHtml;
}

/* ===================================================================
   DATASET EXPLORER TAB (18,047 SAMPLES)
=================================================================== */
function initDatasetExplorer() {
  loadDatasetPage(1);

  document.getElementById("btn-apply-filter").addEventListener("click", () => {
    currentDatasetPage = 1;
    loadDatasetPage(1);
  });

  document.getElementById("dataset-search").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      currentDatasetPage = 1;
      loadDatasetPage(1);
    }
  });

  document.getElementById("btn-prev-page").addEventListener("click", () => {
    if (currentDatasetPage > 1) {
      currentDatasetPage--;
      loadDatasetPage(currentDatasetPage);
    }
  });

  document.getElementById("btn-next-page").addEventListener("click", () => {
    currentDatasetPage++;
    loadDatasetPage(currentDatasetPage);
  });
}

async function loadDatasetPage(page) {
  const source = document.getElementById("filter-source").value;
  const category = document.getElementById("filter-category").value;
  const search = document.getElementById("dataset-search").value.trim();

  const params = new URLSearchParams({
    page: page,
    page_size: datasetPageSize
  });

  if (source !== "All") params.append("source", source);
  if (category !== "All") params.append("category", category);
  if (search) params.append("search", search);

  try {
    const res = await fetch(`/api/dataset-samples?${params.toString()}`);
    const data = await res.json();

    renderDatasetTable(data);
  } catch (err) {
    console.error("Failed to load dataset records:", err);
  }
}

function renderDatasetTable(data) {
  const tbody = document.getElementById("dataset-tbody");
  tbody.innerHTML = "";

  if (data.samples.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; padding: 30px; color: #94a3b8;">Không tìm thấy mẫu dữ liệu nào phù hợp với điều kiện lọc.</td></tr>`;
    document.getElementById("records-counter").textContent = "Không có kết quả";
    document.getElementById("btn-prev-page").disabled = true;
    document.getElementById("btn-next-page").disabled = true;
    return;
  }

  const start = (data.page - 1) * data.page_size + 1;
  const end = Math.min(data.page * data.page_size, data.total);
  document.getElementById("records-counter").textContent = `Hiển thị mẫu ${start} - ${end} trên tổng số ${data.total.toLocaleString()}`;
  document.getElementById("page-indicator").textContent = `Trang ${data.page} / ${data.total_pages}`;

  document.getElementById("btn-prev-page").disabled = (data.page <= 1);
  document.getElementById("btn-next-page").disabled = (data.page >= data.total_pages);

  data.samples.forEach(item => {
    const isHF = item.source.includes("Hugging Face");
    const sourceClass = isHF ? "hf" : "ora";
    const sourceShort = isHF ? "Hugging Face" : "Open Repair";
    const catColor = CATEGORY_COLORS[item.category] || "#94a3b8";

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><code style="font-family: var(--font-mono); font-size: 11.5px; color: #93c5fd;">${item.sample_id}</code></td>
      <td><span class="badge-source ${sourceClass}">${sourceShort}</span></td>
      <td><span class="badge-cat" style="background: ${catColor}20; color: ${catColor}; border: 1px solid ${catColor}40;">${item.category}</span></td>
      <td><strong>${item.issue_name}</strong></td>
      <td style="color: #cbd5e1;">${item.raw_symptoms}</td>
      <td style="color: #94a3b8; font-size: 12px;">${item.solution_steps || item.causes || 'Được kiểm tra tại sự kiện'}</td>
    `;
    tbody.appendChild(tr);
  });
}
