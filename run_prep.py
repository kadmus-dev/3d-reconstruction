import subprocess as sb
import pathlib as pt
from shlex import split
import os
import argparse

import cv2

def main(args):
    esrgan = pt.Path("./esrgan/realesrgan-ncnn-vulkan")
    gfm_input = pt.Path("./GFM/samples/original")
    gfm_output = pt.Path("./GFM/samples/result_color")
    gfm_mask = pt.Path("./GFM/samples/result_alpha")

    for file in gfm_input.iterdir():
        file.unlink()

    sb.run(split(f"{esrgan} -i {args.input_path} -o {gfm_input} -s 2"))
    os.chdir("./GFM")
    sb.run(split(f"python ./core/test.py --cuda --backbone=r34 --rosta=TT " +
                     f"--model_path=./models/pretrained/gfm_r34_tt.pth " +
                     f" --dataset_choice=SAMPLES --test_choice=HYBRID"))
    os.chdir("..")

    for file in gfm_mask.iterdir():
        file.unlink()

    for file in gfm_output.iterdir():
        image = cv2.imread(str(file))
        cv2.imwrite(str(pt.Path(args.output_path).joinpath(file.name)).replace(".png", ".jpg"),
            image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        #file.rename(pt.Path(args.output_path).joinpath(file.name))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The preprocessing pipeline')
    parser.add_argument('-i', '--input_path', type=str, default='3DDFA_V2/examples/inputs')
    parser.add_argument('-o', '--output_path', type=str, default='3DDFA_V2/examples/results')

    args = parser.parse_args()
    main(args)
