import datetime
import re
import subprocess
import traceback

from .conf import conf


def write_to_logfile(txt: str):
    stamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    txt = re.sub("^", stamp + ": ", txt, flags=re.M).strip() + "\n"
    with open(conf["DEFAULT"]["logfile"], "a") as fd:
        fd.write(txt)


def run_cmd(cmd: str, onerror="log"):
    assert onerror in (
        valid := ["log", "fail"]
    ), f"{onerror=} not one of {valid}"
    try:
        proc = subprocess.run(
            re.sub(r"\s{2,}", " ", cmd.strip(), flags=re.M),
            check=True,
            shell=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
        )
        # If the pandoc call fails (exit !=0) then we catch this with
        # check=True and handle the CalledProcessError below. But things like
        # warning text on stderr goes silently to the logfile.
        out = proc.stdout.decode()
        if len(out) > 0:
            write_to_logfile(out)
    except subprocess.CalledProcessError as ex:
        if onerror == "log":
            write_to_logfile(
                ex.stdout.decode() + "\n" + traceback.format_exc()
            )
        elif onerror == "fail":
            print(ex.stdout.decode())
            raise ex
