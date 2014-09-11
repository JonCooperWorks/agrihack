import glob
import sys


def configure_libraries():
    sys.path.extend(glob.glob('libraries/*.zip'))
    # Ensure no duplicates
    sys.path = list(set(sys.path))

configure_libraries()
