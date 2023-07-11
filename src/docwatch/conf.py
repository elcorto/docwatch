import configparser
import copy
import os


conf_default = configparser.ConfigParser()

# configparser magic: settings from the DEFAULT section are mirrored in all
# other sections, and can be overwritten there if needed. That's why
# conf_default.sections() only returns ['pandoc'] .
conf_default["DEFAULT"] = dict(
    editor=os.environ.get("EDITOR", "vim"),
    pdf_viewer="xdg-open",
    logfile="/tmp/docwatch.log",
)

conf_default["pandoc"] = dict(
    pdf_engine="pdflatex",
    filters="",
    latex_options="",
    citeproc=True,
)

conf_fn = os.path.join(os.environ["HOME"], ".config/docwatch/docwatch.conf")


def get_conf():
    if os.path.exists(conf_fn):
        conf_user = configparser.ConfigParser()
        conf_user.read(conf_fn)
        conf = copy.deepcopy(conf_default)
        for section in conf_user.sections():
            conf[section].update(conf_user[section])
    else:
        conf = conf_default
    return conf


conf = get_conf()
