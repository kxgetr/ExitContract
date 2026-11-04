"""Compare stdout, stderr and exit codes of two CLI executables for JSON test cases."""
import argparse,base64,json,subprocess,tempfile
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument("old",type=Path)
p.add_argument("new",type=Path)
p.add_argument("--cases",type=Path,required=True)
p.add_argument("--timeout",type=float,default=10)
a=p.parse_args()
cases=json.loads(a.cases.read_bytes())
if not isinstance(cases,list) or not cases or a.timeout<=0: p.error("expected nonempty case list and positive timeout")
def run(exe,case):
    with tempfile.TemporaryDirectory() as cwd:
        result=subprocess.run([str(exe.resolve()),*case.get("args",[])],input=case.get("stdin","").encode(),capture_output=True,cwd=cwd,timeout=a.timeout)
    return {"exit":result.returncode,"stdout":result.stdout,"stderr":result.stderr}
def show(v):
    if not isinstance(v,bytes): return v
    try: return v.decode()
    except UnicodeDecodeError: return {"base64":base64.b64encode(v).decode()}
diffs=[]
for i,case in enumerate(cases):
    if not isinstance(case,dict) or not isinstance(case.get("args",[]),list) or not all(isinstance(v,str) for v in case.get("args",[])) or not isinstance(case.get("stdin",""),str): p.error("invalid case")
    try: x,y=run(a.old,case),run(a.new,case)
    except (OSError,subprocess.TimeoutExpired) as e: p.exit(2,str(e)+"\n")
    changes={k:[show(x[k]),show(y[k])] for k in x if x[k]!=y[k]}
    if changes: diffs.append({"case":case.get("name",i),"changes":changes})
print(json.dumps(diffs,indent=2))
raise SystemExit(int(bool(diffs)))
