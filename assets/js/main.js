/* =========================
   INITIAL LOAD (FIRST TAB ONLY)
========================= */

document.addEventListener("DOMContentLoaded", function () {

  loadNavbar();
  loadFooter();

  const hasVisited = sessionStorage.getItem("hasVisited");

  if (!hasVisited) {
    sessionStorage.setItem("hasVisited", "true");
    showLoader();
  } else {
    document.body.classList.add("loaded");
  }

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

      const toggle = document.getElementById("menu-toggle");
      const navMenu = document.getElementById("nav-menu");
      const overlay = document.getElementById("overlay");

      function openMenu() {
        navMenu.classList.add("active");
        overlay.classList.add("active");
        toggle.classList.add("active");
        document.body.style.overflow = "hidden";
      }

      function closeMenu() {
        navMenu.classList.remove("active");
        overlay.classList.remove("active");
        toggle.classList.remove("active");
        document.body.style.overflow = "";
      }

      function toggleMenu() {
        if (navMenu.classList.contains("active")) {
          closeMenu();
        } else {
          openMenu();
        }
      }

      if (toggle) toggle.addEventListener("click", toggleMenu);

      if (overlay) overlay.addEventListener("click", closeMenu);

      const links = navMenu.querySelectorAll("a");
      links.forEach(link => {
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
   SHOW LOADER (NO REDIRECT)
========================= */

function showLoader() {

  fetch("assets/components/loader.html")
    .then(res => res.text())
    .then(data => {

      const container = document.getElementById("loader-container");
      if (!container) return;

      container.innerHTML = data;
      document.body.classList.remove("loaded");

      startLoader();
    })
    .catch(() => {
      document.body.classList.add("loaded");
    });
}


/* =========================
   ADVANCED MEC LOADER
========================= */

function startLoader() {

  let percent = 0;

  const percentElement = document.getElementById("load-percent");
  const statusText = document.getElementById("status-text");

  const cloud = document.querySelector(".cloud-node");
  const mecStations = document.querySelectorAll(".mec-station");

  const interval = setInterval(() => {

    percent++;

    if (percentElement)
      percentElement.textContent = percent;

    if (percent === 20 && statusText) {
      statusText.textContent = "Activating MEC Base Stations...";
      mecStations.forEach(station => station.classList.add("active"));
    }

    if (percent === 60 && statusText) {
      statusText.textContent = "Establishing MEC–Cloud Communication...";
    }

    if (percent === 85 && statusText) {
      statusText.textContent = "Scaling Cloud Core...";
      if (cloud) cloud.classList.add("active");
    }

    if (percent >= 100) {
      clearInterval(interval);

      if (statusText)
        statusText.textContent = "Federated MEC System Ready";

      setTimeout(() => {
        document.body.classList.add("loaded");
      }, 500);
    }

  }, 20);
}


/* =========================
   INFINITE TYPING ANIMATION
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

  if (!typingElement) {
    setTimeout(typeEffect, 500);
    return;
  }

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

typeEffect();
