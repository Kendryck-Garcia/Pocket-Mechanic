const VEHICLES_KEY = "pocketMechanicVehicles";
const LINKS_KEY = "pocketMechanicLinks";

const vehicleSelect = document.getElementById("saved-vehicle-select");
const listMaintenance = document.getElementById("list-maintenance");
const listAccessories = document.getElementById("list-accessories");
const listModifications = document.getElementById("list-modifications");

const addLinkButtons = document.querySelectorAll(".add-link");

const linkModal = document.getElementById("link-modal");
const linkModalTitle = document.getElementById("link-modal-title");
const linkTitleInput = document.getElementById("link-title");
const linkUrlInput = document.getElementById("link-url");
const saveLinkBtn = document.getElementById("save-link");
const closeLinkBtn = document.getElementById("close-link");

let vehicles = loadVehicles();
let linksByVehicle = loadLinks();
let currentVehicleId = null;
let currentSection = null;

populateVehicleSelect();

if (vehicleSelect && vehicleSelect.options.length > 0 && vehicleSelect.value) {
  currentVehicleId = vehicleSelect.value;
  renderLists();
}

if (vehicleSelect) {
  vehicleSelect.addEventListener("change", () => {
    currentVehicleId = vehicleSelect.value || null;
    renderLists();
  });
}
addLinkButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    if (!currentVehicleId) {
      alert("Add a vehicle on the Home page, then select it here first.");
      return;
    }

    currentSection = btn.getAttribute("data-section"); 

    if (!currentSection) {
      alert("Could not determine which section you clicked.");
      return;
    }

    const niceName =
      currentSection.charAt(0).toUpperCase() + currentSection.slice(1);
    linkModalTitle.textContent = "Add " + niceName + " link";

    linkTitleInput.value = "";
    linkUrlInput.value = "";
    linkModal.classList.remove("hidden");
  });
});

if (closeLinkBtn) {
  closeLinkBtn.addEventListener("click", () => {
    linkModal.classList.add("hidden");
  });
}

if (saveLinkBtn) {
  saveLinkBtn.addEventListener("click", () => {
    const title = linkTitleInput.value.trim();
    const url = linkUrlInput.value.trim();

    if (!currentVehicleId) {
      alert("Please select a vehicle first.");
      return;
    }

    if (!currentSection) {
      alert("Please choose a section.");
      return;
    }

    if (!url) {
      alert("Please paste a website URL.");
      return;
    }

    if (!linksByVehicle[currentVehicleId]) {
      linksByVehicle[currentVehicleId] = {
        maintenance: [],
        accessories: [],
        modifications: []
      };
    }

    linksByVehicle[currentVehicleId][currentSection].push({
      title: title,
      url: url
    });

    saveLinks();
    renderLists();

    linkModal.classList.add("hidden");
    linkTitleInput.value = "";
    linkUrlInput.value = "";
  });
}
function loadVehicles() {
  const raw = localStorage.getItem(VEHICLES_KEY);
  if (!raw) return [];
  try {
    const data = JSON.parse(raw);
    return Array.isArray(data) ? data : [];
  } catch (e) {
    return [];
  }
}

function populateVehicleSelect() {
  if (!vehicleSelect) return;

  vehicleSelect.innerHTML = "";

  if (!vehicles || vehicles.length === 0) {
    const opt = document.createElement("option");
    opt.value = "";
    opt.textContent = "No vehicles yet (add on Home page)";
    vehicleSelect.appendChild(opt);
    vehicleSelect.disabled = true;
    return;
  }

  vehicleSelect.disabled = false;

  vehicles.forEach((v) => {
    const opt = document.createElement("option");
    opt.value = v.id;
    opt.textContent = v.name + " - " + v.year + " " + v.make + " " + v.model;
    vehicleSelect.appendChild(opt);
  });
}

function loadLinks() {
  const raw = localStorage.getItem(LINKS_KEY);
  if (!raw) return {};
  try {
    const data = JSON.parse(raw);
    return data && typeof data === "object" ? data : {};
  } catch (e) {
    return {};
  }
}

function saveLinks() {
  localStorage.setItem(LINKS_KEY, JSON.stringify(linksByVehicle));
}

function renderLists() {
  clearList(listMaintenance);
  clearList(listAccessories);
  clearList(listModifications);

  if (!currentVehicleId || !linksByVehicle[currentVehicleId]) {
    return;
  }

  const data = linksByVehicle[currentVehicleId];

  renderSectionList(listMaintenance, data.maintenance || []);
  renderSectionList(listAccessories, data.accessories || []);
  renderSectionList(listModifications, data.modifications || []);
}

function clearList(ul) {
  if (!ul) return;
  ul.innerHTML = "";
}

function renderSectionList(ul, items) {
  if (!ul) return;
  items.forEach((item) => {
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.href = item.url;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    a.textContent = item.title || item.url;
    li.appendChild(a);
    ul.appendChild(li);
  });
}
            
