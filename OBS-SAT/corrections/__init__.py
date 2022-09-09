import sys
import os

# Adds corrections module to the python path
for paths in os.listdir():
    if "corrections" in paths:
        if os.path.join(os.getcwd(), paths) not in sys.path:
            sys.path.insert(0, os.path.join(os.getcwd(), paths))
