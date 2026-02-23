// Load shared navbar
fetch("assets/components/navbar.html")
  .then(response => response.text())
  .then(data => {
    document.getElementById("navbar").innerHTML = data;
  });

// Load shared footer
fetch("assets/components/footer.html")
  .then(response => response.text())
  .then(data => {
    document.getElementById("footer").innerHTML = data;
    document.getElementById("current-year").textContent =
      new Date().getFullYear();
  });
// Load shared loader
fetch("assets/components/loader.html")
  .then(response => response.text())
  .then(data => {
    document.getElementById("loader-container").innerHTML = data;

    startLoader();  // start animation after injection
  });

// Typing Animation
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
