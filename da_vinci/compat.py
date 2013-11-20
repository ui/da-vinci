import sys


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


if PY3:
    string_types = str
else:
    string_types = basestring

try:
    from urlparse import urlparse
except ImportError:
    # Python 3 version
    from urllib.parse import urlparse

try:
    from urllib import urlopen
except ImportError:
    # Python 3 version
    from urllib.request import urlopen