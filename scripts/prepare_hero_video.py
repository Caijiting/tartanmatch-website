"""Compose eight audited matching groups from tartanmatch_talk_finalized.pptx.

Slides 1, 81 and 82. Each group retains the existing 2 × 2 layout:
    source input       target input
    target → source    source → target
Media filenames and directions are explicit because slide 81 reverses input order.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import zipfile, subprocess, imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'; WORK=ROOT/'.work'; MEDIA=WORK/'finalized'
MEDIA.mkdir(parents=True,exist_ok=True)
FFMPEG=imageio_ffmpeg.get_ffmpeg_exe()
# label, category, slide, source, target, target-to-source, source-to-target
PAIRS=[
 ('Depth ↔ Depth','SAME MODALITY',1,'image1.png','image2.png','image3.gif','image4.gif'),
 ('Depth ↔ Depth · sparse','SAME MODALITY',82,'image95.png','image96.png','image98.gif','image97.gif'),
 ('RGB ↔ Depth','CROSS MODALITY',1,'image5.png','image2.png','image6.gif','image7.gif'),
 ('RGB ↔ Thermal','CROSS MODALITY',1,'image8.png','image9.png','image10.gif','image11.gif'),
 ('Depth ↔ RGB','CROSS MODALITY',81,'image84.png','image83.png','image85.gif','image86.gif'),
 ('RGB ↔ Event','CROSS MODALITY',81,'image87.png','image88.png','image90.gif','image89.gif'),
 ('LiDAR ↔ RGB','CROSS MODALITY',1,'image12.png','image13.png','image14.gif','image15.gif'),
 ('RGB ↔ Depth · sparse','CROSS MODALITY',82,'image91.png','image92.png','image94.gif','image93.gif'),
]
with zipfile.ZipFile(ROOT/'tartanmatch_talk_finalized.pptx') as deck:
 for filename in {filename for pair in PAIRS for filename in pair[3:]}:
  # Always extract from the specified deck, even if an older extraction exists.
  (MEDIA/filename).write_bytes(deck.read(f'ppt/media/{filename}'))
import json
(OUT/'hero-media-sources.json').write_text(json.dumps({
 'presentation':'tartanmatch_talk_finalized.pptx',
 'groups':[dict(zip(['label','category','slide','source','target','target_to_source','source_to_target'],pair)) for pair in PAIRS]
},indent=2))
for mobile in [False,True]:
 # Same eight groups, reflowed for portrait screens.
 width,height=(900,1800) if mobile else (1920,960)
 cols,rows=(2,4) if mobile else (4,2)
 cw,ch=width//cols,height//rows
 order=[PAIRS[i] for i in ([0,2,1,3,4,6,5,7] if mobile else range(8))]
 base=Image.new('RGB',(width,height),'#11141a');draw=ImageDraw.Draw(base)
 font=ImageFont.truetype(str(OUT/'dm-sans.ttf'),17 if mobile else 19)
 small=ImageFont.truetype(str(OUT/'dm-sans.ttf'),12 if mobile else 14)
 jobs=[]
 for i,(label,group,slide,source,target,to_source,to_target) in enumerate(order):
  x,y=(i%cols)*cw,(i//cols)*ch
  draw.rectangle((x,y,x+cw-2,y+ch-2),fill='#171b21',outline='#343942',width=1)
  draw.text((x+10,y+7),label,font=font,fill='#e7e8eb')
  draw.text((x+10,y+31),group,font=small,fill='#d2a684')
  panel_w=(cw-6)//2
  # Images retain their proportions in a continuous two-row grid.
  panel_h=(ch-96)//2
  for role,index,dx,dy,label_text in [
   ('input',source,3,72,'Source input'),('input',target,3+panel_w,72,'Target input'),
   ('warp',to_source,3,96+panel_h,'Target → source'),('warp',to_target,3+panel_w,96+panel_h,'Source → target')]:
   draw.text((x+dx+7,y+dy-20),label_text,font=small,fill='#c2c7cf')
   src=MEDIA/index
   im=Image.open(src)
   if role=='warp':im.seek(im.n_frames-1)
   tile=ImageOps.contain(im.convert('RGB'),(panel_w,panel_h))
   xx=x+dx+(panel_w-tile.width)//2;yy=y+dy+(panel_h-tile.height)//2
   base.paste(tile,(xx,yy))
   if role=='warp':jobs.append((src,xx,yy,tile.width,tile.height))
 name='hero-warping-mobile' if mobile else 'hero-warping'
 base.save(OUT/f'{name}.webp',quality=90)
 layout=WORK/f'{name}-layout.png';base.save(layout)
 cmd=[FFMPEG,'-hide_banner','-loglevel','error','-y','-loop','1','-i',str(layout)]
 for src,*_ in jobs:cmd+=['-stream_loop','-1','-i',str(src)]
 filters=[];previous='0:v'
 for i,(_,x,y,w,h) in enumerate(jobs,1):
  filters.append(f'[{i}:v]fps=24,scale={w}:{h},setsar=1[v{i}]')
  filters.append(f'[{previous}][v{i}]overlay={x}:{y}:shortest=1[o{i}]');previous=f'o{i}'
 cmd+=['-filter_complex_threads','2','-filter_complex',';'.join(filters),'-map',f'[{previous}]','-t','12','-r','24','-an','-c:v','libx264','-crf','24','-preset','fast','-pix_fmt','yuv420p','-threads','4','-movflags','+faststart',str(OUT/f'{name}.mp4')]
 subprocess.run(cmd,check=True)
 print(name,round((OUT/f'{name}.mp4').stat().st_size/1e6,2),'MB',flush=True)
