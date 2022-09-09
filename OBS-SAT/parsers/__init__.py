import sys
import os

# Adds parse module to the python path
for paths in os.listdir():
    if "parse" in paths:
        if os.path.join(os.getcwd(), paths) not in sys.path:
            sys.path.insert(0, os.path.join(os.getcwd(), paths))
