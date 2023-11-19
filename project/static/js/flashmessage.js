
const icons11 = document.querySelectorAll(".icon"); // Select all elements with the class "icon"

icons11.forEach(icon => {
  icon.addEventListener("click", () => {
    const popup = icon.closest(".popup"); // Find the closest popup element to the clicked icon
    if (popup) {
      popup.style.display = "none"; // Hide the popup
    }
  });
});
