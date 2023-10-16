// const popup = document.querySelector(".popup");
// const button = document.getElementById("button");
// const icon = document.getElementById("icon");

// //button.addEventListener("click",()=>{
// //   popup.style.display="flex"
// //});

// icon.addEventListener("click", () => {
//   popup.style.display = "none";
// });

const icons = document.querySelectorAll(".icon"); // Select all elements with the class "icon"

icons.forEach(icon => {
  icon.addEventListener("click", () => {
    const popup = icon.closest(".popup"); // Find the closest popup element to the clicked icon
    if (popup) {
      popup.style.display = "none"; // Hide the popup
    }
  });
});