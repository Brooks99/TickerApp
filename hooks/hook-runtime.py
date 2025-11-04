import os
import sys

def pre_init():
    # Ensure environment variables are set early
    os.environ["LANG"] = "en_US.UTF-8"
    os.environ["LC_ALL"] = "en_US.UTF-8"
    
    # Additional macOS specific setup
    if sys.platform == 'darwin':
        os.environ["PYTHONIOENCODING"] = "utf-8"
        os.environ["TK_SILENCE_DEPRECATION"] = "1"