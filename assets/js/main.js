/* =========================
   INITIAL LOAD
========================= */

document.addEventListener("DOMContentLoaded", function () {

  loadNavbar();
  loadFooter();

  // Always show page immediately (no loader)
  document.body.classList.add("loaded");

  // Start typing animations
  typeEffect();
  typeQuote();

  // Initialize contact form if present
  initializeContactForm();

});


/* =========================
   NAVBAR & FOOTER
========================= */

function loadNavbar() {
  fetch("assets/components/navbar.html")
    .then(res => res.text())
    .then(data => {

      const navContainer = document.getElementById("navbar");
      if (!navContainer) return;

      navContainer.innerHTML = data;

      // Hide navbar photo on homepage
      const navPhoto = document.getElementById("nav-photo");
      if (
        window.location.pathname.endsWith("index.html") ||
        window.location.pathname === "/" ||
        window.location.pathname.endsWith("/")
      ) {
        if (navPhoto) navPhoto.style.display = "none";
      }

      const toggle = document.getElementById("menu-toggle");
      const navMenu = document.getElementById("nav-menu");
      const overlay = document.getElementById("overlay");

      if (!toggle || !navMenu || !overlay) return;

      function toggleMenu() {
        navMenu.classList.toggle("active");
        overlay.classList.toggle("active");
        toggle.classList.toggle("active");

        document.body.style.overflow =
          navMenu.classList.contains("active") ? "hidden" : "";
      }

      function closeMenu() {
        navMenu.classList.remove("active");
        overlay.classList.remove("active");
        toggle.classList.remove("active");
        document.body.style.overflow = "";
      }

      toggle.addEventListener("click", toggleMenu);
      overlay.addEventListener("click", closeMenu);

      navMenu.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", closeMenu);
      });

    });
}


function loadFooter() {
  fetch("assets/components/footer.html")
    .then(res => res.text())
    .then(data => {
      const foot = document.getElementById("footer");
      if (!foot) return;

      foot.innerHTML = data;

      const year = document.getElementById("current-year");
      if (year) year.textContent = new Date().getFullYear();
    });
}


/* =========================
   DOMAIN TYPING ANIMATION
========================= */

const texts = [
  "Multi-Access Edge Computing",
  "Federated MEC",
  "5G / 6G IoT Systems",
  "Edge Intelligence",
  "Real-Time Scheduling"
];

let textIndex = 0;
let charIndex = 0;
let isDeleting = false;

function typeEffect() {

  const typingElement = document.getElementById("typing");
  if (!typingElement) return;

  const currentText = texts[textIndex];

  if (!isDeleting) {
    typingElement.textContent =
      currentText.substring(0, charIndex + 1);
    charIndex++;

    if (charIndex === currentText.length) {
      setTimeout(() => isDeleting = true, 1500);
    }

  } else {
    typingElement.textContent =
      currentText.substring(0, charIndex - 1);
    charIndex--;

    if (charIndex === 0) {
      isDeleting = false;
      textIndex = (textIndex + 1) % texts.length;
    }
  }

  setTimeout(typeEffect, isDeleting ? 40 : 80);
}


/* =========================
   HERO QUOTE TYPING
========================= */

const quoteText = "I build distributed systems that cannot afford to miss deadlines.";

let quoteIndex = 0;

function typeQuote() {

  const element = document.getElementById("typing-quote");
  if (!element) return;

  element.textContent =
    quoteText.substring(0, quoteIndex + 1);

  quoteIndex++;

  if (quoteIndex < quoteText.length) {
    setTimeout(typeQuote, 40);
  }
}


/* =========================
   PROTECTED CONTACT FORM
========================= */

function initializeContactForm() {

  const form = document.getElementById("contact-form");
  if (!form) return;

  const startTime = Date.now();

  form.addEventListener("submit", async function(e) {

    e.preventDefault();

    const honeypot = form.querySelector("input[name='_gotcha']");
    const now = Date.now();

    const button = form.querySelector(".submit-btn");
    const loader = form.querySelector(".btn-loader");
    const btnText = form.querySelector(".btn-text");
    const status = document.getElementById("form-status");

    // Honeypot protection
    if (honeypot && honeypot.value !== "") {
      return;
    }

    // Time-based bot detection (min 3 sec)
    if ((now - startTime) < 3000) {
      status.textContent = "Submission too fast. Please try again.";
      status.style.color = "#ef4444";
      return;
    }

    // Rate limiting (1 per 60 sec)
    const lastSubmit = localStorage.getItem("lastSubmitTime");
    if (lastSubmit && (now - lastSubmit) < 60000) {
      status.textContent = "Please wait before sending another message.";
      status.style.color = "#ef4444";
      return;
    }

    loader.style.display = "inline-block";
    btnText.textContent = "Sending...";
    button.disabled = true;

    const formData = new FormData(form);

    try {

      const response = await fetch("https://formspree.io/f/xzdakvyp", {
        method: "POST",
        body: formData,
        headers: { 'Accept': 'application/json' }
      });

      if (response.ok) {

        localStorage.setItem("lastSubmitTime", now);

        form.reset();

        btnText.textContent = "Sent ✓";
        status.textContent = "Message sent successfully.";
        status.style.color = "#22c55e";

        setTimeout(() => {
          btnText.textContent = "Send Message";
          status.textContent = "";
        }, 4000);

      } else {
        throw new Error();
      }

    } catch (error) {
      status.textContent = "Network error. Please try again.";
      status.style.color = "#ef4444";
      btnText.textContent = "Send Message";
    }

    loader.style.display = "none";
    button.disabled = false;

  });
}
