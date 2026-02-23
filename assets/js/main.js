// main.js - loads data/citations.json and populates Publications
document.getElementById('year').textContent = new Date().getFullYear();

// fill profile links found by build-time defaults (can be overridden by data)
const defaults = {
  linkedin: "https://www.linkedin.com/in/aakashjit-bhattacharya-35b405133",
  gscholar: "https://scholar.google.com/citations?user=BLMncXIAAAAJ",
  github: "https://github.com/AakashjitBhattacharya",
  orcid: "https://orcid.org/0000-0003-2188-6245",
  researchgate: "https://www.researchgate.net/profile/Aakashjit-Bhattacharya"
};
document.getElementById('link-linkedin').href = defaults.linkedin;
document.getElementById('link-gscholar').href = defaults.gscholar;
document.getElementById('link-github').href = defaults.github;
document.getElementById('link-orcid').href = defaults.orcid;
document.getElementById('link-researchgate').href = defaults.researchgate;

// load dynamic publications JSON
fetch('data/citations.json').then(r=>{
  if(!r.ok) throw new Error('No citations file');
  return r.json();
}).then(data=>{
  const list = document.getElementById('pub-list');
  const total = data.total_citations || 0;
  document.getElementById('total-citations').textContent = `Total citations: ${total}`;
  list.innerHTML = '';
  (data.publications || []).forEach(pub=>{
    const div = document.createElement('div');
    div.className = 'pub-item';
    div.innerHTML = `<strong>${pub.title}</strong>
      <div><em>${pub.venue || pub.journal || ''}</em> • ${pub.year || ''}</div>
      <div class="muted">Citations: ${pub.citations || 0} • <a href="${pub.link||'#'}" target="_blank">view</a></div>`;
    list.appendChild(div);
  });
}).catch(err=>{
  document.getElementById('pub-list').textContent = 'No publications data found. The citations updater Action may not have run yet.';
});
