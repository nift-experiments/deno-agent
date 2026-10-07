// Standalone OG production phase: same pinned Satori/resvg/Sharp and fonts.
import satori from 'lume/deps/satori.ts';
import sharp from 'npm:sharp@0.34.5';
import {initWasm,Resvg} from 'npm:@resvg/resvg-wasm@2.6.2';
import {toFileUrl} from '@std/path';
const started=performance.now();
await initWasm(await Deno.readFile('publication/vendor/resvg-2.6.2.wasm'));
const all=JSON.parse(await Deno.readTextFile('.generated/og-data.json'));
const selected=Deno.args.flatMap((arg,i)=>arg==='--route'?[Deno.args[i+1]]:[]);
if(!Deno.args.includes('--all') && !selected.length)throw Error('Explicit --route or --all required');
const data=all.filter((row:any)=>Deno.args.includes('--all')||selected.includes(row.route));
if(selected.some(route=>!data.some((row:any)=>row.route===route)))throw Error('Unknown OG route');
const fonts=await Promise.all([
 {name:'Courier',style:'normal',path:'assets/fonts/courier/CourierPrime-Regular.ttf'},
 {name:'Inter',weight:400,style:'normal',path:'assets/fonts/inter/hacked/Inter-Regular-hacked.woff'},
 {name:'Inter',weight:700,style:'normal',path:'assets/fonts/inter/hacked/Inter-SemiBold-hacked.woff'},
].map(async({path,...font})=>({...font,data:(await Deno.readFile(path)).buffer})));
for(const row of data){
 const name=row.openGraphLayout.split('/').at(-1);
 if(!['default.jsx','examples.jsx','cli-commands.jsx'].includes(name))throw Error('Unsupported OG layout: '+name);
 const path=Deno.args.includes('--agent')?'publication/og/'+name.replace('.jsx','.js'):'authored/_includes/open_graph/'+name;
 const template=(await import(toFileUrl(Deno.cwd()+'/'+path).href)).default;
 const svg=await satori(await template(row),{width:1200,height:630,fonts});
 const resvg=new Resvg(svg,{fitTo:{mode:'original'}});const image=resvg.render();
 const png=await sharp(image.asPng()).toBuffer();image.free();resvg.free();
 const dir='assets/og'+row.route;await Deno.mkdir(dir,{recursive:true});
 await Deno.writeFile(dir+'index.png',png);
}
await Deno.writeTextFile('.generated/og-metrics.json',JSON.stringify({og_s:(performance.now()-started)/1000,images:data.length}));
