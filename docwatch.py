#!/usr/bin/env python3

import argparse
import configparser
import copy
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
    tgt_ext = None

    def __init__(self, src, tgt, filters=[]):
        self.src = src
        self.tgt = tgt
        self.filters = filters
        if self.tgt_ext is not None:
            assert tgt.endswith(self.tgt_ext)

    def convert(self):
        filters = " ".join(f"-F {ff}" for ff in self.filters)
        cmd = f"pandoc {filters} {self.options} -o {self.tgt} {self.src}"
        subprocess.run(shlex.split(cmd), check=True)


# XXX link-citations and citecolor doesn't work
class Markdown2PDFConverter(PandocConverter):
    options = '-V documentclass=scrartcl \
               -V pagesize=a4 \
               -V colorliks \
               -V linkcolor=red \
               -V urlcolor=blue \
               -V citecolor=green \
               -V link-citations=true \
               '
    tgt_ext = 'pdf'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='foo')
    parser.add_argument('source_file')
    parser.add_argument('-e', '--with-editor', action='store_true')
    args = parser.parse_args()

    conf_default = {'editor': 'gvim',
                    'pdf_viewer': 'xpdf',
                    'filters': []}
    conf_fn = os.path.join(os.environ['HOME'], '.config/docwatch.conf')
    if os.path.exists(conf_fn):
        cfp = configparser.ConfigParser()
        cfp.read(conf_fn)
        conf = copy.deepcopy(conf_default)
        conf.update(cfp['DEFAULT'])
    else:
        conf = conf_default

    filters = [os.path.expanduser(p) for p in conf['filters'].strip().split()]
    with tempfile.NamedTemporaryFile(suffix='.pdf') as fd:
        cv = Markdown2PDFConverter(src=args.source_file,
                                   tgt=fd.name,
                                   filters=filters)
        cv.convert()
        threads = {}
        threads['viewer'] = threading.Thread(
            target=lambda: subprocess.run(f"{conf['pdf_viewer']} {cv.tgt} > /dev/null 2>&1",
                                          shell=True,
                                          check=True)
            )
        if args.with_editor:
            threads['editor'] = threading.Thread(
                target=lambda: subprocess.run(f"{conf['editor']} {cv.src} > /dev/null 2>&1",
                                              shell=True,
                                              check=True)
                )
        for thr in threads.values():
            thr.start()
        mtime = get_mtime(cv.src)
        while threads['viewer'].is_alive():
            this_mtime = get_mtime(cv.src)
            if this_mtime > mtime:
                mtime = this_mtime
                cv.convert()
            time.sleep(0.5)
