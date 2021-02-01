import argparse
import os
import shutil
import subprocess
import tempfile
import threading
import time

from .converters import PandocToPDFConverter
from .conf import conf
from .subproc import run_cmd


def get_mtime(fn):
    return os.stat(fn).st_mtime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file", metavar="SOURCE")
    parser.add_argument(
        "-p",
        "--print-command",
        action="store_true",
        default=False,
        help="""Print converter (e.g. pandoc) command that would be executed and
                exit.""",
    )
    parser.add_argument(
        "-N",
        "--no-editor",
        action="store_true",
        default=False,
        help="Only render and open result in viewer, don't open editor.",
    )
    parser.add_argument(
        "-c",
        "--convert",
        nargs="?",
        metavar="TARGET",
        default=None,
        const="",
        help="""Convert mode. Only run converter (see --print-command) and
                produce TARGET (optional, temp file used if omitted, use
                '%(prog)s -c -- SOURCE' or '%(prog)s SOURCE -c' in that
                case).""",
    )
    parser.add_argument(
        "-o",
        "--extra-opts",
        default="",
        help="""Additional options to pass to the converter, e.g. for pandoc:
                %(prog)s -o '--bibliography=/path/to/lit.bib' SOURCE.
                Mind the quoting.""",
    )
    args = parser.parse_args()

    # pandoc-specific
    converter = PandocToPDFConverter

    conf_dct = conf[converter.conf_section]

    if os.path.exists(conf_dct["logfile"]):
        os.unlink(conf_dct["logfile"])

    src = os.path.expanduser(args.source_file)
    if not os.path.exists(src):
        with open(src, "w") as fd:
            fd.write(f"Hi, I'm your new file '{os.path.basename(fd.name)}'. "
                     f"Delete this line and start hacking.")

    # src and extra_opts are the same in every place where we call
    # converter(...). Better use smth like
    #   converter=functools.partial(PandocToPDFConverter,
    #                               extra_opts=args.extra_opts,
    #                               src=src)
    #   ...
    #   cv = converter(tgt=...)
    # but that breaks access to converter.some_attrs (e.g.
    # converter.conf_section)
    if args.print_command:
        cv = converter(src=src,
                       tgt=f"output{converter.tgt_ext}",
                       extra_opts=args.extra_opts)
        print(cv.make_cmd())
        return

    with tempfile.NamedTemporaryFile(suffix=converter.tgt_ext) as fd:
        cv = converter(src=src, tgt=fd.name, extra_opts=args.extra_opts)

        def target_viewer():
            run_cmd(f"{conf_dct['pdf_viewer']} {cv.tgt}")

        def target_watch_convert():
            mtime = get_mtime(cv.src)
            while thread_viewer.is_alive():
                this_mtime = get_mtime(cv.src)
                if this_mtime > mtime:
                    mtime = this_mtime
                    cv.convert()
                time.sleep(0.5)

        if args.convert is not None:
            cv.convert(onerror="fail")
            if args.convert != "":
                shutil.copy(cv.tgt, args.convert)
        else:
            cv.convert(onerror="fail")
            thread_viewer = threading.Thread(target=target_viewer)
            thread_viewer.start()
            if args.no_editor:
                target_watch_convert()
            else:
                thread_watch_convert = threading.Thread(
                    target=target_watch_convert
                )
                thread_watch_convert.start()
                subprocess.run(f"{conf_dct['editor']} {cv.src}",
                               shell=True,
                               check=True)
