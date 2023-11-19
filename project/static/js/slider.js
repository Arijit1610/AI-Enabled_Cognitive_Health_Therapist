const btns = document.querySelectorAll(".nav-btn");
const slides = document.querySelectorAll(".image-slide");
let currentSlide = 0;

function changeSlide(manual) {
  btns.forEach((btn) => {
    btn.classList.remove("active-sli");
  });

  slides.forEach((slide) => {
    slide.classList.remove("active-sli");
  });

  btns[manual].classList.add("active-sli");
  slides[manual].classList.add("active-sli");
  currentSlide = manual;
}

function autoSlideChange() {
  currentSlide = (currentSlide + 1) % btns.length;
  changeSlide(currentSlide);
}

btns.forEach((btn, i) => {
  btn.addEventListener("click", () => {
    changeSlide(i);
    clearInterval(autoSlideInterval);
  });
});

// Change slide automatically every 3 seconds (3000 milliseconds)
const autoSlideInterval = setInterval(autoSlideChange, 3000);
