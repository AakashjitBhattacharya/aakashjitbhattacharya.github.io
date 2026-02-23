/* =========================
   INITIAL LOAD
========================= */

document.addEventListener("DOMContentLoaded", function () {

  loadNavbar();
  loadFooter();

  const hasVisited = sessionStorage.getItem("hasVisited");

  if (!hasVisited) {
    showLoader(null);
    sessionStorage.setItem("hasVisited", "true");
  } else {
    document.body.classList.add("loaded");
  }

  enablePageTransitions();
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
   LOADER DISPLAY HANDLER
========================= */

function showLoader(callback) {

  fetch("assets/components/loader.html")
    .then(res => res.text())
    .then(data => {

      const container = document.getElementById("loader-container");
      if (!container) return;

      container.innerHTML = data;
      document.body.classList.remove("loaded");

      startLoader(callback);
    })
    .catch(() => {
      document.body.classList.add("loaded");
      if (callback) callback();
    });
}


/* =========================
   ADVANCED MEC LOADER
========================= */

function startLoader(callback) {

  let percent = 0;

  const percentElement = document.getElementById("load-percent");
  const statusText = document.getElementById("status-text");

  const cloud = document.querySelector(".cloud-node");
  const mecStations = document.querySelectorAll(".mec-station");

  const interval = setInterval(() => {

    percent++;

    if (percentElement)
      percentElement.textContent = percent;

    if (percent === 20) {
      if (statusText)
        statusText.textContent = "Activating MEC Base Stations...";
      mecStations.forEach(station => station.classList.add("active"));
    }

    if (percent === 60) {
      if (statusText)
        statusText.textContent = "Establishing MEC–Cloud Communication...";
    }

    if (percent === 85) {
      if (statusText)
        statusText.textContent = "Scaling Cloud Core...";
      if (cloud)
        cloud.classList.add("active");
    }

    if (percent >= 100) {
      clearInterval(interval);

      if (statusText)
        statusText.textContent = "Federated MEC System Ready";

      setTimeout(() => {

        document.body.classList.add("loaded");

        if (callback)
          callback();

      }, 500);
    }

  }, 20);
}


/* =========================
   PAGE TRANSITION CONTROL
========================= */

function enablePageTransitions() {

  document.addEventListener("click", function (e) {

    const link = e.target.closest("a");
    if (!link) return;

    const url = link.getAttribute("href");

    if (!url) return;

    // Ignore external links, anchors, mail, tel
    if (
      url.startsWith("http") ||
      url.startsWith("#") ||
      url.startsWith("mailto:") ||
      url.startsWith("tel:")
    ) {
      return;
    }

    e.preventDefault();

    showLoader(function () {
      window.location.href = url;
    });

  });
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
