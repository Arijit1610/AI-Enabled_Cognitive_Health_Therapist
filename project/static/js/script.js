const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");
const otp_container = document.querySelector("#otp-conainer");
// const signup=document.querySelector("#sign-up");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});
const signup = () => {
  otp_container.classList.add("verify");
};

// // hide button
// const passicons = document.querySelectorAll(".pass-icon"); 
// const passwords = document.querySelectorAll(".password"); 

// passicons.forEach((passicon, index) => {
//   passicon.addEventListener("click", () => {
//     const pd = passwords[index];
//     if (pd.type === "password") {
//       pd.type = "text";
//       passicon.src = '${window.static}/eye.png';
//     } else {
//       pd.type = "password";
//       passicon.src = '${window.static}/hidden.png';
//     }
//   });
// });


// //password strength check
// const alphabet = /[a-zA-Z]/;
// const number = /[0-9]/;
// const symbols = /[!,@,#,$,%,^,&,*,?,_,(,),-,+,=,~,/,\,|]/;

// const pwd = document.querySelectorAll(".pwd");
// const stpara = document.querySelectorAll(".st_para");

// const strengthchecker = (passwordInput,index) => {
//   if (passwordInput.length === 0) {
//     pwd[index].style.border = "none";
//     stpara[index].style.color = "none";
//     stpara[index].innerHTML = "";
//   }
//   if (
//     alphabet.test(passwordInput) &&
//     number.test(passwordInput) &&
//     symbols.test(passwordInput)
//   ) {
//     console.log("strong");
//     pwd[index].style.border = "2px solid  rgb(8, 146, 8)";
//     stpara[index].style.color = "rgb(8, 146, 8)";
//     stpara[index].innerHTML = "Strong";
//   } else if (
//     (alphabet.test(passwordInput) && number.test(passwordInput)) ||
//     (alphabet.test(passwordInput) && symbols.test(passwordInput)) ||
//     (number.test(passwordInput) && symbols.test(passwordInput))
//   ) {
//     console.log("medium");
//     pwd[index].style.border = "2px solid  rgb(206, 206, 5)";
//     stpara[index].style.color = "rgb(206, 206, 5)";
//     stpara[index].innerHTML = "Medium";
//   } else if (
//     alphabet.test(passwordInput) ||
//     number.test(passwordInput) ||
//     symbols.test(passwordInput)
//   ) {
//     console.log("weak");
//     pwd[index].style.border = "2px solid  rgb(235, 10, 10)";
//     stpara[index].style.color = " rgb(235, 10, 10)";
//     stpara[index].innerHTML = "Weak";
//   }
//   // if(passwordInput.length>=8 && passwordInput.length<=16){
//   //   console.log('ok');
//   // }
//   // else{
//   //   console.log('invalid');
//   // }
// };

// passwords.forEach((ele,ind) => {
//   ele.addEventListener("input", () => {
 
//     const passwordInput = ele.value;
  
//     strengthchecker(passwordInput,ind);
//   });
  
// });

//otp
const inputs = ["input1", "input2", "input3", "input4", "input5", "input6"];

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
