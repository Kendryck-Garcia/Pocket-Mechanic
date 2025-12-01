const addBtn = document.getElementById("add-vehicles-btn");
const form = document.getElementById("vehicle-form");
const saveBtn = document.getElementById("save-vehicle");
const list = document.getElementById("vehicle-list");
const totalVehiclesElem = document.getElementById("total-vehicles");
const totalLinksElem = document.getElementById("total-links");

const VEHICLES_KEY = "pocketMechanicVehicles";
const LINKS_KEY = "pocketMechanicLinks";

let vehicles = loadVehicles();

renderVehicles();
updateVehicleTotal();
updateLinksTotal();

if (addBtn) {
  addBtn.addEventListener("click", () => {
    clearInputs();
    if (form.style.display === "block") {
      form.style.display = "none";
    } else {
      form.style.display = "block";
    }
  });
}

if (saveBtn) {
  saveBtn.addEventListener("click", () => {
    const name = document.getElementById("veh-name").value.trim();
    const year = document.getElementById("veh-year").value.trim();
    const make = document.getElementById("veh-make").value.trim();
    const model = document.getElementById("veh-model").value.trim();

    if (!name || !year || !make || !model) {
      alert("Please fill everything out.");
      return;
    }

    const newVehicle = {
      id: Date.now().toString(),
      name: name,
      year: year,
      make: make,
      model: model
    };

    vehicles.push(newVehicle);
    saveVehicles();
    renderVehicles();
    updateVehicleTotal();

    form.style.display = "none";
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

function saveVehicles() {
  localStorage.setItem(VEHICLES_KEY, JSON.stringify(vehicles));
}

function renderVehicles() {
  if (!list) return;
  list.innerHTML = "";

  vehicles.forEach((v) => {
    const card = document.createElement("div");
    card.className = "card";
    card.textContent = v.name + " - " + v.year + " " + v.make + " " + v.model;
    list.appendChild(card);
  });
}

function updateVehicleTotal() {
  if (!totalVehiclesElem) return;
  totalVehiclesElem.textContent = String(vehicles.length);
}

function clearInputs() {
  const nameInput = document.getElementById("veh-name");
  const yearInput = document.getElementById("veh-year");
  const makeInput = document.getElementById("veh-make");
  const modelInput = document.getElementById("veh-model");

  if (nameInput) nameInput.value = "";
  if (yearInput) yearInput.value = "";
  if (makeInput) makeInput.value = "";
  if (modelInput) modelInput.value = "";
}

function updateLinksTotal() {
  if (!totalLinksElem) return;

  const raw = localStorage.getItem(LINKS_KEY);
  if (!raw) {
    totalLinksElem.textContent = "0";
    return;
  }

  try {
    const data = JSON.parse(raw) || {};
    let total = 0;

    Object.values(data).forEach((sections) => {
      if (!sections) return;
      const maint = sections.maintenance || [];
      const acc = sections.accessories || [];
      const mods = sections.modifications || [];
      total += maint.length + acc.length + mods.length;
    });

    totalLinksElem.textContent = String(total);
  } catch (e) {
    totalLinksElem.textContent = "0";
  }
}
