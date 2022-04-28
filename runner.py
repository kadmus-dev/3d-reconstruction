import pathlib as pt
import tempfile
import argparse
import subprocess as sb
from shlex import split

#import run_pifu
import run_prep
import run_3ddfa
import time


class IOargs():
    def __init__(self, input, output):
        self.input_path = str(input)
        self.output_path = str(output)


def run(input, output, mode):
    start = time.time()
    data = pt.Path(input)
    result = pt.Path(output)
    #prep = pt.Path("./prep")
    #prep.mkdir(exist_ok=True)


    if mode == "Pose":
        print('Running preprocessing')
        pifu_path = "./pifuhd/sample_images"
        run_prep.main(IOargs(data, pifu_path))
        #sb.run(split(f"python run_pifu.py -i {pifu_path} -o {result}"))

    else:
        with tempfile.TemporaryDirectory() as prep:
            print('Running preprocessing')
            run_prep.main(IOargs(data, prep))
            print('Running 3ddfa')
            run_3ddfa.main(IOargs(prep, result))

    print(time.time() - start)


def main(args):
    run(args.input_path, args.output_path, args.mode)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runner')
    parser.add_argument('-i', '--input_path', type=str, default='./data')
    parser.add_argument('-o', '--output_path', type=str, default='./result')
    parser.add_argument('-m', '--mode', type=str, choices=['Face', 'Pose'], default='body')
    args = parser.parse_args()
    main(args)
