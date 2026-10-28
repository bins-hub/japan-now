'use strict';
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..'), langs=['en','ja','zh-cn'];
const pages=[];function walk(d){for(const e of fs.readdirSync(d,{withFileTypes:true})){if(e.name==='.git')continue;const p=path.join(d,e.name);if(e.isDirectory())walk(p);else if(e.name==='index.html')pages.push(path.relative(root,p).replaceAll(path.sep,'/'));}}walk(root);
const ko=pages.filter(p=>!langs.some(l=>p.startsWith(l+'/')));
const metrics=[],issues=[];
for(const p of ko){const source=fs.readFileSync(path.join(root,p),'utf8');const core=(source.match(/<h2(?:\s[^>]*)?>/g)||[]).length;for(const lang of langs){const target=lang+'/'+p;if(!pages.includes(target)){issues.push({severity:'missing',page:target,source:p});continue;}const html=fs.readFileSync(path.join(root,target),'utf8');const h2=(html.match(/<h2(?:\s[^>]*)?>/g)||[]).length;const ratio=Number((html.length/Math.max(1,source.length)).toFixed(2));metrics.push({page:target,source:p,sourceBytes:source.length,localeBytes:html.length,ratio,sourceSections:core,localeSections:h2});if(core>=4&&h2<Math.ceil(core/2))issues.push({severity:'thin',page:target,sourceSections:core,localeSections:h2,ratio});if(/(?:Open Korean|韓国語の詳細|韩语详细|Korean source guide)/.test(html))issues.push({severity:'korean-cta',page:target});}}
const summary={checked:metrics.length,missing:issues.filter(x=>x.severity==='missing').length,thin:issues.filter(x=>x.severity==='thin').length,koreanCta:issues.filter(x=>x.severity==='korean-cta').length};
console.log('I18N PARITY AUDIT '+JSON.stringify(summary));for(const issue of issues.slice(0,80))console.log(JSON.stringify(issue));
if(process.env.JP_PARITY_STRICT==='1'&&issues.length)process.exitCode=1;
