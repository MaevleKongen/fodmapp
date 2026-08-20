const fs=require('fs'),path=require('path');
const ROOT=path.resolve(__dirname,'..','..','..');
const src=fs.readFileSync(path.join(ROOT,'js','i18n.js'),'utf8');
const load=new Function('localStorage','document',src.replace(/^const /gm,'var ')+'\nreturn {T:T,LANGS:LANGS};');
const {T,LANGS}=load({getItem:()=>null,setItem:()=>{}},{documentElement:{},querySelectorAll:()=>[],getElementById:()=>null,createElement:()=>({})});
module.exports={T,LANGS};
if(require.main===module){
  const keys=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
  const langs=process.argv[3]?process.argv[3].split(','):['en','nb'];
  const out={};
  for(const l of langs){out[l]={};for(const k of keys){out[l][k]=T[l]?T[l][k]:undefined;}}
  console.log(JSON.stringify(out,null,2));
}
