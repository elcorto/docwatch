import argparse
import os
import subprocess
import tempfile
import threading
import time
import sys


from .converters import PandocToPDFConverter
from .conf import conf
from .subproc import run_cmd


def get_mtime(fn):
    return os.stat(fn).st_mtime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file')
    parser.add_argument('-N', '--no-editor', action='store_true',
                        help="Only render and open result in viewer, "
                             "don't open editor")
    parser.add_argument('-c', '--print-command', action='store_true',
                        help="Print pandoc command that would be executed "
                             "and exit")
    args = parser.parse_args()

    converter = PandocToPDFConverter
    conf_dct = conf[converter.conf_section]

    if os.path.exists(conf_dct['logfile']):
        os.unlink(conf_dct['logfile'])

    src = os.path.expanduser(args.source_file)
    if not os.path.exists(src):
        with open(src, 'w') as fd:
            fd.write(f"Hi, I'm your new file '{os.path.basename(fd.name)}'. "
                     f"Delete this line and start hacking.")

    if args.print_command:
        cv = converter(src=src, tgt=f'output{converter.tgt_ext}')
        print(cv.make_cmd())
        sys.exit()

    with tempfile.NamedTemporaryFile(suffix=converter.tgt_ext) as fd:
        cv = converter(src=src, tgt=fd.name)

        def target_viewer():
            # initial convert only
            cv.convert()
            run_cmd(f"{conf_dct['pdf_viewer']} {cv.tgt}")

        def target_watch_convert():
            mtime = get_mtime(cv.src)
            while thread_viewer.is_alive():
                this_mtime = get_mtime(cv.src)
                if this_mtime > mtime:
                    mtime = this_mtime
                    cv.convert()
                time.sleep(0.5)

        thread_viewer = threading.Thread(target=target_viewer)
        thread_viewer.start()
        if args.no_editor:
            target_watch_convert()
        else:
            thread_watch_convert = threading.Thread(target=target_watch_convert)
            thread_watch_convert.start()
            subprocess.run(f"{conf_dct['editor']} {cv.src}",
                           shell=True,
                           check=True)
