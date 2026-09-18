const {chromium}=require('playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
 for (const [tag,vp] of [['d',{width:1440,height:900}],['m',{width:390,height:844}]]){
  const p=await (await b.newContext({viewport:vp,deviceScaleFactor:tag=='d'?1.5:2})).newPage();
  for (const path of ['info','home']){
   await p.goto('https://oonaschweikhardt.cargo.site/'+path,{waitUntil:'networkidle'});
   await p.addStyleTag({content:'*{color:transparent!important;border-color:transparent!important} .page-content,.page-content *{visibility:hidden!important;background:transparent!important} [id="N1079376802"] *{background:transparent!important}'});
   await p.waitForTimeout(5000);
   const n= path=='home'?14:1;
   for(let i=0;i<n;i++){ await p.screenshot({path:`bdf/${tag}-${path}-${String(i).padStart(2,'0')}.png`}); await p.waitForTimeout(3300); }
  }
 }
 await b.close();
})();
