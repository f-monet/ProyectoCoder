const STORAGE_KEY = "rs-discografia-estado";

function loadState() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
  } catch {
    return {};
  }
}

function saveState(state) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch {
    // localStorage no disponible (modo privado, etc.) — se pierde al recargar.
  }
}

let state = loadState();
let currentFilter = "all";
let searchTerm = "";
let onlyMissing = false;

const tbody = document.getElementById("album-body");
const searchInput = document.getElementById("search");
const onlyMissingCheckbox = document.getElementById("only-missing");
const tabs = document.querySelectorAll(".tab");

function getEntry(id) {
  return state[id] || { owned: false, format: "", notes: "" };
}

function updateEntry(id, patch) {
  state[id] = { ...getEntry(id), ...patch };
  saveState(state);
  renderStats();
}

function renderStats() {
  const total = ALBUMS_SEED.length;
  const owned = ALBUMS_SEED.filter((a) => getEntry(a.id).owned).length;
  const missing = total - owned;
  const pct = total ? Math.round((owned / total) * 100) : 0;

  document.getElementById("stat-total").textContent = total;
  document.getElementById("stat-owned").textContent = owned;
  document.getElementById("stat-missing").textContent = missing;
  document.getElementById("stat-pct").textContent = `${pct}%`;
}

function matchesFilters(album) {
  if (currentFilter !== "all" && album.type !== currentFilter) return false;
  if (searchTerm && !album.title.toLowerCase().includes(searchTerm)) return false;
  if (onlyMissing && getEntry(album.id).owned) return false;
  return true;
}

function renderTable() {
  tbody.innerHTML = "";
  const rows = ALBUMS_SEED.filter(matchesFilters).sort((a, b) => a.year - b.year);

  if (rows.length === 0) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td colspan="6" class="empty-row">No hay álbumes que coincidan.</td>`;
    tbody.appendChild(tr);
    return;
  }

  for (const album of rows) {
    const entry = getEntry(album.id);
    const tr = document.createElement("tr");
    if (entry.owned) tr.classList.add("owned-row");

    tr.innerHTML = `
      <td>
        <input type="checkbox" ${entry.owned ? "checked" : ""} data-id="${album.id}" data-field="owned" />
      </td>
      <td>${album.year}</td>
      <td>${album.title}</td>
      <td><span class="badge badge-${album.type}">${album.type}</span></td>
      <td>
        <select data-id="${album.id}" data-field="format">
          <option value="" ${!entry.format ? "selected" : ""}>—</option>
          <option value="Vinilo" ${entry.format === "Vinilo" ? "selected" : ""}>Vinilo</option>
          <option value="CD" ${entry.format === "CD" ? "selected" : ""}>CD</option>
          <option value="Digital" ${entry.format === "Digital" ? "selected" : ""}>Digital</option>
          <option value="Cassette" ${entry.format === "Cassette" ? "selected" : ""}>Cassette</option>
        </select>
      </td>
      <td>
        <input type="text" class="notes-input" placeholder="Notas..." value="${entry.notes || ""}" data-id="${album.id}" data-field="notes" />
      </td>
    `;
    tbody.appendChild(tr);
  }
}

tbody.addEventListener("change", (e) => {
  const target = e.target;
  const id = target.dataset.id;
  const field = target.dataset.field;
  if (!id || !field) return;

  let value;
  if (field === "owned") value = target.checked;
  else value = target.value;

  updateEntry(id, { [field]: value });
  if (field === "owned") renderTable();
});

tbody.addEventListener("input", (e) => {
  const target = e.target;
  if (target.dataset.field === "notes") {
    updateEntry(target.dataset.id, { notes: target.value });
  }
});

searchInput.addEventListener("input", (e) => {
  searchTerm = e.target.value.trim().toLowerCase();
  renderTable();
});

onlyMissingCheckbox.addEventListener("change", (e) => {
  onlyMissing = e.target.checked;
  renderTable();
});

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    tabs.forEach((t) => t.classList.remove("active"));
    tab.classList.add("active");
    currentFilter = tab.dataset.filter;
    renderTable();
  });
});

renderStats();
renderTable();
