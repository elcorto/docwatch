import datetime
import re
import subprocess
import traceback

from .conf import conf


def run_cmd(cmd, onerror="log"):
    assert onerror in (valid := ["log", "fail"]), f"{onerror=} not one of {valid}"
    try:
        subprocess.run(
            re.sub(r"\s{2,}", " ", cmd.strip(), flags=re.M),
            check=True,
            shell=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as ex:
        if onerror == "log":
            out = ex.stdout.decode() + "\n" + traceback.format_exc()
            stamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            out = re.sub("^", stamp + ": ", out, flags=re.M).strip() + "\n"
            with open(conf["DEFAULT"]["logfile"], "a") as fd:
                fd.write(out)
        elif onerror == "fail":
            print(ex.stdout.decode())
            raise ex
