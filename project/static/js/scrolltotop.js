window.addEventListener("DOMContentLoaded", () => {
  const bookvisit = document.querySelectorAll(".bookvisit");

  bookvisit.forEach((element) => {
    element.addEventListener("click", () => {
      const docslider = document.querySelector(".doc-slider");
      docslider.scrollIntoView({ behavior: "smooth" });
      console.log("Arijit");
    });
  });
});
