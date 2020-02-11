import argparse
import configparser
import copy
import os
import subprocess
import tempfile
import threading
import time


from .converters import PandocToPDFConverter


def get_mtime(fn):
    return os.stat(fn).st_mtime


def main():
    parser = argparse.ArgumentParser()
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

    # suffix='.pdf' is hard-coded here and relies on cv being an instance of
    # PandocToPDFConverter. We only need to add a suffix here in the PDF case
    # b/c of the quirky pandoc behavior that in order to produce a PDF by
    # running latex, we need to use
    #     pandoc -o foo.pdf
    # instead of what one would expect
    #     pandoc -t pdf
    with tempfile.NamedTemporaryFile(suffix='.pdf') as fd:
        cv = PandocToPDFConverter(src=args.source_file,
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
