#!/usr/bin/env python3
"""Reproduce Santos-Santos+2020 J/MNRAS/495/58 Table A1 gravity diagnostics.
Usage: python cross_survey_fiducial_2026-10-19.py tablea1.dat
Requires original 160-line CDS fixed-width file, no third-party packages.
This is one fiducial point per galaxy, NOT full rotation-curve analysis.
"""
import sys,math,json,hashlib
from pathlib import Path
SHA="3d8839e658c84002387273755e21237191fd7d48"
KPC=3.085677581491367e19
def load(path):
    buf=Path(path).read_bytes()
    sha=hashlib.sha1(b"blob "+str(len(buf)).encode()+b"\0"+buf).hexdigest()
    if sha!=SHA: raise ValueError("Source hash differs: "+sha)
    lines=buf.decode().strip().splitlines()
    if len(lines)!=160: raise ValueError("Not 160 source rows")
    result=[]
    for s in lines:
        d=dict(name=s[:11].strip(),survey=s[12:14].strip(),
               vmax=float(s[15:21]),vo=float(s[29:35]),
               vb=float(s[36:42]),mass=float(s[43:51]),
               size=float(s[52:57]))
        if d["survey"] not in ("S","LT","TH","A","R") or any(d[k]<=0 for k in ("vmax","vo","vb","mass","size")):
            raise ValueError("Bad source row "+s)
        radius=2*d["vmax"]/70
        d["go"]=d["vo"]**2/radius*1e6/KPC
        d["gb"]=d["vb"]**2/radius*1e6/KPC
        d["radius"]=math.log10(radius)
        d["weak"]=math.log10(1e-10/d["gb"])
        d["y"]=math.log10(d["go"]/d["gb"])
        result.append(d)
    counts={c:sum(d["survey"]==c for d in result) for c in ("S","LT","TH","A","R")}
    if counts!={"S":141,"LT":11,"TH":2,"A":2,"R":4}: raise ValueError("Bad survey split")
    return result
def fit(rows,keys):
    n=len(keys)+1
    a=[[0.]*(n+1) for _ in range(n)]
    for d in rows:
        z=[1.]+[d[k] for k in keys]
        for i in range(n):
            for j in range(n): a[i][j]+=z[i]*z[j]
            a[i][n]+=z[i]*d["y"]
    for i in range(n):
        p=max(range(i,n),key=lambda t:abs(a[t][i]))
        a[i],a[p]=a[p],a[i]
        if abs(a[i][i])<1e-12: raise ValueError("Singular")
        div=a[i][i]
        a[i]=[v/div for v in a[i]]
        for j in range(n):
            if j!=i:
                c=a[j][i]
                a[j]=[x-c*y for x,y in zip(a[j],a[i])]
    return [r[n] for r in a]
def analyze(sample):
    rows=sorted(sample,key=lambda d:d["name"].lower())
    models=dict(constant=[],radius=["radius"],acceleration=["weak"],both=["radius","weak"])
    rms={}
    for name,keys in models.items():
        loss=0
        for i,d in enumerate(rows):
            train=[t for j,t in enumerate(rows) if j%5!=i%5]
            coeff=fit(train,keys)
            guess=coeff[0]+sum(c*d[k] for c,k in zip(coeff[1:],keys))
            loss+=(guess-d["y"])**2
        rms[name]=math.sqrt(loss/len(rows))
    baryon=math.sqrt(sum(d["y"]**2 for d in rows)/len(rows))
    rar=math.sqrt(sum(math.log10((d["gb"]/-math.expm1(-math.sqrt(d["gb"]/1.2e-10)))/d["go"])**2 for d in rows)/len(rows))
    candidates=[]
    for i,one in enumerate(rows):
        for two in rows[i+1:]:
            a,b=sorted((one,two),key=lambda d:d["size"])
            dm=abs(math.log10(a["mass"]/b["mass"]))
            ratio=b["size"]/a["size"]
            if dm<=.1 and ratio>=2:
                candidates.append((dm,-ratio,a["name"].lower(),b["name"].lower(),a,b))
    candidates.sort(key=lambda z:z[:4])
    used=set(); pairs=[]
    for _,_,_,_,a,b in candidates:
        if a["name"] not in used and b["name"] not in used:
            used.update((a["name"],b["name"]));pairs.append((a,b))
    return dict(galaxies=len(rows),cross_validated_RMSE_dex=rms,
                baryon_only_fixed_RMSE_dex=baryon,fixed_RAR_RMSE_dex=rar,
                selected_pairs=len(pairs),extended_lower_gbar=sum(b["gb"]<a["gb"] for a,b in pairs),
                extended_larger_discrepancy=sum(b["y"]>a["y"] for a,b in pairs))
if __name__=="__main__":
    if len(sys.argv)!=2: raise SystemExit("Usage: python script.py tablea1.dat")
    data=load(sys.argv[1])
    sets={"all_160":data,"SPARC_141":[d for d in data if d["survey"]=="S"],
          "nonSPARC_19":[d for d in data if d["survey"]!="S"],
          "LITTLE_THINGS_11":[d for d in data if d["survey"]=="LT"]}
    print(json.dumps({k:analyze(v) for k,v in sets.items()},indent=2))
