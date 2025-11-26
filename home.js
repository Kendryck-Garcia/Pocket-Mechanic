const addBtn = document.getElementById("add-vehicles-btn")
const form = document.getElementById("vehicle-form")
const saveBtn = document.getElementById("save-vehicle")
const list = document.getElementById("vehicle-list")
const total = document.getElementById("total-vehicles")

let count = 0

addBtn.addEventListener("click", function() {
  if(form.style.display === "block") {
   form.style.display = "none"
  } else {
    form.style.display = "block"
  }
})

saveBtn.addEventListener("click", function() {
  const name = document.getElementById("veh-name").value
  const year = document.getElementById("veh-year").value
  const make = document.getElementById("veh-make").value
  const model = document.getElementById("veh-model").value

  if (name === "" || year === "" || make === "" || model === "") {
    alert("Fill everything out")
    return
  }

  count = count + 1
  total.textContent = count

  const vehicle = document.createElement("vehicle")
  vehicle.textContent = name + " - " + year + " " + make + " " + model
  list.appendChild(vehicle)

  form.style.display = "none"
})
