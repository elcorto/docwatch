import datetime
import re
import subprocess
import traceback

from .conf import conf


def run_cmd(cmd):
    try:
        subprocess.run(cmd, check=True, shell=True,
                       stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as ex:
        out = ex.stdout.decode() + '\n' + traceback.format_exc()
        stamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        out = re.sub('^', stamp + ': ', out, flags=re.M).strip() + '\n'
        with open(conf['DEFAULT']['logfile'], 'a') as fd:
            fd.write(out)
