"""Extract original research media; run with Python 3.11 + Pillow, PyMuPDF, imageio-ffmpeg."""
from pathlib import Path
import zipfile, subprocess, json, shutil, concurrent.futures
import pymupdf
import imageio_ffmpeg
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'; ASSETS.mkdir(exist_ok=True)
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
for i,p in enumerate(sorted(ROOT.glob('*.pptx'))):
 folder=ROOT/'.work'/f'deck-{i}'; folder.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(p) as z:
  for n in z.namelist():
   if n.startswith('ppt/media/'):
    f=folder/Path(n).name
    if not f.exists(): f.write_bytes(z.read(n))
jobs=[]; manifest=[]
def video(deck,num,name,crop=None):
 src=ROOT/'.work'/f'deck-{deck}'/f'image{num}.gif'; dest=ASSETS/f'{name}.mp4'
 im=Image.open(src).convert('RGB')
 if crop: im=im.crop(crop)
 im.save(ASSETS/f'{name}.webp',quality=85)
 filt=f'crop={crop[2]-crop[0]}:{crop[3]-crop[1]}:{crop[0]}:{crop[1]},' if crop else ''
 jobs.append([ffmpeg,'-hide_banner','-loglevel','error','-y','-i',str(src),'-vf',filt+'scale=trunc(iw/2)*2:trunc(ih/2)*2','-c:v','libx264','-preset','fast','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart','-an','-threads','2',str(dest)])
 manifest.append({'asset':dest.name,'source':f'deck {deck}, image{num}.gif','operation':f'GIF to H.264; crop {crop}'})
mods=['rgb','event','thermal','depth','lidar']
grid=[[39,42,45,46,44],[47,41,48,49,50],[51,52,53,54,55],[56,57,43,40,58],[59,60,61,62,63]]
for r,row in enumerate(grid):
 for c,num in enumerate(row):video(0,num,f'pair-{mods[r]}-{mods[c]}',(0,18,864,306))
for name,nums in [('event-event',[64,66,68]),('event-lidar',[65,67,69]),('event-rgb',[70,72,74]),('rgb-lidar',[77,79,81]),('thermal-event',[82,84,86]),('thermal-lidar',[83,85,87])]:
 for model,num in zip(['minima','matchanything','ours'],nums):video(0,num,f'real-{name}-{model}',(0,18,756,207))
# Static input pairs and both warp directions, verified against presentation layouts.
for name,source,target,to_source,to_target in [
 ('rgb-depth',21,22,23,24), ('rgb-event',17,18,19,20),
 ('depth-thermal',25,26,27,28), ('thermal-event',29,30,31,32)]:
 for role,num in [('source',source),('target',target)]:
  im=Image.open(ROOT/'.work/deck-0'/f'image{num}.png').convert('RGB')
  im.save(ASSETS/f'intro-{name}-{role}.webp',quality=90)
 for direction,num in [('to-source',to_source),('to-target',to_target)]:
  video(0,num,f'intro-{name}-{direction}')
  # A paused or reduced-motion view should show the final predicted alignment.
  im=Image.open(ROOT/'.work/deck-0'/f'image{num}.gif'); im.seek(im.n_frames-1)
  im.convert('RGB').save(ASSETS/f'intro-{name}-{direction}.webp',quality=90)
video(1,97,'dynamic-objects',(0,18,756,207))
for name,num in [('retina-to-target',100),('retina-to-source',101),('satellite-to-source',104),('satellite-to-target',105)]:
 video(1,num,name)
 im=Image.open(ROOT/'.work/deck-1'/f'image{num}.gif'); im.seek(im.n_frames-1)
 im.convert('RGB').save(ASSETS/f'{name}.webp',quality=90)
for name,num in [('retina-source',98),('retina-target',99),('satellite-source',102),('satellite-target',103)]:
 im=Image.open(ROOT/'.work/deck-1'/f'image{num}.png').convert('RGB'); im.save(ASSETS/f'{name}.webp',quality=88)
for name,num in [('snow-rgb',45),('snow-event',46),('snow-lidar',47),('snow-thermal',48)]:
 im=Image.open(ROOT/'.work/deck-1'/f'image{num}.png').convert('RGB'); im.save(ASSETS/f'{name}.webp',quality=85)
paper=next(ROOT.glob('*.pdf')); doc=pymupdf.open(paper)
for name,page,rect in [('architecture',3,(49,56,566,226)),('teaser',0,(49,170,565,377)),('refinement',3,(309,294,565,433))]:
 pix=doc[page].get_pixmap(matrix=pymupdf.Matrix(3,3),clip=pymupdf.Rect(*rect)); pix.save(str(ASSETS/f'{name}.png'))
shutil.copyfile(paper,ASSETS/'tartanmatch-paper.pdf')
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 list(pool.map(lambda args:subprocess.run(args,check=True),jobs))
(ASSETS/'manifest.json').write_text(json.dumps(manifest,indent=2))
print(f'Prepared {len(jobs)} videos. Assets: {sum(p.stat().st_size for p in ASSETS.rglob("*") if p.is_file())/1e6:.1f} MB')
