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

const inputs = [
	"input1",
	"input2",
	"input3",
	"input4",
	"input5",
	"input6",
  ];
  
  inputs.map((id) => {
	const input = document.getElementById(id);
	addListener(input);
  });
  
  function addListener(input) {
	input.addEventListener("keyup", () => {
	  const code = parseInt(input.value);
	  if (code >= 0 && code <= 9) {
		const n = input.nextElementSibling;
		if (n) n.focus();
	  } else {
		input.value = "";
	  }
  
	  const key = event.key;
	  if (key === "Backspace" || key === "Delete") {
		const prev = input.previousElementSibling;
		if (prev) prev.focus();
	  }
	});
  }
  
