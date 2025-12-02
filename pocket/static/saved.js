document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("toggleSavedBtn");
    const savedSection = document.getElementById("savedPartsSection");

    toggleBtn.addEventListener("click", () => {
        if (savedSection.style.display === "none") {
            savedSection.style.display = "block";
            toggleBtn.textContent = "Hide Saved Parts";
        } else {
            savedSection.style.display = "none";
            toggleBtn.textContent = "Show Saved Parts";
        }
    });
});
