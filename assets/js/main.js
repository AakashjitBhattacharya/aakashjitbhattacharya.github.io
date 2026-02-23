/* =========================
   LOAD SHARED COMPONENTS
========================= */

document.addEventListener("DOMContentLoaded", function () {

  const hasVisited = sessionStorage.getItem("hasVisited");

  loadNavbar();
  loadFooter();

  if (!hasVisited) {

    fetch("assets/components/loader.html")
      .then(res => res.text())
      .then(data => {
        document.getElementById("loader-container").innerHTML = data;
        startLoader();  // <-- THIS calls the function
        sessionStorage.setItem("hasVisited", "true");
      });

  } else {
    document.body.classList.add("loaded");
  }

});
/* =========================
   NAVBAR & FOOTER FUNCTIONS
========================= */

function loadNavbar() {
  fetch("assets/components/navbar.html")
    .then(res => res.text())
    .then(data => {
      document.getElementById("navbar").innerHTML = data;
    });
}

function loadFooter() {
  fetch("assets/components/footer.html")
    .then(res => res.text())
    .then(data => {
      document.getElementById("footer").innerHTML = data;
      document.getElementById("current-year").textContent =
        new Date().getFullYear();
    });
}

/* =========================
   LOADER FUNCTION
========================= */

function startLoader() {

  let percent = 0;
  const percentElement = document.getElementById("load-percent");
  const statusText = document.getElementById("status-text");

  const iot = document.querySelector(".iot");
  const edge = document.querySelector(".edge");
  const cloud = document.querySelector(".cloud");

  const interval = setInterval(() => {

    percent++;
    percentElement.textContent = percent;

    if (percent === 20) {
      iot.classList.add("active");
      statusText.textContent = "IoT Devices Online...";
    }

    if (percent === 50) {
      edge.classList.add("active");
      statusText.textContent = "Deploying Edge Services...";
    }

    if (percent === 80) {
      cloud.classList.add("active");
      statusText.textContent = "Scaling Cloud Infrastructure...";
    }

    if (percent >= 100) {
      clearInterval(interval);

      setTimeout(() => {
        document.body.classList.add("loaded");
      }, 800);
    }

  }, 25);
}

/* =========================
   TYPING ANIMATION
========================= */

const texts = [
  "Multi-Access Edge Computing",
  "Federated MEC",
  "5G / 6G IoT Systems",
  "Edge Intelligence",
  "Real-Time Scheduling"
];

let count = 0;
let index = 0;
let currentText = "";
let letter = "";

(function type() {

  if (count === texts.length) {
    count = 0;
  }

  currentText = texts[count];
  letter = currentText.slice(0, ++index);

  document.getElementById("typing").textContent = letter;

  if (letter.length === currentText.length) {
    setTimeout(() => {
      index = 0;
      count++;
    }, 1500);
  }

  setTimeout(type, 80);

})();
