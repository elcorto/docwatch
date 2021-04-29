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


def get_src_context(src: str = None, src_ext: str = ""):
    _src_ext = src_ext if src_ext != "" else "markdown"
    if src is None:
        return tempfile.NamedTemporaryFile(suffix=f".{_src_ext}", mode="w+")
    else:
        return open(os.path.expanduser(src), mode="a+")


def get_mtime(fn: str):
    return os.stat(fn).st_mtime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file", metavar="SOURCE_FILE", nargs="?")
    parser.add_argument(
        "-p",
        "--print-command",
        action="store_true",
        default=False,
        help="""Print converter (e.g. pandoc) command that would be executed and
                exit.""",
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
                '%(prog)s -c -- SOURCE_FILE' or '%(prog)s SOURCE_FILE -c' in
                that case).""",
    )
    parser.add_argument(
        "-o",
        "--extra-opts",
        default="",
        help="""Additional options to pass to the converter, e.g. for pandoc:
                %(prog)s -o '--bibliography=/path/to/lit.bib' SOURCE_FILE. Mind
                the quoting. Some shells mess up quoting in the short form -f,
                using the long form as in --extra-opts='-f rst' then helps.""",
    )
    parser.add_argument(
        "-f",
        "--source-format",
        default="",
        help="""Format of SOURCE_FILE (file type, typically file extension).
                Same as %(prog)s --extra-opts='-f SOURCE_FORMAT'. Passed to
                pandoc (-f/--from) if used. Else (default) we use pandoc's
                automatic detection. Use in combination with omitted
                SOURCE_FILE, e.g. "%(prog)s -f rst" to edit a temp rst
                file.""",
    )
    args = parser.parse_args()

    # That is (should be :)) the only pandoc-specific hard coded line.
    converter = PandocToPDFConverter

    conf_dct = conf[converter.conf_section]

    if os.path.exists(conf_dct["logfile"]):
        os.unlink(conf_dct["logfile"])

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
        cv = converter(
            src=args.source_file
                if args.source_file is not None
                else "SOURCE_FILE",
            tgt=f"TARGET.{converter.tgt_ext}",
            extra_opts=args.extra_opts,
            src_ext=args.source_format,
        )
        print(cv.cmd)
        return

    with tempfile.NamedTemporaryFile(
        suffix=f".{converter.tgt_ext}"
    ) as fd_tgt, get_src_context(
        src=args.source_file, src_ext=args.source_format
    ) as fd_src:

        cv = converter(
            src=fd_src.name,
            tgt=fd_tgt.name,
            extra_opts=args.extra_opts,
            src_ext=args.source_format,
        )

        if os.stat(fd_src.name).st_size == 0:
            fd_src.write(
                f"Hi, I'm your new file '{os.path.basename(fd_src.name)}'. "
                f"Delete this line and start hacking."
            )
            # Actually write to file now before we hand fd_src down.
            fd_src.flush()

        def target_viewer():
            run_cmd(f"{conf_dct['pdf_viewer']} {cv.tgt}")

        def target_watch_convert():
            try:
                mtime = get_mtime(cv.src)
                while thread_viewer.is_alive():
                    this_mtime = get_mtime(cv.src)
                    if this_mtime > mtime:
                        mtime = this_mtime
                        cv.convert()
                    time.sleep(0.5)
            except FileNotFoundError:
                # Only when: src is NamedTemporaryFile().name and editor is
                # closed before viewer. Then get_mtime() will raise
                # FileNotFoundError since the temp file was removed. Maybe we
                # should log this case (logfile).
                return

        if args.convert is not None:
            cv.convert(onerror="fail")
            if args.convert != "":
                shutil.copy(cv.tgt, args.convert)
        else:
            cv.convert(onerror="fail")
            thread_viewer = threading.Thread(target=target_viewer)
            thread_viewer.start()
            thread_watch_convert = threading.Thread(
                target=target_watch_convert
            )
            thread_watch_convert.start()
            subprocess.run(
                f"{conf_dct['editor']} {cv.src}", shell=True, check=True
            )
