/* Deterministic shot animation. HyperFrames owns all picture and media time. */
window.DocRuntime={mount(id,data){
  document.fonts.ready.then(()=>{
    const root=document.querySelector(`[data-composition-id="${id}"]`);
    const q=selector=>Array.from(root.querySelectorAll(selector));
    const frame=root.querySelector('.figure-wrap');
    if(frame && data.figure)frame.innerHTML=window.DocFigures.render(data.figure,id);
    const tl=gsap.timeline({paused:true,defaults:{ease:'power3.out'}});
    // One actual DOM node per tween also works through the renderer's GSAP proxy.
    const fromTo=(nodes,from,vars,at)=>{
      const {stagger=0,...to}=vars;
      nodes.forEach((node,i)=>tl.fromTo(node,from,to,at+i*stagger));
    };
    const toElements=(nodes,vars,at)=>nodes.forEach(node=>tl.to(node,vars,at));
    const duration=data.duration;
    fromTo(q('.heading-rule'),{scaleX:0},{scaleX:1,duration:.5,ease:'power4.out'},.08);
    fromTo(q('.kicker'),{y:12,opacity:0},{y:0,opacity:1,duration:.4},.1);
    fromTo(q('.title-line'),{y:24,rotationX:-7,opacity:0},{y:0,rotationX:0,opacity:1,duration:.65,stagger:data.list?.4:.12,ease:'power4.out'},.12);
    fromTo(q('.subline'),{y:17,opacity:0},{y:0,opacity:1,duration:.5},Math.min(1.0,duration*.23));
    fromTo(q('.copy-note'),{y:12,opacity:0},{y:0,opacity:1,duration:.42},duration*.48);
    const pictures=q('.photo-frame');
    pictures.forEach((picture,i)=>{
      const at=i?duration*.43:.06;
      tl.fromTo(picture,{x:i?-32:34,y:i?34:8,scale:i?.96:1,opacity:0},{x:0,y:0,scale:1,opacity:1,duration:.72,ease:'power4.out'},at);
      const img=picture.querySelector('img');
      if(img){
        if(data.camera==='reveal'){
          tl.fromTo(picture,{clipPath:'inset(0% 100% 0% 0%)'},{clipPath:'inset(0% 0% 0% 0%)',duration:.82,ease:'power3.inOut'},at);
          tl.fromTo(img,{x:-12,scale:1.02},{x:12,scale:1.02,duration:duration-at,ease:'none'},at);
        }else if(data.camera==='push'){
          tl.fromTo(img,{scale:1.005},{scale:1.055,duration:duration-at,ease:'sine.inOut'},at);
        }else if(data.camera==='drift'){
          tl.fromTo(img,{x:-16,scale:1.035},{x:16,scale:1.035,duration:duration-at,ease:'sine.inOut'},at);
        }
      }
    });
    fromTo(q('.photo-caption'),{y:8,opacity:0},{y:0,opacity:1,duration:.4},duration*.56);
    const items=q('.figure-item');
    items.forEach((item,i)=>{
      const at=.38+(i%12)*Math.min(.18,duration*.032);
      tl.fromTo(item,{y:13,opacity:0},{y:0,opacity:1,duration:.52,ease:'power3.out'},at);
    });
    q('.figure-line').forEach((line,i)=>{
      if(typeof line.getTotalLength!=='function')return;
      let length=0;try{length=line.getTotalLength();}catch{}
      if(!length || length>20000)return;
      tl.fromTo(line,{strokeDasharray:length,strokeDashoffset:length},{strokeDashoffset:0,duration:Math.min(1.1,duration*.22),ease:'power2.inOut'},.35+(i%8)*.11);
    });
    if(data.figure==='seat'){
      toElements(q('.figure-focus'),{opacity:0,y:-10,duration:.8,ease:'power2.inOut'},duration*.52);
    }else if(data.figure==='map'){
      fromTo(q('.figure-focus'),{scale:.85,transformOrigin:'50% 50%'},{scale:1,duration:.42,stagger:.08,ease:'back.out(1.5)'},duration*.57);
    }else if(data.figure==='cosmos'){
      tl.fromTo(frame,{rotation:-3,scale:.98},{rotation:0,scale:1,duration:duration,ease:'sine.inOut'},0);
    }
    // The final message is fully settled before the original spoken CTA.
    if(data.cta)fromTo(q('.headline'),{scale:.985},{scale:1,duration:.65,ease:'power3.out'},.15);
    window.__timelines=window.__timelines||{};
    window.__timelines[id]=tl;
    tl.seek(0);
  });
}};
