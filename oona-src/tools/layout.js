const {chromium}=require('playwright');
const pages=['archive','info','home','page-1','page-2','page-3','page-4','page-5','page-6','page-7'];
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
 const res={};
 for (const [tag,vp] of [['d',{width:1440,height:900}],['m',{width:390,height:844}]]){
  const p=await (await b.newContext({viewport:vp})).newPage();
  for (const path of pages){
   await p.goto('https://oonaschweikhardt.cargo.site/'+path,{waitUntil:'networkidle',timeout:90000}).catch(()=>{});
   await p.waitForTimeout(1500);
   const r=await p.evaluate(()=>{
     const out=[];
     const gals=[...document.querySelectorAll('gallery-justify,gallery-columnized,gallery-freeform,gallery-grid,gallery-slideshow')];
     for (const g of gals){
       const gr=g.getBoundingClientRect();
       const items=[...g.querySelectorAll(':scope > media-item')].map(m=>{const r=m.getBoundingClientRect();return {hash:m.getAttribute('hash'),x:(r.left-gr.left)/gr.width*100,y:(r.top-gr.top)/gr.width*100,w:r.width/gr.width*100,h:r.height/gr.width*100}});
       out.push({tag:g.tagName.toLowerCase(),w:gr.width,hRatio:gr.height/gr.width*100,items});
     }
     const solo=[...document.querySelectorAll('media-item')].filter(m=>!m.parentElement.tagName.startsWith('GALLERY')).map(m=>{const r=m.getBoundingClientRect();const pr=m.parentElement.getBoundingClientRect();return {hash:m.getAttribute('hash'),w:r.width,pw:pr.width,h:r.height}});
     const pc=[...document.querySelectorAll('.page-content')].map(e=>{const r=e.getBoundingClientRect();return {w:r.width,h:r.height,y:r.top}});
     return {gals:out,solo,pc,docH:document.documentElement.scrollHeight};
   });
   res[tag+':'+path]=r;
  }
 }
 require('fs').writeFileSync('layout.json',JSON.stringify(res,null,1));
 await b.close();
})();
