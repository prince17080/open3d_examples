#!/bin/sh

sudo apt-get install ffmpeg libsm6 libxext6  -y

conda install -c open3d-admin -c conda-forge open3d=0.14.1 --yes
