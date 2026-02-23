// Load shared navbar
fetch("/assets/components/navbar.html")
  .then(response => response.text())
  .then(data => {
    document.getElementById("navbar").innerHTML = data;
  });
// Loader
window.addEventListener("load", function () {
  document.body.classList.add("loaded");
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
