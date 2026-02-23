fetch('data/citations.json')
.then(response => response.json())
.then(data => {

  document.getElementById("total-citations").textContent = data.total_citations;

  const container = document.getElementById("pub-list");
  container.innerHTML = "";

  data.publications.forEach(pub => {

    const div = document.createElement("div");
    div.className = "pub-item";

    const title = document.createElement("strong");
    title.textContent = pub.title;

    const meta = document.createElement("div");
    meta.textContent = pub.year;

    const btn = document.createElement("button");
    btn.textContent = "Download BibTeX";

    btn.onclick = function() {
      const bib = `
@article{${pub.title.replace(/\s+/g,'')},
  title={${pub.title}},
  year={${pub.year}}
}`;
      const blob = new Blob([bib], { type: "text/plain" });
      const url = URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = "citation.bib";
      a.click();
    };

    div.appendChild(title);
    div.appendChild(meta);
    div.appendChild(btn);

    container.appendChild(div);
  });

});
