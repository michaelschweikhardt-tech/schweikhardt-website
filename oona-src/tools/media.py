import json,os,glob,subprocess,concurrent.futures as cf
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS=None
out='site/media'; info={}
WIDTHS=[640,1280,2000]
def img(f):
    h=os.path.basename(f).split('.')[0]
    im=Image.open(f); im=ImageOps.exif_transpose(im)
    has_alpha = im.mode in ('RGBA','LA') or (im.mode=='P' and 'transparency' in im.info)
    im=im.convert('RGBA' if has_alpha else 'RGB')
    W,H=im.size; ws=[]
    for w in WIDTHS:
        if w>=W and ws: break
        ww=min(w,W); t=im.resize((ww,round(H*ww/W)),Image.LANCZOS) if ww<W else im
        t.save(f'{out}/{h}-{ww}.webp','WEBP',quality=82,method=5); ws.append(ww)
        if ww==W: break
    return h,{'type':'image','w':W,'h':H,'widths':ws}
def vid(f):
    h=os.path.basename(f).split('.')[0]
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f,'-vf',"scale='min(1280,iw)':-2",'-c:v','libx264','-crf','26','-preset','slow','-pix_fmt','yuv420p','-movflags','+faststart','-an',f'{out}/{h}.mp4'],check=True)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'{out}/{h}.mp4','-vframes','1','-q:v','4','-vf',"scale='min(1280,iw)':-2",f'{out}/{h}-poster.jpg'],check=True)
    p=json.loads(subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',f'{out}/{h}.mp4'],capture_output=True,text=True).stdout)['streams'][0]
    return h,{'type':'video','w':p['width'],'h':p['height']}
files=glob.glob('orig/*')
with cf.ProcessPoolExecutor(os.cpu_count()) as ex:
    res=list(ex.map(lambda f: None, [])) 
    fut=[ex.submit(vid if f.endswith('.mp4') else img,f) for f in files]
    for x in fut:
        h,i=x.result(); info[h]=i
json.dump(info,open('mediainfo.json','w'))
print(len(info))
