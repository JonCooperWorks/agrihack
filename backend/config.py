import glob
import os
import sys


def configure_libraries():
    sys.path.extend(glob.glob('libraries/*.zip'))
    # Ensure no duplicates
    sys.path = list(set(sys.path))

configure_libraries()

DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Development')
