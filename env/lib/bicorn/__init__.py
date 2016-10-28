# from __future__ import absolute_import

# import re
# import sys
# import os

from .utils import *

__version__ = "0.1"


# def thriftzoo_main():
#     from .thriftzoo.app import run as app_run
#     sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
#     return app_run()
#
#
# def gunthrift_main():
#     from .gunthrift.app import run as app_run
#     sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
#     return app_run()
#
# if __package__ == '':
#     path = os.path.dirname(os.path.dirname(__file__))
#     sys.path.insert(0, path)
#
# if __name__ == '__main__':
#     sys.exit(thriftzoo_main())
