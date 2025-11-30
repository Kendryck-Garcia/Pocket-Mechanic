const addBtn = document.getElementById("add-vehicles-btn")
const form = document.getElementById("vehicle-form")
const saveBtn = document.getElementById("save-vehicle")
const list = document.getElementById("vehicle-list")
const total = document.getElementById("total-vehicles")

let count = 0

addBtn.addEventListener("click", function () {
  clearInputs()

  if (form.style.display === "block") {
    form.style.display = "none"
  } else {
    form.style.display = "block"
  }
})

saveBtn.addEventListener("click", function () {
  const name = document.getElementById("veh-name").value
  const year = document.getElementById("veh-year").value
  const make = document.getElementById("veh-make").value
  const model = document.getElementById("veh-model").value

  if (name === "" || year === "" || make === "" || model === "") {
    alert("Fill everything out")
    return
  }
  createVehicle(name, year, make, model)

  incrementVehicleTotal()

  form.style.display = "none"
})

function incrementVehicleTotal() {
  count += 1
  total.textContent = count
}

function createVehicle(name, year, make, model) {
  const vehicle = document.createElement("vehicle")
  vehicle.textContent = name + " - " + year + " " + make + " " + model
  list.appendChild(vehicle)
}

function clearInputs() {
  const name = document.getElementById("veh-name")
  const year = document.getElementById("veh-year")
  const make = document.getElementById("veh-make")
  const model = document.getElementById("veh-model")

  name.value = ""
  year.value = ""
  make.value = ""
  model.value = ""
}