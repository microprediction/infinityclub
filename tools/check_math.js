// Checks every \\( \\) and \\[ \\] for KaTeX errors, exercise/answer counts, tag balance and house style.
// Run: (cd tools && npm install) then node tools/check_math.js   (exit code 1 on any issue)
const fs=require('fs'), path=require('path'), katex=require('katex');
const R=path.resolve(__dirname,'..'); let out=[];
function walk(d){return fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>e.isDirectory()?(/^(grade-\d+|sheets|demos)$/.test(e.name)||d!==R?walk(path.join(d,e.name)):[]):e.name.endsWith('.html')?[path.join(d,e.name)]:[]);}
const dec=s=>s.replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&').replace(/&quot;/g,'"').replace(/&#x27;|&#39;/g,"'");
for(const f of walk(R)){ const t=fs.readFileSync(f,'utf8'), rel=f.slice(R.length+1);
  const body=t.replace(/<script[\s\S]*?<\/script>/g,'').replace(/<svg[\s\S]*?<\/svg>/g,'').replace(/<style[\s\S]*?<\/style>/g,'');
  let n=0; const re=/\\\(([\s\S]*?)\\\)|\\\[([\s\S]*?)\\\]/g; let m;
  while((m=re.exec(body))){ n++; const src=dec(m[1]!==undefined?m[1]:m[2]);
    if(/<[a-zA-Z\/]/.test(src)) out.push(`HTML-IN-MATH ${rel}: ${src.slice(0,70)}`);
    try{katex.renderToString(src,{throwOnError:true,displayMode:m[2]!==undefined});}catch(e){out.push(`KATEX ${rel}: ${String(e.message).slice(0,90)} :: ${src.slice(0,60)}`);} }
  if(/\\\(|\\\[/.test(body.replace(re,''))) out.push(`UNBALANCED ${rel}`);
  if(/grade-\d+\/sheets\//.test(rel)){
    const ex=(t.match(/<section class="exercises"[\s\S]*?<\/section>/)||[''])[0], an=(t.match(/<section class="answers"[\s\S]*?<\/section>/)||[''])[0];
    const top=s=>{const ol=(s.match(/<ol[\s\S]*<\/ol>/)||[''])[0]; let d=0,c=0; ol.replace(/<(\/?)(ol|ul|li)\b/g,(_,cl,tag)=>{ if(tag==='li'){ if(!cl&&d===1)c++; } else d+=cl?-1:1; }); return c;};
    const a=top(ex), b=top(an); if(a!==b) out.push(`EX/ANS ${rel}: ${a} exercises, ${b} answers`);
    if(!/<b>Stretch\.?<\/b>/.test(an)) out.push(`NO-STRETCH-ANSWER ${rel}`);
    if(/!/.test(body.replace(/<[^>]+>/g,' ').replace(re,'').replace(/\d!|[a-z)]!/g,''))) out.push(`EXCLAM ${rel}`);
    const ids=[...t.matchAll(/\sid="([^"]+)"/g)].map(x=>x[1]); const dup=ids.filter((x,i)=>ids.indexOf(x)!==i); if(dup.length) out.push(`DUP-ID ${rel}: ${dup[0]}`);
    if((t.match(/<figure/g)||[]).length!==(t.match(/<\/figure>/g)||[]).length) out.push(`FIGURE-TAGS ${rel}`);
    for(const tag of ['section','ol','ul','li','p','div','table','figure']){const o=(t.match(new RegExp('<'+tag+'[\\s>]','g'))||[]).length,c=(t.match(new RegExp('</'+tag+'>','g'))||[]).length; if(o!==c) out.push(`TAGS ${rel}: <${tag}> ${o} open ${c} close`);}
  }
  if(/\bmaths\b/i.test(t)) out.push(`MATHS ${rel}`);
  if(/\bbright (kids|children|\d|grade)/i.test(t)) out.push(`BRIGHT ${rel}`);
}
console.log(out.join('\n')); console.log('issues',out.length); process.exitCode=out.length?1:0;
