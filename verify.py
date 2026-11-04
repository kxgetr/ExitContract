import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

SCRIPT = Path(__file__).with_name("exitcontract.py")
def run(*args, ok=0):
    result = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)
    assert result.returncode == ok, (args, result.stdout, result.stderr)
    return result

def git(*args):
    subprocess.run(["git", *args], check=True)

with tempfile.TemporaryDirectory() as tmp:
    os.chdir(tmp)
    Path("cases.json").write_text(json.dumps([{"args":["-c","print(42)"]}]))
    assert json.loads(run(sys.executable,sys.executable,"--cases","cases.json").stdout)==[]
    if os.name=="posix":
        for name,code in [("a","1"),("b","2")]:
            path=Path(name)
            path.write_text("#!/bin/sh\nexit "+code+"\n")
            path.chmod(0o755)
        assert json.loads(run("a","b","--cases","cases.json",ok=1).stdout)[0]["changes"]["exit"]==[1,2]
