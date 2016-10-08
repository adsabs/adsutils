import os
import sys
import nose

test_dir = os.path.abspath(os.path.dirname(__file__))

argv = sys.argv[:] + ['-v']
nose.main(argv=argv)
