import wget
import os
import subprocess

if not os.path.exists('lhpe/checkpoint_iter_370000.pth'):
    wget.download(url="https://download.01.org/opencv/openvino_training_extensions/models/human_pose_estimation/checkpoint_iter_370000.pth",
                  out="lhpe")
else:
    print('checkpoint_iter_370000.pth already exists')


if not os.path.exists('pifuhd/checkpoints/pifuhd.pt'):
    # WARNING: THIS IS A REALLY BAD PRACTICE, REPLACE ASAP
    os.chdir('./pifuhd')
    subprocess.run(['sh', './scripts/download_trained_model.sh'])
else:
    print('pifuhd.pt already exists')
