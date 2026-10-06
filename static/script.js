const icons={Images:"🖼️",Documents:"📄",PDFs:"📕",Videos:"🎬",Audio:"🎵",Archives:"🗜️",Code:"💻",Others:"📦"};

function renderStats(s){
  document.getElementById("total").textContent=s.Total;
  document.getElementById("images").textContent=s.Images;
  document.getElementById("documents").textContent=s.Documents;
  document.getElementById("code").textContent=s.Code;
  const box=document.getElementById("categories");
  box.innerHTML="";
  Object.entries(s).filter(([k])=>k!=="Total").forEach(([k,v])=>{
    box.innerHTML += `<div class="cat"><b>${icons[k]||"📁"} ${k}</b><span>${v}</span></div>`;
  });
}
async function refresh(){
  const s=await fetch("/stats").then(r=>r.json());
  renderStats(s);
}
document.getElementById("organizeBtn").onclick=async()=>{
  const btn=document.getElementById("organizeBtn"), status=document.getElementById("status");
  btn.disabled=true; btn.textContent="Organizing...";
  const data=await fetch("/organize",{method:"POST"}).then(r=>r.json());
  status.textContent=`✓ Successfully organized ${data.count} file(s) in the local demo folder.`;
  renderStats(data.stats);
  btn.textContent="⚡ Organize Demo Folder"; btn.disabled=false;
};
document.getElementById("search").addEventListener("input",async e=>{
  const q=e.target.value.trim(), box=document.getElementById("results");
  if(!q){box.innerHTML='<div class="empty">Type a filename above to search.</div>';return;}
  const data=await fetch("/search?q="+encodeURIComponent(q)).then(r=>r.json());
  box.innerHTML=data.results.length ? data.results.map(x=>`<div class="result">📄 ${x}</div>`).join("") : '<div class="empty">No matching files found.</div>';
});
refresh();