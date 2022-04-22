import wget
import os
import subprocess

wget.download(url="https://download.01.org/opencv/openvino_training_extensions/models/human_pose_estimation/checkpoint_iter_370000.pth",
              out="lhpe")

# WARNING: THIS IS A REALLY BAD PRACTICE, REPLACE ASAP
os.chdir('./pifuhd')
subprocess.run(['sh', './scripts/download_trained_model.sh'])