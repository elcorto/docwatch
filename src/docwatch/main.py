import argparse
import configparser
import copy
import os
import subprocess
import tempfile
import threading
import time


from .converters import PandocToPDFConverter


conf_default = {'editor': os.environ.get('EDITOR', 'vim'),
                'pdf_viewer': 'xdg-open',
                'filters': []}
conf_fn = os.path.join(os.environ['HOME'], '.config/docwatch.conf')


def get_mtime(fn):
    return os.stat(fn).st_mtime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file')
    parser.add_argument('--no-editor', action='store_true')
    args = parser.parse_args()

    if os.path.exists(conf_fn):
        cfp = configparser.ConfigParser()
        cfp.read(conf_fn)
        conf = copy.deepcopy(conf_default)
        conf.update(cfp['DEFAULT'])
    else:
        conf = conf_default
    filters = [os.path.expanduser(p) for p in conf['filters'].strip().split()]

    src = os.path.expanduser(args.source_file)
    if not os.path.exists(src):
        with open(src, 'w') as fd:
            fd.write(f"Hi, I'm your new file '{os.path.basename(fd.name)}'. "
                     f"Delete this line and start hacking.")

    # suffix='.pdf' is hard-coded here and relies on cv being an instance of
    # PandocToPDFConverter. We only need to add a suffix here in the PDF case
    # b/c of the quirky pandoc behavior that in order to produce a PDF by
    # running latex, we need to use
    #     pandoc -o foo.pdf
    # instead of what one would expect
    #     pandoc -t pdf
    with tempfile.NamedTemporaryFile(suffix='.pdf') as fd:
        cv = PandocToPDFConverter(src=src,
                                  tgt=fd.name,
                                  filters=filters)

        def viewer_target():
            cv.convert()
            subprocess.run(f"{conf['pdf_viewer']} {cv.tgt} > /dev/null 2>&1",
                           shell=True,
                           check=True)

        thread_viewer = threading.Thread(target=viewer_target)
        thread_viewer.start()

        def wait_target():
            mtime = get_mtime(cv.src)
            while thread_viewer.is_alive():
                this_mtime = get_mtime(cv.src)
                if this_mtime > mtime:
                    mtime = this_mtime
                    cv.convert()
                time.sleep(0.5)

        # Without starting an editor, wait_target() keeps this script running
        # as foreground process, which will in turn keep all started threads
        # alive (e.g. thread_viewer).
        #
        # In case of GUI editors that start their own window, we could also
        # send the editor to a thread in the background, just as we do with
        # thread_viewer.
        #
        # In case we want to open an editor that runs in the terminal (vim), we
        # send wait_target() to the background and start the editor as the
        # foreground process. This will block the Python interpreter process
        # and thus also keep the threads alive. Basically,
        #   python3 -c "import subprocess; subprocess.run('vim')"
        # blocks the Python process as long as vim runs and fills the terminal
        # in which we started this script. Yeah!
        #
        if args.no_editor:
            wait_target()
        else:
            thread_wait = threading.Thread(target=wait_target)
            thread_wait.start()
            subprocess.run(f"{conf['editor']} {cv.src}", shell=True, check=True)
