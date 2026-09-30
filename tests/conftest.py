import os
import sys

# Ensure src directory is on sys.path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_dir = os.path.join(repo_root, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

import fenrirscreenreader.core.i18n
