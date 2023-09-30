const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");
const form = document.querySelector(".form-container form");
container.classList.remove("sign-up-mode");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
  form.action = "/user-panel/signup";
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
  form.action = "/user-panel/signin";
});
