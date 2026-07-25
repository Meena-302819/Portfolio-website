// ======================================
// Professional Portfolio Script
// ======================================

// Smooth Scroll

document.querySelectorAll('nav a').forEach(link => {

    link.addEventListener('click', function(e){

        e.preventDefault();

        const target = document.querySelector(this.getAttribute('href'));

        target.scrollIntoView({

            behavior:'smooth'

        });

    });

});

// ======================================
// Active Navbar
// ======================================

const sections = document.querySelectorAll("section");

const navLinks = document.querySelectorAll("nav ul li a");

window.addEventListener("scroll", ()=>{

    let current="";

    sections.forEach(section=>{

        const sectionTop = section.offsetTop-120;

        if(pageYOffset>=sectionTop){

            current=section.getAttribute("id");

        }

    });

    navLinks.forEach(link=>{

        link.classList.remove("active");

        if(link.getAttribute("href")==="#"+current){

            link.classList.add("active");

        }

    });

});

// ======================================
// Reveal Animation
// ======================================

const revealElements=document.querySelectorAll(

".project-card,.skill,.about-container,.contact-container"

);

function reveal(){

    revealElements.forEach(el=>{

        const top=el.getBoundingClientRect().top;

        const visible=window.innerHeight-120;

        if(top<visible){

            el.classList.add("fade");

        }

    });

}

window.addEventListener("scroll",reveal);

reveal();

// ======================================
// Typing Effect
// ======================================

const title=document.querySelector(".left h2");

const words=[

"Python Full Stack Developer",

"Frontend Developer",

"Flask Developer",

"UI Designer"

];

let wordIndex=0;

let charIndex=0;

let deleting=false;

function typing(){

    const current=words[wordIndex];

    if(!deleting){

        title.textContent=current.substring(0,charIndex++);

        if(charIndex>current.length){

            deleting=true;

            setTimeout(typing,1500);

            return;

        }

    }else{

        title.textContent=current.substring(0,charIndex--);

        if(charIndex===0){

            deleting=false;

            wordIndex=(wordIndex+1)%words.length;

        }

    }

    setTimeout(typing,deleting?50:100);

}

typing();

// ======================================
// Button Hover Animation
// ======================================

document.querySelectorAll(".btn,.btn2,.project-btn").forEach(btn=>{

btn.addEventListener("mouseenter",()=>{

btn.style.transform="translateY(-5px) scale(1.05)";

});

btn.addEventListener("mouseleave",()=>{

btn.style.transform="translateY(0px) scale(1)";

});

});

// ======================================
// Console
// ======================================

console.log("Portfolio Loaded Successfully");
