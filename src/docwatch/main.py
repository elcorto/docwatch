import argparse
import os
import subprocess
import tempfile
import threading
import time
import traceback


from .converters import PandocToPDFConverter
from .conf import conf


def get_mtime(fn):
    return os.stat(fn).st_mtime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file')
    parser.add_argument('--no-editor', action='store_true')
    args = parser.parse_args()

    converter = PandocToPDFConverter
    conf_section = conf[converter.conf_section]

    src = os.path.expanduser(args.source_file)
    if not os.path.exists(src):
        with open(src, 'w') as fd:
            fd.write(f"Hi, I'm your new file '{os.path.basename(fd.name)}'. "
                     f"Delete this line and start hacking.")

    # We need to add a suffix == converter.tgt = '.pdf' here in the PDF case
    # b/c of the quirky pandoc behavior that in order to produce a PDF by
    # running latex, we need to use
    #     pandoc -o foo.pdf
    # instead of what one would expect
    #     pandoc -t pdf
    with tempfile.NamedTemporaryFile(suffix=converter.tgt_ext) as fd:
        cv = converter(src=src, tgt=fd.name)

        def target_viewer():
            # initial convert only
            cv.convert()
            subprocess.run(f"{conf_section['pdf_viewer']} {cv.tgt} "
                           f"> /dev/null 2>&1",
                           shell=True,
                           check=True)

        def target_watch_convert():
            mtime = get_mtime(cv.src)
            while thread_viewer.is_alive():
                this_mtime = get_mtime(cv.src)
                if this_mtime > mtime:
                    mtime = this_mtime
                    try:
                        cv.convert()
                    except Exception:
                        traceback.print_exc()
                time.sleep(0.5)

        # Without starting an editor, target_watch_convert() keeps this script
        # running as foreground process, which will in turn keep all started
        # threads alive (e.g. thread_viewer).
        #
        # In case of GUI editors that start their own window, we could also
        # send the editor to a thread in the background, just as we do with
        # thread_viewer.
        #
        # In case we want to open an editor that runs in the terminal (vim), we
        # send target_watch_convert() to the background and start the editor as the
        # foreground process. This will block the Python interpreter process
        # and thus also keep the threads alive. Basically,
        #   python3 -c "import subprocess; subprocess.run('vim')"
        # blocks the Python process as long as vim runs and fills the terminal
        # in which we started this script. Yeah!
        #
        thread_viewer = threading.Thread(target=target_viewer)
        thread_viewer.start()
        if args.no_editor:
            target_watch_convert()
        else:
            thread_watch_convert = threading.Thread(target=target_watch_convert)
            thread_watch_convert.start()
            subprocess.run(f"{conf_section['editor']} {cv.src}",
                           shell=True,
                           check=True)
