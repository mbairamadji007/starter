#!/usr/bin/env python3
"""Build 44 static HyperFrames sub-compositions from the checked editorial plan.

Images stay local. No remote media, rendering-time clocks or injected narration.
"""
from pathlib import Path
import html,json

ROOT=Path(__file__).resolve().parents[1]
PLAN=json.loads((ROOT/'shot-plan.json').read_text())
OUT=ROOT/'compositions';OUT.mkdir(exist_ok=True)
H=html.escape

ASSETS={
'war':('ancient/01-standard-ur.jpg','étendard d’ur · vers 2550 av. n. è. · domaine public'),
'gold':('ancient/02-ur-headdress.jpg','coiffe d’ur · vers 2600 av. n. è. · the met · domaine public'),
'ziggurat':('ancient/03-ur-ziggurat.jpg','ziggourat d’ur · monument du xxie siècle av. n. è. · domaine public'),
'tablets':('ancient/04-sumerian-tablet-and-tokens.png','tablette : gary todd, cc0 · jetons : marie-lan nguyen, cc by 2.5'),
'cone':('ancient/05-votive-cone.jpg','cône votif · mésopotamie · domaine public'),
'stele':('ancient/06-hammurabi-stele.png','stèle d’hammurabi · xviiie siècle av. n. è. · domaine public'),
'shamash':('ancient/07-shamash-tablet.jpg','shamash · détail de tablette · ixe siècle av. n. è. · cc0'),
'votive':('ancient/08-sumerian-worshiper.jpg','figurine d’orant · mésopotamie · domaine public'),
'divine':('ancient/09-hammurabi-divine-authority.jpg','hammurabi devant shamash · xviiie siècle av. n. è. · erin / flickr · cc by 2.0'),
'tribute':('ancient/10-black-obelisk-tribute.jpg','obélisque noir · vers 825 av. n. è. · domaine public'),
'narmer':('ancient/11-narmer-palette.jpg','palette de narmer · vers 3150–3000 av. n. è. · cc0'),
'persia':('ancient/12-persepolis-tablet.jpg','tablette de persépolis · empire achéménide · domaine public'),
'san':('photos-extra/san_fire.jpg','groupe san · photographie contemporaine d’illustration · cc0'),
'san-art':('photos-extra/san_group_1804.jpg','illustration de 1804 · domaine public · pas une image de la préhistoire'),
'grain':('photos-extra/wheat_sunset.png','céréales · photographie contemporaine d’illustration · cc by 4.0'),
'site':('photos-extra/gobekli_tepe_aerial.png','göbekli tepe · german archaeological institute, e. kücük / plos one · cc by 4.0'),
'jericho':('photos-extra/jericho_tower.png','tour de jéricho · vestige néolithique · domaine public'),
'crown':('photos-extra/silla_gold_crown.jpg','couronne de silla · corée · domaine public · objet d’une autre époque'),
'palace':('photos-extra/palace_ruins.jpg','yuanmingyuan · vestiges d’un palais chinois · domaine public'),
'terraces':('photos-extra/irrigated_terraces.jpg','rizières en terrasses · photographie actuelle d’illustration · cc by 3.0'),
'leaders':('photos-extra/institution_carter_deng.jpg','rencontre carter–deng · 1979 · archives du gouvernement américain · domaine public'),
}
VIDEOS={
'wheat':('wheat-wind-pexels.mp4',0.0,'champ de blé actuel · joshua woroniecki / pexels'),
'river':('river-forest-pexels.mp4',0.5,'rivière forestière actuelle · ruvim m / pexels · illustration'),
'storm':('storm-clouds-pexels.mp4',1.0,'ciel orageux actuel · james cheney / pexels · illustration'),
}
# The same real objects can be revisited in a new framing when the narration returns
# to their function. No photo is represented as footage from antiquity.
EDIT=[
('hero','light',['crown','gold'],None,None,'push'),
('collage','light',['votive','gold'],None,None,'drift'),
('diagram','light',[],None,'institution',None),
('photo','dark',['divine'],None,None,'reveal'),
('video','dark',[],'river',None,None),
('collage','light',['san','san-art'],None,None,'drift'),
('diagram','light',[],None,'nomads',None),
('video','dark',[],'river',None,None),
('statement','light',[],None,'nomads',None),
('collage','red',['grain','site'],None,None,'push'),
('video','dark',[],'wheat',None,None),
('diagram','light',[],None,'stock',None),
('gallery','light',['tablets'],None,None,'reveal'),
('statement','dark',['grain'],None,None,'push'),
('collage','light',['terraces','site'],None,None,'drift'),
('diagram','light',[],None,'village',None),
('gallery','dark',['jericho'],None,None,'push'),
('diagram','light',[],None,'ledger',None),
('diagram','light',[],None,'stock',None),
('photo','light',['cone'],None,None,'drift'),
('diagram','light',[],None,'map',None),
('diagram','dark',[],None,'network',None),
('gallery','dark',['war'],None,None,'reveal'),
('collage','light',['tablets','war'],None,None,'drift'),
('diagram','dark',[],None,'pyramid',None),
('photo','light',['war'],None,None,'push'),
('statement','red',[],None,'dynasty',None),
('collage','light',['stele','votive'],None,None,'drift'),
('photo','dark',['divine'],None,None,'push'),
('collage','light',['shamash','divine'],None,None,'reveal'),
('diagram','light',[],None,'scale',None),
('gallery','dark',['ziggurat'],None,None,'drift'),
('statement','dark',[],None,'cosmos',None),
('collage','light',['stele','tribute'],None,None,'push'),
('diagram','light',[],None,'dynasty',None),
('diagram','dark',[],None,'seat',None),
('diagram','light',[],None,'institution',None),
('video','dark',[],'storm',None,None),
('statement','red',[],None,'institution',None),
('gallery','light',['leaders'],None,None,'drift'),
('gallery','dark',['crown'],None,None,'push'),
('collage','light',['votive','gold'],None,None,'drift'),
('diagram','dark',[],None,'seat',None),
('cta','light',[],None,None,None),
]
assert len(EDIT)==len(PLAN['shots'])
hosts=[];video_hosts=[];final=[]
for n,(shot,edit) in enumerate(zip(PLAN['shots'],EDIT),1):
 sid=shot['id'];start=shot['start'];end=shot['end'];duration=end-start
 layout,theme,images,video,figure,camera=edit
 chapter=next((c for c in PLAN['chapters'] if c['start']<=start<c['end']),PLAN['chapters'][-1])
 title=shot.get('title') or '';subtitle=shot.get('subtitle') or ''
 if n==3: figure='institution'
 if n==6: title='un groupe,\npas un trône'
 if n==13: title=''
 if n==19: title='grain contre travail';subtitle='alliances et dettes'
 if n==20: subtitle='des traces écrites de l’administration'
 if n==28: title='faire accepter le pouvoir'
 if n==32: title=''
 if n==36: title='le rôle demeure'
 if n==38: title='des dieux de l’orage…';subtitle='…à la permanence des institutions'
 if n==40: title='';subtitle=''
 if n==44: subtitle='les détails changent tout'
 kicker='épilogue' if n==44 else f'{chapter["id"]:02d} — {chapter["title"]}'
 # Avoid duplicating a chapter title as both kicker and headline.
 if title.replace('\n',' ')==chapter['title']:kicker=f'chapitre {chapter["id"]:02d}'
 line_html=''.join(f'<span class="title-line">{H(line)}</span>' for line in title.split('\n'))
 copy=f'<div class="copy"><div class="heading-rule" aria-hidden="true"></div><h2 class="headline">{line_html}</h2>'
 if subtitle:copy+=f'<p class="subline">{H(subtitle)}</p>'
 if n==1:copy+='<div class="copy-note">palais, armée, impôts.<br>comment un seul homme en est-il venu à tout incarner ?</div>'
 copy+='</div>'
 media='';captions=[]
 for i,key in enumerate(images):
  path,credit=ASSETS[key];full=ROOT/'assets/media'/path
  if not full.exists():raise FileNotFoundError(full)
  if n==1 and i==0: credit='couronne de silla · objet royal de corée'
  captions.append(credit)
  media+=f'<div class="photo-frame {"secondary" if i else ""}"><img id="{sid}-image-{i}" src="../assets/media/{H(path)}" alt="{H(credit)}"><span class="image-index" aria-hidden="true" data-layout-ignore>{i+1:02d}</span></div>'
 if media:media+=f'<div class="photo-caption">{H(" / ".join(captions))}</div>'
 if figure:media+='<div class="figure-wrap" aria-label="schéma éditorial"></div>'
 if video:
  file,media_start,credit=VIDEOS[video]
  if n==8:media_start=5.5
  video_hosts.append(f'<video id="{sid}-video" class="root-video clip" src="assets/media/video/{file}" data-start="{start:.9f}" data-duration="{duration:.9f}" data-media-start="{media_start}" data-track-index="1" data-fit="cover" muted playsinline preload="auto"></video>')
  media='<div class="video-cover" aria-hidden="true"></div><div class="video-window" aria-hidden="true" style="background:transparent"></div>'+f'<div class="photo-caption">{H(credit)}</div>'
 data={'duration':duration,'figure':figure,'camera':camera,'list':n==14,'cta':n==44}
 surface=f'{layout} theme-{theme}'+(' video-surface' if video else '')
 content=f'''<template>
<div id="{sid}" data-composition-id="{sid}" data-width="1920" data-height="1080" data-duration="{duration:.9f}" style="position:relative;width:100%;height:100%">
<section class="shot-surface {surface}">
<div class="ground-texture" aria-hidden="true" data-layout-ignore></div>
<header class="frame-header"><span><i class="header-dot"></i>une histoire du pouvoir</span><span class="header-right">{chapter['id']:02d} / 09</span></header>
<div class="kicker">{H(kicker)}</div>{copy}{media}
<footer class="frame-footer"><span>qui a inventé les rois ?</span><span class="footer-page">{n:02d} / 44</span></footer>
</section>
</div>
<script>window.DocRuntime.mount({json.dumps(sid)},{json.dumps(data,ensure_ascii=False)});</script>
</template>'''
 (OUT/f'{sid}.html').write_text(content)
 hosts.append(f'<div id="{sid}" class="clip" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{start:.9f}" data-duration="{duration:.9f}" data-track-index="2"></div>')
 final.append({**shot,'actualLayout':layout,'theme':theme,'selectedAssets':images,'selectedVideo':video,'figure':figure,'camera':camera,'displayTitle':title,'displaySubtitle':subtitle})
