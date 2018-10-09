# Project Title

File Manager in Google Colaboratory

## Getting Started

These instructions will enable you to use the File Manager on Google Collaborator using ngrok.

## How to use

```
!wget -P colab_utils https://raw.githubusercontent.com/gwgga/fileManagerColab/master/filemanager.py

import os
import sys;
import colab_utils.filemanager
sys.path.append("./colab_utils")

ROOT = %pwd
LOG_DIR = os.path.join(ROOT, 'log')
colab_utils.filemanager.launch_apache( bin_dir=ROOT, log_dir=LOG_DIR )
```
