// Loader
window.addEventListener("load", function () {
  document.body.classList.add("loaded");
});

// Load publications
fetch('data/citations.json')
.then(response => response.json())
.then(data => {

  const citationElem = document.getElementById("total-citations");
  if (citationElem) {
    citationElem.textContent = data.total_citations;
  }

  const container = document.getElementById("pub-list");
  if (!container) return;

  container.innerHTML = "";

  data.publications.forEach(pub => {

    const div = document.createElement("div");
    div.className = "card";

    div.innerHTML = `
      <strong>${pub.title}</strong>
      <div>${pub.year || ""}</div>
      <button>Download BibTeX</button>
    `;

    div.querySelector("button").onclick = function() {
      const bib = `
@article{${pub.title.replace(/\s+/g,'')},
  title={${pub.title}},
  year={${pub.year || ""}}
}`;
      const blob = new Blob([bib], { type: "text/plain" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "citation.bib";
      a.click();
    };

    container.appendChild(div);
  });

});
