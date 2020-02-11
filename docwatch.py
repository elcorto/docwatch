#!/usr/bin/env python3

import os
import shlex
import subprocess
import sys
import tempfile
import threading
import time


def get_mtime(fn):
    return os.stat(fn).st_mtime


class PandocConverter:
    # For now pypandoc would be overkill here. Re-visit should we plan to
    # support arbitrary input and output formats. Then pypandoc's format
    # handling might come in handy.
    options = ''
    filters = []
    tgt_ext = None

    def __init__(self, src, tgt):
        self.src = src
        self.tgt = tgt
        if self.tgt_ext is not None:
            assert tgt.endswith(self.tgt_ext)

    def convert(self):
        filters = " ".join(f"-F {ff}" for ff in self.filters)
        cmd = f"pandoc {filters} {self.options} -o {self.tgt} {self.src}"
        subprocess.run(shlex.split(cmd))


class Markdown2PDFConverter(PandocConverter):
    options = '-V documentclass=scrartcl -V pagesize=a4'
    filters = ['/home/elcorto/soft/git/pandocfilters/examples/gitlab_markdown.py']
    tgt_ext = 'pdf'


if __name__ == '__main__':
    src = sys.argv[1]

    with tempfile.NamedTemporaryFile(suffix='.pdf') as fd:
        cv = Markdown2PDFConverter(src=src, tgt=fd.name)
        cv.convert()
        thread = threading.Thread(
            target=lambda: subprocess.run(f"xdg-open {cv.tgt} > /dev/null 2>&1", shell=True)
            )
        thread.start()
        mtime = get_mtime(src)
        while thread.is_alive():
            this_mtime = get_mtime(src)
            if this_mtime > mtime:
                mtime = this_mtime
                cv.convert()
            time.sleep(0.5)
