(() => {
  'use strict';
  const KEY='academic-theme';
  const root=document.documentElement;
  const systemDark=()=>window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches;
  function apply(pref){const p=['light','dark','system'].includes(pref)?pref:'system';const mode=p==='system'?(systemDark()?'dark':'light'):p;root.dataset.theme=mode;root.dataset.themePreference=p;const s=document.querySelector('[data-theme-select]');if(s)s.value=p;}
  let stored='';try{stored=localStorage.getItem(KEY)||'';}catch(_){ }
  apply(stored||root.dataset.defaultTheme||'system');
  document.addEventListener('change',e=>{if(e.target.matches('[data-theme-select]')){try{localStorage.setItem(KEY,e.target.value);}catch(_){ }apply(e.target.value);}});
  if(window.matchMedia){const q=window.matchMedia('(prefers-color-scheme: dark)');q.addEventListener?.('change',()=>{if((root.dataset.themePreference||'system')==='system')apply('system');});}

  const navToggle=document.querySelector('[data-nav-toggle]');
  const siteNav=document.querySelector('[data-site-nav]');
  navToggle?.addEventListener('click',()=>{const open=navToggle.getAttribute('aria-expanded')==='true';navToggle.setAttribute('aria-expanded',String(!open));siteNav?.classList.toggle('is-open',!open);});

  document.querySelectorAll('[data-publication-index]').forEach(rootEl=>{
    const input=rootEl.querySelector('[data-publication-search]');
    const publicationType=rootEl.querySelector('[data-publication-type]');
    const publicationStatus=rootEl.querySelector('[data-publication-status]');
    const publicationYear=rootEl.querySelector('[data-publication-year]');
    const items=[...rootEl.querySelectorAll('[data-publication]')];
    const filter=()=>{
      const q=(input?.value||'').trim().toLowerCase();
      const type=publicationType?.value||''; const status=publicationStatus?.value||''; const year=publicationYear?.value||'';
      items.forEach(item=>{const text=item.textContent.toLowerCase();item.hidden=Boolean((q&&!text.includes(q))||(type&&item.dataset.type!==type)||(status&&item.dataset.status!==status)||(year&&item.dataset.year!==year));});
    };
    [input,publicationType,publicationStatus,publicationYear].forEach(el=>el?.addEventListener(el===input?'input':'change',filter));
    rootEl.querySelector('[data-publication-clear]')?.addEventListener('click',()=>{if(input)input.value='';if(publicationType)publicationType.value='';if(publicationStatus)publicationStatus.value='';if(publicationYear)publicationYear.value='';filter();});
  });

  async function copyText(text, button){
    try{await navigator.clipboard.writeText(text);const status=button.closest('.citation-tools')?.querySelector('.citation-status');if(status){status.textContent=document.documentElement.lang==='fa'?'کپی شد':'Copied';setTimeout(()=>status.textContent='',1800);}}
    catch(_){const area=document.createElement('textarea');area.value=text;area.hidden=true;document.body.append(area);area.select();document.execCommand('copy');area.remove();}
  }
  document.querySelectorAll('[data-citation-copy]').forEach(button=>button.addEventListener('click',()=>copyText(button.dataset.citation||'',button)));
  function downloadText(button,mime){const blob=new Blob([button.dataset.content||''],{type:mime});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=button.dataset.filename||'citation.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),0);}
  document.querySelectorAll('[data-bibtex]').forEach(button=>button.addEventListener('click',()=>downloadText(button,'application/x-bibtex;charset=utf-8')));
  document.querySelectorAll('[data-ris]').forEach(button=>button.addEventListener('click',()=>downloadText(button,'application/x-research-info-systems;charset=utf-8')));

  document.querySelectorAll('[data-search-root]').forEach(async box=>{const input=box.querySelector('[data-site-search]');const results=box.querySelector('[data-search-results]');let index=[];try{index=await fetch(box.dataset.indexUrl,{cache:'no-store'}).then(r=>r.json());}catch(_){results.textContent=document.documentElement.lang==='fa'?'نمایه جستجو در دسترس نیست.':'Search index unavailable.';return;}const run=()=>{const q=(input.value||'').trim().toLowerCase();results.replaceChildren();if(!q)return;index.filter(x=>(x.title+' '+x.text).toLowerCase().includes(q)).slice(0,30).forEach(x=>{const a=document.createElement('a');a.href=x.url;a.textContent=x.title;const p=document.createElement('p');p.append(a);results.append(p);});};input.addEventListener('input',run);box.querySelector('[data-search-button]')?.addEventListener('click',run);});
})();
