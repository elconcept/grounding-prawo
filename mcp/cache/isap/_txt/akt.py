import sys,re,json,os,subprocess,html
eli=sys.argv[1]; fmt=sys.argv[2]; unit=sys.argv[3]  # art|par
D=os.path.dirname(os.path.abspath(__file__)); key=eli.replace('/','_')
raw=f"{D}/{key}.txt"
if not os.path.exists(raw):
    if fmt=='pdf':
        p=f"/home/user/abogada/mcp/cache/isap/_pdf/{key}.pdf"
        if not os.path.exists(p):
            subprocess.run(['curl','-sS','-o',p,f'https://api.sejm.gov.pl/eli/acts/{eli}/text.pdf'],check=True)
        import pypdf
        t='\n'.join((pg.extract_text() or '') for pg in pypdf.PdfReader(p).pages)
        t=re.sub(r'\n\s*Dziennik Ustaw\s+–\s*\d+\s*–\s*Poz\. \d+\s*\n','\n',t)
    else:
        t=subprocess.run(['curl','-sS',f'https://api.sejm.gov.pl/eli/acts/{eli}/text.html'],capture_output=True,text=True).stdout
        t=re.sub(r'<(br|/p|/div|/h\d)[^>]*>','\n',t); t=re.sub(r'<[^>]+>',' ',t); t=html.unescape(t)
    open(raw,'w').write(t)
t=open(raw).read()
H=r'Art\.' if unit=='art' else r'§'
heads=[(m.start(),m.group(1)) for m in re.finditer(r'(?m)^\s*'+H+r'\s*(\d+[a-z]*(?:\[\d+\])?)\.\s',t)]
def get(n,which=-1):
    idx=[i for i,(s,k) in enumerate(heads) if k==n]
    if not idx: return None
    i=idx[which]; s=heads[i][0]; e=heads[i+1][0] if i+1<len(heads) else len(t)
    return re.sub(r'\s+',' ',t[s:e]).strip()
if __name__=='__main__':
    which=int(os.environ.get('WHICH','-1'))
    for a in sys.argv[4:]:
        print(f"\n===== {eli} {unit} {a}\n", (get(a,which) or 'BRAK')[:3500])
