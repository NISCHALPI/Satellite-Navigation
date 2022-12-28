import sys
import os

# Adds calculations module to the python path
for paths in os.listdir():
    if "calculations" in paths:
        if os.path.join(os.getcwd(), paths) not in sys.path:
            sys.path.insert(0, os.path.join(os.getcwd(), paths))
