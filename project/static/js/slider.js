const btns = document.querySelectorAll(".nav-btn");
const slides = document.querySelectorAll(".image-slide");

let sliderNav = function(manual){
    btns.forEach((btn)=>{
    btn.classList.remove("active-sli");
    });

    slides.forEach((slide)=>{
        slide.classList.remove("active-sli");
        });

    btns[manual].classList.add("active-sli");    
    slides[manual].classList.add("active-sli");
    
}

btns.forEach((btn,i)=>{
    btn.addEventListener("click",()=>{
        sliderNav(i);
        console.log(btn)
    
    })
});