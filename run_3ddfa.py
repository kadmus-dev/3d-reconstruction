import argparse
import os
import pathlib as pt
import sys

# hack from savitsky)
sys.path.append('./3DDFA_V2')

import cv2
import yaml
from FaceBoxes import FaceBoxes
from TDDFA import TDDFA
from utils.functions import get_suffix
from utils.serialization import ser_to_obj
from utils.serialization import ser_to_ply
from utils.uv import uv_tex
from utils.functions import draw_landmarks

def main(args):
    input_path = pt.Path(args.input_path).resolve()
    output_path = pt.Path(args.output_path).resolve()

    # cos of hardcoded relative pathes in config yml
    os.chdir("./3DDFA_V2")
    cfg = yaml.load(open("configs/mb1_120x120.yml"), Loader=yaml.SafeLoader)

    tddfa = TDDFA(gpu_mode=False, **cfg)
    face_boxes = FaceBoxes()

    # Given a still image path and load to BGR channel
    for img_path in input_path.iterdir():
        if not img_path.is_file() or img_path.name.startswith("."):
            continue
        print(img_path)
        img = cv2.imread(str(img_path))

        # Detect faces, get 3DMM params and roi boxes
        boxes = face_boxes(img)
        n = len(boxes)
        #if n == 0:
        #    print(f'No face detected, exit')
        #    os.chdir("..")
        #    sys.exit(-1)
        print(f'Detect {n} faces')

        param_lst, roi_box_lst = tddfa(img, boxes)

        # Visualization and serialization
        old_suffix = get_suffix(str(img_path))
        name = img_path.name.replace(old_suffix, "")

        wfp = output_path.joinpath(name)
        #wfp.mkdir(exist_ok=True)
        #wfp = wfp.joinpath(name)

        ver_lst = tddfa.recon_vers(param_lst, roi_box_lst, dense_flag=True)
    
        draw_landmarks(img, ver_lst, show_flag=False, dense_flag=True, wfp=f"{wfp}_2d.jpg")
        uv_tex(img, ver_lst, tddfa.tri, show_flag=False, wfp=f"{wfp}_uv.jpg")
        ser_to_ply(ver_lst, tddfa.tri, height=img.shape[0], wfp=f"{wfp}.ply")
        ser_to_obj(img, ver_lst, tddfa.tri, height=img.shape[0], wfp=f"{wfp}.obj")
    os.chdir("..")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The demo of still image of 3DDFA_V2')
    parser.add_argument('-i', '--input_path', type=str, default='3DDFA_V2/examples/inputs')
    parser.add_argument('-o', '--output_path', type=str, default='3DDFA_V2/examples/results')

    args = parser.parse_args()
    main(args)
