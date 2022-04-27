import deploy
import run_3ddfa
import run_pifu
import shutil
import os

parent_dir = "./data"

if __name__ == '__main__':
    prep_path = os.path.join(parent_dir, "preps")
    os.makedirs(prep_path, 0o777)
    print("Directory '%s' created" % prep_path)

    ddfa_path = os.path.join(parent_dir, "3ddfa")
    os.makedirs(ddfa_path, 0o777)
    print("Directory '%s' created" % ddfa_path)

    pifu_path = os.path.join(parent_dir, "3ddfa")
    os.makedirs(pifu_path, 0o777)
    print("Directory '%s' created" % pifu_path)

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_path', type=str, default=prep_path)
    parser.add_argument('-o', '--out_path', type=str, default=pifu_path)
    run_pifu.main(parser.parse_args())

    parser = argparse.ArgumentParser(description='The demo of still image of 3DDFA_V2')
    parser.add_argument('-i', '--input_path', type=str, default=pifu_path)
    parser.add_argument('-o', '--output_path', type=str, default=ddfa_path)
    run_3ddfa.main(parser.parse_args())

    shutil.rmtree(parent_dir)
