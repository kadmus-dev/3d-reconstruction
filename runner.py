import pathlib as pt
import tempfile
import argparse

import run_prep
import run_3ddfa
import run_pifu


class IOargs():
    def __init__(self, input, output):
        self.input_path = input
        self.output_path = output


def run(input, output, mode):
    data = pt.Path(input)
    result = pt.Path(output)
    with tempfile.TemporaryDirectory() as prep:
        print('Running preprocessing')
        run_prep.main(IOargs(data, prep))

        if mode == "body":
            print('Running pifu')
            run_pifu.main(IOargs(prep, result))
        else:
            print('Running 3ddfa')
            run_3ddfa.main(IOargs(prep, result))


def main(args):
    run(args.input_path, args.output_path, args.mode)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runner')
    parser.add_argument('-i', '--input_path', type=str, default='./data')
    parser.add_argument('-o', '--output_path', type=str, default='./result')
    parser.add_argument('-m', '--mode', type=str, choices=['face', 'body'], default='body')
    args = parser.parse_args()
    main(args)
