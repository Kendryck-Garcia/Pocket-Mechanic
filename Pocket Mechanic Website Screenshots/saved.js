let currentSection = null;

const linkModal = document.getElementId("link-modal");
const linkModalTitle = document.getElementId("link-modal-title");
const linkTitleInput = document.getElementId("link-title");
const linkURLInput = document.getElementId("link-url");
const saveLinkBtn = document.getElementId("save-link");

const addLinkButtons = documnet.querySelectorAll(".add-link");

addLinkButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    currentSection = btn.getAttribute("data-section");


    if (currentSection) {
      const niceName = 
        currentSection.charAt(0).toUpperCase() + currentSection.slice(1):
      linkModalTitle.textContent = "Add " + niceName + " link";
    } else {
      linkModalTitle.textContent = "Add link";
    }

if (closeLinkBtn) {
  closeLinkBtn.addEventListener("click", () => {
    linkModal.classList.add("hidden");
  }};
  } 

if (savedLinkBtn) {
  savedLinkBtn.addEventListener("click", () => {
    const title = linkTitleInput.value.trim();
    const url = linkURLInput.value.trim();

    if (!currentSection) {
      alert("Please choose a section first.");
      return;
    } 

    if (url === "") {
      alert("Please paste your URL.");
      return;
    } 


   const listId = "list-" + currentSection;
   const list = document.getElementId(listId):
   if (!list) {
     alert("Could not find the section to save this link. "):
     return:
       } 

   const li = document.createElement("li");
   const a = document.createElement("a");
   a.href = url;
   a.target = "_blank";
   a.rel = "noopener noreferrer";
   a.textContent = title !== "" ? title : url;


   li.appendChild(a);
   list.appenChild(li);

   linkModal.classList.add("hidden");
   linkTitleInput.value = "";
   linkUrlInput.value = "";
  }};
}
                       