head='''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>qui a inventé les rois ?</title>
<style>@font-face{font-family:Cormorant;src:url('assets/fonts/CormorantGaramond.ttf') format('truetype');font-weight:300 700;font-style:normal;font-display:block}@font-face{font-family:Manrope;src:url('assets/fonts/Manrope.ttf') format('truetype');font-weight:200 800;font-style:normal;font-display:block}</style>
<link rel="stylesheet" href="styles/film.css"><script src="assets/vendor/gsap.min.js"></script><script src="components/figures.js"></script><script src="scenes/runtime.js"></script></head><body>'''
duration=PLAN['duration']
index=head+f'<div id="royalty-film" data-composition-id="royaute-documentaire" data-width="1920" data-height="1080" data-duration="{duration:.9f}" data-fps="30">'+''.join(video_hosts)+''.join(hosts)+f'<audio id="documentary-sound" src="assets/audio/documentary-master.wav" data-start="0" data-duration="{duration:.9f}" data-track-index="3" data-volume="1" preload="auto"></audio></div>'
index+='''<script>document.fonts.ready.then(()=>{const tl=gsap.timeline({paused:true});window.__timelines=window.__timelines||{};window.__timelines['royaute-documentaire']=tl;tl.seek(0);});</script></body></html>'''
(ROOT/'index.html').write_text(index)
(ROOT/'visual-edit.json').write_text(json.dumps({'duration':duration,'fps':30,'shots':final},ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(hosts)} sub-compositions, {len(video_hosts)} video placements, {duration:.6f} seconds.')
