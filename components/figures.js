/* Original schematic figures for the documentary. No autonomous animation.
 * Each render owns its identifiers; the host timeline animates the marked groups. */
window.DocFigures = (() => {
  const ink = 'var(--ink,#191C1B)';
  const paper = 'var(--paper,#EEE9DE)';
  const gold = 'var(--gold,#B88C50)';
  const accent = 'var(--accent,#934332)';
  const text = (x,y,s,size=27,extra='') => `<text x="${x}" y="${y}" font-size="${size}" ${extra}>${s}</text>`;
  const path = (d,color=ink,extra='') => {
    const width=(extra.match(/stroke-width="([^"]*)"/)||[])[1]||'2';
    const attributes=extra.replace(/\s*stroke-width="[^"]*"/g,'');
    return `<path d="${d}" fill="none" stroke="${color}" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round" class="figure-line" ${attributes}/>`;
  };
  const group = s => `<g class="figure-item">${s}</g>`;
  const marker = (prefix) => `<defs><marker id="${prefix}-arrow" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto" markerUnits="strokeWidth"><path d="M1 1 7 4 1 7" fill="none" stroke="${gold}" stroke-width="1.4"/></marker><linearGradient id="${prefix}-clay" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${gold}" stop-opacity=".5"/><stop offset=".45" stop-color="${gold}" stop-opacity=".24"/><stop offset="1" stop-color="${accent}" stop-opacity=".23"/></linearGradient></defs>`;
  const arrow = (prefix,d,extra='') => path(d,gold,`marker-end="url(#${prefix}-arrow)" ${extra}`);
  const box = (x,y,w,h,extra='') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="3" fill="${paper}" stroke="${ink}" stroke-width="1.5" ${extra}/>`;
  const dot = (x,y,r=7,color=accent,extra='') => `<circle cx="${x}" cy="${y}" r="${r}" fill="${color}" ${extra}/>`;
  function base(type,prefix,body){
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 640" fill="${ink}" role="img" aria-label="${type}" font-family="Manrope, sans-serif" font-weight="500">${marker(prefix)}<g aria-hidden="true" fill="none" stroke="${ink}" stroke-width="1" opacity=".25"><path d="M40 70V40H70M1030 40h30v30M40 570v30h30M1030 600h30v-30"/></g>${body}</svg>`;
  }
  function map(p){
    const body = `
      <g class="figure-item" fill="${gold}" fill-opacity=".07" stroke="${ink}" stroke-opacity=".14" stroke-width="1.5"><path d="M381 56 541 38 672 80 744 158 751 232 808 301 837 381 811 461 862 560 720 590 635 551 546 518 491 454 448 383 394 312 348 226 339 130Z"/></g>
      <g fill="none" stroke="${gold}" stroke-width="5" stroke-linecap="round">
        <path class="figure-line" d="M472 80C412 105 391 140 414 185S469 240 478 286 521 342 550 366 599 396 621 432L688 492"/>
        <path class="figure-line" d="M605 60C629 105 585 131 608 177S635 234 652 286 656 338 683 368 699 428 713 466L688 492C702 522 730 538 760 553"/>
      </g>
      <g class="figure-item"><path d="M730 526 788 541 857 598H670L690 544Z" fill="${gold}" opacity=".13"/>${text(790,576,'golfe',22)}${text(108,130,'mésopotamie',43,'font-weight="650"')}${text(108,172,'la terre entre les fleuves',23,'opacity=".65"')}${text(338,220,'euphrate',24)}${text(660,210,'tigre',24)}${text(476,485,'sumer',26,'letter-spacing="2"')}</g>
      <g class="figure-item figure-focus">${dot(621,432,15,accent,'fill-opacity=".15"')}${dot(621,432,6,accent)}${path('M608 432H459',accent,'stroke-width="1.5"')}<rect x="349" y="399" width="110" height="55" fill="${paper}"/>${text(356,438,'uruk',37,'font-weight="650"')}</g>
      <g class="figure-item" opacity=".62">${text(105,563,'carte schématique',22)}${path('M970 141V81M959 94 970 81 981 94',ink,'stroke-width="1.5"')}${text(970,68,'n',18,'text-anchor="middle"')}</g>`;
    return base('mésopotamie — carte schématique',p,body);
  }
  function stock(p){
    let wheat='';
    for(let i=0;i<7;i++){
      const x=112+i*24;
      wheat += `<path class="figure-line" d="M${x} 383V${230+(i%3)*15}m0 44-13-14m13-5 13-14m-13 51-13-14m13-8 13-14" fill="none" stroke="${gold}" stroke-width="2.5" stroke-linecap="round"/>`;
    }
    let grains='';
    for(let row=0;row<4;row++)for(let col=0;col<6;col++)grains+=`<ellipse cx="${460+col*27}" cy="${250+row*34}" rx="6" ry="12" fill="${gold}" opacity="${.6+(row%2)*.15}"/>`;
    let stores='';
    for(let row=0;row<3;row++)for(let col=0;col<3;col++)stores+=`<rect x="${815+col*54}" y="${240+row*47}" width="45" height="38" rx="2" fill="${gold}" fill-opacity="${.12+row*.07}" stroke="${gold}" stroke-width="1.5"/>`;
    return base('champs, grain et stocks',p,`
      ${group(`${box(75,150,265,285,'stroke-opacity=".3"')}${text(97,194,'01',21,'opacity=".55"')}${wheat}${path('M96 395H317',ink,'opacity=".3"')}`)}
      ${group(`${box(418,150,265,285,'stroke-opacity=".3"')}${text(440,194,'02',21,'opacity=".55"')}${grains}`)}
      ${group(`${box(761,150,265,285,'stroke-opacity=".3"')}${text(783,194,'03',21,'opacity=".55"')}${stores}`)}
      ${arrow(p,'M357 292H399')}${arrow(p,'M700 292H742')}
      ${group(`${text(75,493,'champs',38,'font-weight="650"')}${text(75,537,'une récolte',24,'opacity=".65"')}`)}
      ${group(`${text(418,493,'grain',38,'font-weight="650"')}${text(418,537,'une quantité',24,'opacity=".65"')}`)}
      ${group(`${text(761,493,'stocks',38,'font-weight="650"')}${text(761,537,'une réserve',24,'opacity=".65"')}`)}
    `);
  }
  function ledger(p){
    let marks='';
    for(let row=0;row<6;row++)for(let col=0;col<6;col++){
      const x=129+col*42,y=190+row*43;
      marks+=`<path d="M${x} ${y}l14 4-13 5 2-5Zm8 13 15 3-14 5 2-5Z" fill="${ink}" fill-opacity="${.3+((row+col)%3)*.09}"/>`;
    }
    return base('compter et organiser — schéma',p,`
      ${group(`<rect x="82" y="113" width="366" height="394" rx="34" fill="url(#${p}-clay)" stroke="${gold}" stroke-width="2"/><path d="M108 150Q268 123 423 150M109 470Q266 494 420 469" fill="none" stroke="${gold}" stroke-opacity=".35" stroke-width="1.5"/>${marks}${text(266,553,'tablette comptable',26,'text-anchor="middle"')}`)}
      ${arrow(p,'M471 300H531')}
      ${group(`${text(571,152,'noter. compter.',40,'font-weight="650"')}${text(571,197,'organiser.',40,'font-weight="650"')}${path('M568 233H1004',ink,'opacity=".5"')}`)}
      ${group(`${text(571,282,'entrée',25)}<rect x="747" y="260" width="215" height="24" fill="${gold}" fill-opacity=".68"/>${path('M568 307H1004',ink,'opacity=".18"')}`)}
      ${group(`${text(571,356,'sortie',25)}<rect x="747" y="334" width="120" height="24" fill="${accent}" fill-opacity=".63"/>${path('M568 381H1004',ink,'opacity=".18"')}`)}
      ${group(`${text(571,430,'solde',25,'font-weight="650"')}<rect x="747" y="408" width="95" height="24" fill="${ink}" fill-opacity=".8"/>${path('M568 455H1004',ink,'opacity=".5"')}`)}
      ${group(`${text(571,519,'grain · travail · dette',25,'fill="'+accent+'"')}${text(571,560,'exemple schématique',21,'opacity=".55"')}`)}
    `);
  }
  function pyramid(p){
    return base('la hiérarchie du pouvoir',p,`
      <g fill="none" stroke="${ink}" stroke-width="1.6" opacity=".2"><path d="M550 74V548M221 536H883"/></g>
      ${group(`<path d="M550 101 643 231H457Z" fill="${accent}" fill-opacity=".2" stroke="${accent}" stroke-width="2" class="figure-line"/>${text(550,196,'pouvoir',31,'text-anchor="middle" font-weight="650"')}`)}
      ${group(`<path d="M457 231H643L736 361H364Z" fill="${gold}" fill-opacity=".16" stroke="${gold}" stroke-width="1.8" class="figure-line"/>${text(550,312,'administration',29,'text-anchor="middle"')}`)}
      ${group(`<path d="M364 361H736L850 521H250Z" fill="${gold}" fill-opacity=".06" stroke="${ink}" stroke-width="1.7" class="figure-line"/>${text(550,454,'communauté',34,'text-anchor="middle"')}`)}
      ${group(`${text(84,192,'ordonner',24,'fill="'+accent+'"')}${path('M237 185H420',accent,'opacity=".6"')}${dot(426,185,4,accent)}`)}
      ${group(`${path('M762 305H838',gold,'opacity=".8"')}${text(858,314,'coordonner',23)}`)}
      ${group(`${path('M874 451H931',gold,'opacity=".8"')}${text(946,460,'protéger',22,'text-anchor="start"')}`)}
      ${group(`${text(550,581,'un sommet à justifier',26,'text-anchor="middle" fill="'+accent+'"')}`)}
    `);
  }
  function dynasty(p){
    const person=(x,caption,focus=false)=>`<g class="figure-item${focus?' figure-focus':''}">${dot(x,130,27,focus?accent:ink,'fill-opacity=".83"')}${path(`M${x-47} 222Q${x-45} 168 ${x} 168T${x+47} 222`,focus?accent:ink,'stroke-width="3"')}${text(x,267,caption,23,'text-anchor="middle"')}${path(`M${x} 287V330`,gold,'stroke-dasharray="4 7"')}</g>`;
    return base('la transmission de l’institution',p,`
      ${person(210,'un dirigeant',true)}${person(550,'son successeur')}${person(890,'la génération suivante')}
      ${arrow(p,'M289 166H463')}${arrow(p,'M629 166H803')}
      ${group(`<rect x="110" y="330" width="880" height="112" rx="3" fill="${gold}" fill-opacity=".11" stroke="${ink}" stroke-width="2"/>${text(550,401,'l’institution',46,'font-weight="650" text-anchor="middle"')}`)}
      ${arrow(p,'M120 503H979')}
      ${group(`${text(550,555,'les personnes passent. le rôle demeure.',30,'text-anchor="middle"')}`)}
    `);
  }
  function network(p){
    const node=(x,y,word,sub,n)=>group(`${box(x,y,266,124,'stroke-opacity=".55"')}${text(x+21,y+29,n,17,'opacity=".45"')}${text(x+133,y+69,word,36,'text-anchor="middle" font-weight="650"')}${text(x+133,y+102,sub,22,'text-anchor="middle" opacity=".65"')}`);
    return base('coordonner la cité',p,`
      ${path('M336 156C398 156 418 247 458 264',gold,'stroke-width="2"')}${path('M764 156C702 156 682 247 642 264',gold,'stroke-width="2"')}
      ${path('M336 461C398 461 418 374 458 358',gold,'stroke-width="2"')}${path('M764 461C702 461 682 374 642 358',gold,'stroke-width="2"')}
      ${node(70,94,'eau','répartir','01')}${node(764,94,'rations','nourrir','02')}${node(70,399,'conflits','arbitrer','03')}${node(764,399,'défense','protéger','04')}
      ${group(`<circle cx="550" cy="311" r="116" fill="${paper}" stroke="${accent}" stroke-width="2.2"/><circle cx="550" cy="311" r="102" fill="none" stroke="${accent}" stroke-opacity=".23"/>${text(550,323,'coordonner',35,'text-anchor="middle" font-weight="650" fill="'+accent+'"')}`)}
      ${group(`${text(550,582,'une organisation permanente',27,'text-anchor="middle"')}`)}
    `);
  }
  function nomads(p){
    const clan=(x,n,caption)=>group(`<circle cx="${x}" cy="293" r="100" fill="${gold}" fill-opacity=".05" stroke="${ink}" stroke-opacity=".45" stroke-width="1.5"/>${dot(x,256,16,ink)}${dot(x-29,290,14,ink)}${dot(x+29,290,14,ink)}${path(`M${x-22} 322Q${x} 288 ${x+22} 322M${x-54} 343Q${x-29} 310 ${x-7} 343M${x+7} 343Q${x+29} 310 ${x+54} 343`,ink,'stroke-width="2.2"')}${text(x,434,caption,27,'text-anchor="middle"')}${text(x,173,n,20,'text-anchor="middle" opacity=".5"')}`);
    return base('la possibilité de partir',p,`
      ${clan(200,'01','un groupe')}${clan(550,'02','un déplacement')}${clan(900,'03','un autre lieu')}
      ${arrow(p,'M318 293H431','stroke-dasharray="6 9"')}${arrow(p,'M668 293H781','stroke-dasharray="6 9"')}
      ${group(`${text(550,94,'rester ou partir',41,'text-anchor="middle" font-weight="650"')}${text(550,556,'la possibilité de choisir',29,'text-anchor="middle" fill="'+accent+'"')}`)}
    `);
  }
  function institution(p){
    const column=(x,word,n)=>group(`<rect x="${x-55}" y="272" width="110" height="197" rx="2" fill="${gold}" fill-opacity=".08" stroke="${ink}" stroke-width="1.7"/><path class="figure-line" d="M${x-68} 269H${x+68}M${x-68} 476H${x+68}" fill="none" stroke="${ink}" stroke-width="3"/><path d="M${x-19} 291V448M${x+19} 291V448" fill="none" stroke="${ink}" stroke-opacity=".16" stroke-width="1"/>${text(x,329,n,19,'text-anchor="middle" opacity=".55"')}${text(x,402,word,31,'text-anchor="middle" font-weight="650"')}`);
    return base('la continuité des institutions',p,`
      ${group(`<path d="M135 168 550 80 965 168V229H135Z" fill="${gold}" fill-opacity=".1" stroke="${ink}" stroke-width="2" class="figure-line"/>${text(550,192,'une organisation durable',37,'text-anchor="middle" font-weight="650"')}`)}
      ${column(280,'lois','01')}${column(550,'impôts','02')}${column(820,'armée','03')}
      ${group(`<path class="figure-line" d="M132 496H968V517H132Z" fill="${ink}" fill-opacity=".06" stroke="${ink}" stroke-width="1.8"/>${text(550,577,'les personnes changent. la structure reste.',27,'text-anchor="middle"')}`)}
    `);
  }
  function village(p){
    let fields='';
    for(let row=0;row<3;row++)for(let col=0;col<3;col++){
      const x=143+col*62,y=178+row*54;
      fields+=`<rect x="${x}" y="${y}" width="48" height="39" fill="${gold}" fill-opacity=".1" stroke="${gold}" stroke-width="1.3"/><path d="M${x+12} ${y+5}v29m12-29v29m12-29v29" fill="none" stroke="${gold}" stroke-opacity=".55" stroke-width="1"/>`;
    }
    let homes='';
    for(let row=0;row<2;row++)for(let col=0;col<3;col++){
      const x=643+col*82,y=190+row*100;
      homes+=`<path d="M${x} ${y+22}  ${x+28} ${y} ${x+56} ${y+22}v44h-56Z" fill="${paper}" stroke="${ink}" stroke-width="1.8"/><path d="M${x+22} ${y+66}v-24h13v24" fill="none" stroke="${gold}" stroke-width="1.3"/>`;
    }
    return base('village — organisation schématique',p,`
      ${group(`<path d="M105 142H371V373H105Z" fill="${gold}" fill-opacity=".035" stroke="${ink}" stroke-opacity=".28" stroke-width="1.3"/>${fields}${text(237,418,'champs',31,'text-anchor="middle"')}`)}
      ${group(`${homes}${text(754,418,'maisons',31,'text-anchor="middle"')}`)}
      ${group(`<circle cx="490" cy="389" r="62" fill="${gold}" fill-opacity=".13" stroke="${gold}" stroke-width="1.8"/><path d="M459 388h62m-52-15h42m-40 30h38" fill="none" stroke="${gold}" stroke-width="3"/>${text(490,493,'réserve',29,'text-anchor="middle"')}`)}
      ${path('M378 263C427 263 433 331 452 344M552 361C604 361 597 276 636 270',gold,'stroke-dasharray="5 8"')}
      ${arrow(p,'M784 166C844 136 905 120 981 118','stroke-dasharray="5 8"')}
      ${group(`${text(915,91,'partir',25,'text-anchor="middle" fill="'+accent+'"')}${text(550,576,'organisation schématique du village',24,'text-anchor="middle" opacity=".7"')}`)}
    `);
  }
  function cosmos(p){
    let rays='';
    for(let i=0;i<12;i++){
      const a=i*Math.PI/6;
      const x1=(550+117*Math.cos(a)).toFixed(2),y1=(320+117*Math.sin(a)).toFixed(2);
      const x2=(550+215*Math.cos(a)).toFixed(2),y2=(320+215*Math.sin(a)).toFixed(2);
      rays+=path(`M${x1} ${y1}L${x2} ${y2}`,gold,'stroke-opacity=".62" stroke-width="1.5"');
    }
    return base('l’ordre — représentation symbolique',p,`
      <g class="figure-item" fill="none" stroke="${gold}"><circle cx="550" cy="320" r="215" stroke-width="1.7"/><circle cx="550" cy="320" r="182" stroke-width="1" stroke-dasharray="3 10" stroke-opacity=".55"/><circle cx="550" cy="320" r="118" stroke-width="1.3" stroke-opacity=".4"/></g>
      ${rays}
      ${group(`<circle cx="550" cy="320" r="98" fill="${paper}" stroke="${accent}" stroke-width="2.1"/>${text(550,335,'ordre',43,'text-anchor="middle" font-weight="650" fill="'+accent+'"')}`)}
      ${group(`${dot(550,105,7,gold)}${text(550,77,'les dieux',26,'text-anchor="middle"')}`)}
      ${group(`${dot(765,320,7,gold)}${text(805,329,'le souverain',25)}`)}
      ${group(`${dot(335,320,7,gold)}${text(294,329,'les rites',25,'text-anchor="end"')}`)}
      ${group(`${dot(550,535,7,gold)}${text(550,580,'représentation symbolique',23,'text-anchor="middle" opacity=".65"')}`)}
    `);
  }
  function seat(p){
    return base('le siège et la personne',p,`
      ${group(`<rect x="414" y="119" width="272" height="302" rx="4" fill="${gold}" fill-opacity=".04" stroke="${ink}" stroke-width="2.3"/><path d="M438 143H662V397H438Z" fill="none" stroke="${gold}" stroke-width="1.3"/><path class="figure-line" d="M382 390v52h336v-52M398 444V512M702 444V512M382 442H718" fill="none" stroke="${ink}" stroke-width="3" stroke-linecap="round"/><path d="M394 453H706" fill="none" stroke="${gold}" stroke-width="7" stroke-opacity=".45"/>`)}
      <g class="figure-item figure-focus">${dot(550,227,35,accent,'fill-opacity=".9"')}<path d="M493 387v-58c0-38 19-59 57-59s57 21 57 59v58Z" fill="${accent}" fill-opacity=".66"/><path d="M501 348 467 391M599 348l34 43" fill="none" stroke="${accent}" stroke-width="12" stroke-linecap="round"/></g>
      ${group(`${path('M700 194H852',gold,'stroke-width="1.3"')}${text(875,202,'la fonction',25)}${text(550,574,'le siège demeure',34,'text-anchor="middle" font-weight="650"')}`)}
    `);
  }
  function scale(p){
    const small=x=>`<g class="figure-item">${dot(x,362,16,ink,'fill-opacity=".65"')}<path d="M${x-23} 456v-42c0-21 7-31 23-31s23 10 23 31v42Z" fill="${ink}" fill-opacity=".48"/></g>`;
    return base('mise à l’échelle symbolique',p,`
      ${path('M136 463H1000',ink,'stroke-opacity=".28" stroke-width="1.3"')}
      <g class="figure-item figure-focus">${dot(359,192,47,accent,'fill-opacity=".85"')}<path d="M285 456V332c0-58 25-87 74-87s74 29 74 87v124Z" fill="${accent}" fill-opacity=".5"/><path d="M295 333 259 401M423 333l36 68" fill="none" stroke="${accent}" stroke-width="15" stroke-linecap="round"/></g>
      ${small(740)}${small(823)}${small(906)}
      ${group(`${text(359,511,'le souverain',28,'text-anchor="middle" font-weight="650"')}${text(823,511,'les autres',28,'text-anchor="middle"')}${text(550,579,'mise à l’échelle symbolique',24,'text-anchor="middle" opacity=".67"')}`)}
    `);
  }
  const figures={map,stock,ledger,pyramid,dynasty,network,nomads,institution,village,cosmos,seat,scale};
  return {
    render(type,prefix='figure'){
      const safe=String(prefix).replace(/[^a-zA-Z0-9_-]/g,'-');
      return (figures[type]||figures.institution)(safe);
    },
    types:Object.freeze(Object.keys(figures))
  };
})();
