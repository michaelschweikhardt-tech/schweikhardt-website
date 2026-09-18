import re,json,subprocess,collections
base='https://oonaschweikhardt.cargo.site/'
seen={};pages={};media={};todo=['','archive','info','home']
def get(u):
    return subprocess.run(['curl','-sSL','-m','30',u],capture_output=True,text=True).stdout
while todo:
    path=todo.pop(0)
    if path in seen: continue
    h=get(base+path); seen[path]=len(h)
    m=re.search(r'window\.__PRELOADED_STATE__\s*=\s*(\{.*?\});?\s*</script>',h,re.S)
    if not m: print('no state',path); continue
    s=json.loads(m.group(1))
    for k,p in s['pages']['byId'].items():
        pages[p['purl']]=p
        for m2 in p.get('media') or []: media[m2['hash']]=m2
        for href in re.findall(r'href="([^"#:]+)"',p['content']):
            href=href.strip('/')
            if href and href not in seen and '.' not in href: todo.append(href)
    for k,p in s['sets']['byId'].items():
        pages.setdefault('SET:'+str(p.get('purl')),p)
        for m2 in p.get('media') or []: media[m2['hash']]=m2
    for mm in s['media'].get('data',[]): media[mm['hash']]=mm
    print(path, len(h), list(s['pages']['byId'].keys()), s['structure']['byParent'])
json.dump({'pages':pages,'media':media},open('all.json','w'),indent=1)
print(len(pages),'pages',len(media),'media')
