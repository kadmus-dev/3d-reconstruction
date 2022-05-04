# 3d-reconstruction


## Cloning

To clone this repository AND its submodules - run the following command:
```bash
git clone --recurse-submodules git@github.com:kadmus-dev/3d-reconstruction.git
```

If your submodule folders are empty(e.g. you forgot `--recurse-submodules` or checkouted to a branch with new submodules) - run:
```bash
git submodule init
git submodule update
```

## Download models
To download models, simply run
```bash
python3 deploy.py
```

## Dependencies
Because of pip quirks - to install with thw following command:
```bash
pip install cython
pip install numpy
pip install -r requirements.txt
```

## How to run 3DDFA_V2
Script will be runned on all the files inside input_directory and will output results to output_directory
```bash
python run_pifu.py -i {input_directory} -o {output_directory}
```

## How to run 3DDFA_V2
Script will be runned on all the files inside input_directory and will output results to output_directory
```bash
python run_3ddfa.py -i {input_directory} -o {output_directory}
```

