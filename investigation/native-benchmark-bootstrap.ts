// Frozen delivery of two pinned WASM dependencies; original CLI/config, engines,
// compilation count and worker lifetime remain unchanged. Initialization stays timed.
const resvgURL='https://cdn.jsdelivr.net/npm/@resvg/resvg-wasm@2.6.2/index_bg.wasm';
const esbuildURL='https://cdn.jsdelivr.net/gh/esbuild/deno-esbuild@0.27.0/esbuild.wasm';
const assets=new Map<string,string>();
for(const [url,file]of [[resvgURL,'resvg-2.6.2.wasm'],[esbuildURL,'esbuild-0.27.0.wasm']]){
 assets.set(url,URL.createObjectURL(new Blob([await Deno.readFile(new URL('./tools/native-wasm/'+file,import.meta.url))],{type:'application/wasm'})));
}
const upstreamFetch=globalThis.fetch.bind(globalThis);
globalThis.fetch=async(input,init)=>{
 const url=input instanceof Request?input.url:String(input);
 return await upstreamFetch(assets.get(url)??input,init);
};
const UpstreamWorker=globalThis.Worker;
globalThis.Worker=class extends UpstreamWorker{
 postMessage(message:any,options?:any){super.postMessage(typeof message==='string'&&assets.has(message)?assets.get(message):message,options);}
};
await import('lume/cli.ts');
