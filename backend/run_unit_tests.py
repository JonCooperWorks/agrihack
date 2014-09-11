#!/usr/bin/env python

import os
import sys

from nose.core import TestProgram

APPENGINE_SDK_PATH = '/usr/local/google_appengine'


def main():
    # Add the App Engine SDK to the system path.
    sys.path.insert(0, APPENGINE_SDK_PATH)

    # For good measure, also update the PYTHONPATH environment variable.
    os.environ['PYTHONPATH'] = APPENGINE_SDK_PATH

    # Let the dev_appserver do some magic fixing.
    import dev_appserver
    dev_appserver.fix_sys_path()

    # Add the project libraries to the PYTHONPATH.
    import config
    config.configure_libraries()

    # Run just like nosetests.
    return TestProgram()


if __name__ == '__main__':
    main()
