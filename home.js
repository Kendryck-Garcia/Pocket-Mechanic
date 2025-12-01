const VEHICLES_KEY = "pocketMechanicVehicles";
const LINKS_KEY = "pocketMechanicLinks";

const addBtn = document.getElementById("add-vehicles-btn");
const form = document.getElementById("vehicle-form");
const saveBtn = document.getElementById("save-vehicle");
const list = document.getElementById("vehicle-list");
const totalElem = document.getElementById("total-vehicles");
const totalLinksElem = document.getElementById("total-links");

let vehicles = JSON.parse(localStorage.getItem(VEHICLES_KEY) || "[]");

renderVehicles();
updateTotalVehicles();
updateTotalLinks();

if (addBtn) {
  addBtn.addEventListener("click", () => {
    form.style.display = form.style.display === "block" ? "none" : "block";
  });
}

if (saveBtn) {
  saveBtn.addEventListener("click", () => {
    const name = document.getElementById("veh-name").value.trim();
    const year = document.getElementById("veh-year").value.trim();
    const make = document.getElementById("veh-make").value.trim();
    const model = document.getElementById("veh-model").value.trim();

    if (!name || !year || !make || !model) {
      alert("Please fill in all fields!");
      return;
    }

    const newVehicle = {
      id: Date.now().toString(),
      name,
      year,
      make,
      model
    };

    vehicles.push(newVehicle);
    localStorage.setItem(VEHICLES_KEY, JSON.stringify(vehicles));

    renderVehicles();
    updateTotalVehicles();

    form.style.display = "none";
    clearInputs();
  });
}
function renderVehicles() {
  if (!list) return;
  list.innerHTML = "";
  vehicles.forEach(v => {
    const div = document.createElement("div");
    div.className = "card";
    div.textContent = `${v.name} - ${v.year} ${v.make} ${v.model}`;
    list.appendChild(div);
  });
}

function updateTotalVehicles() {
  if (!totalElem) return;
  totalElem.textContent = String(vehicles.length);
}

function updateTotalLinks() {
  if (!totalLinksElem) return;
  const data = JSON.parse(localStorage.getItem(LINKS_KEY) || "{}");
  let total = 0;
  for (const vehicle of Object.values(data)) {
    total += (vehicle.maintenance?.length || 0)
           + (vehicle.accessories?.length || 0)
           + (vehicle.modifications?.length || 0);
  }
  totalLinksElem.textContent = String(total);
}

function clearInputs() {
  ["veh-name", "veh-year", "veh-make", "veh-model"].forEach(id => {
    const input = document.getElementById(id);
    if (input) input.value = "";
  });
}
