import os
import sys


if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    if BASE_DIR.endswith('bin'):
        BASE_DIR = os.path.dirname(BASE_DIR)
    BASE_DIR = os.path.join(BASE_DIR, 'src')
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_BASE_DIR = None
if os.name == "nt":  # Windows users could be on a domain with a documents folder not in their home directory.
    try:
        import ctypes.wintypes
        CSIDL_PERSONAL = 5
        SHGFP_TYPE_CURRENT = 0
        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_PERSONAL, 0, SHGFP_TYPE_CURRENT, buf)
        DB_BASE_DIR = os.path.join(buf.value, "ADSM Workspace", "settings")
    except:
        DB_BASE_DIR = None
if not DB_BASE_DIR:
    DB_BASE_DIR = os.path.join(os.path.expanduser("~"), "Documents", "ADSM Workspace", "settings")
if not os.path.exists(DB_BASE_DIR):
    os.makedirs(DB_BASE_DIR, exist_ok=True)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zkvb3#=7zub^kw-@hmf2v4rgsn%5q$!^0i4v#l)$_umn=_lx&3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {

}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'