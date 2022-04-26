import os
import gdown
import subprocess
import zipfile

import wget

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
# os.chdir("..")

os.chdir("./3DDFA_V2")
subprocess.run(['sh', './build.sh'])
os.chdir("..")

if not os.path.exists('realesrgan-ncnn-vulkan-20220424-ubuntu.zip'):
    wget.download("https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-ubuntu.zip")
    with zipfile.ZipFile('realesrgan-ncnn-vulkan-20220424-ubuntu.zip', 'r') as zip_ref:
        zip_ref.extractall('esrgan')
    os.chmod('esrgan/realesrgan/', 0o777)
else:
    print('realesrgan-ncnn-vulkan-20220424-ubuntu.zip already exists')

# if not os.path.exists('GFM/models/pretrained/'):
if not os.path.exists('GFM/models/'):
    os.mkdir('GFM/models/')
    
if not os.path.exists('GFM/models/pretrained/'):
    os.mkdir('GFM/models/pretrained/')

url = "https://drive.google.com/uc?export=download&id=1AdtoIdYTLsjXfVe_a50tin0cFwZMSz93"
if not os.path.exists('GFM/models/pretrained/gfm_r34_tt.pth'):
    gdown.download(url, 'GFM/models/pretrained/gfm_r34_tt.pth', quiet=False)
