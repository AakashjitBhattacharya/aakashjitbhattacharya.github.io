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
        const container = document.getElementById("loader-container");
        if (!container) return;

        container.innerHTML = data;
        startLoader();
        sessionStorage.setItem("hasVisited", "true");
      })
      .catch(() => {
        // If loader fails, show page anyway
        document.body.classList.add("loaded");
      });

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
      const nav = document.getElementById("navbar");
      if (nav) nav.innerHTML = data;
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
   ADVANCED LOADER FUNCTION
========================= */

function startLoader() {

  let percent = 0;

  const percentElement = document.getElementById("load-percent");
  const statusText = document.getElementById("status-text");

  const layers = {
    iot: document.querySelector(".iot"),
    fog: document.querySelector(".fog"),
    edge: document.querySelector(".edge"),
    mec: document.querySelector(".mec"),
    cloud: document.querySelector(".cloud")
  };

  const connections = document.querySelectorAll(".connection");

  const interval = setInterval(() => {

    percent++;

    if (percentElement)
      percentElement.textContent = percent;

    if (percent === 10 && layers.iot) {
      layers.iot.classList.add("active");
      statusText.textContent = "IoT Devices Activated";
    }

    if (percent === 25 && layers.fog) {
      layers.fog.classList.add("active");
      connections[2]?.classList.add("active");
      connections[3]?.classList.add("active");
      statusText.textContent = "Fog Layer Online";
    }

    if (percent === 45 && layers.edge) {
      layers.edge.classList.add("active");
      connections[0]?.classList.add("active");
      statusText.textContent = "Edge Nodes Deployed";
    }

    if (percent === 65 && layers.mec) {
      layers.mec.classList.add("active");
      connections[1]?.classList.add("active");
      statusText.textContent = "MEC Platform Initializing";
    }

    if (percent === 85 && layers.cloud) {
      layers.cloud.classList.add("active");
      statusText.textContent = "Cloud Infrastructure Scaling";
    }

    if (percent >= 100) {
      clearInterval(interval);

      statusText.textContent = "Federated MEC System Ready";

      setTimeout(() => {
        document.body.classList.add("loaded");
      }, 900);
    }

  }, 20);
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

(function type() {

  const typingElement = document.getElementById("typing");
  if (!typingElement) return;

  if (count === texts.length) count = 0;

  const currentText = texts[count];
  const letter = currentText.slice(0, ++index);

  typingElement.textContent = letter;

  if (letter.length === currentText.length) {
    setTimeout(() => {
      index = 0;
      count++;
    }, 1500);
  }

  setTimeout(type, 80);

})();
