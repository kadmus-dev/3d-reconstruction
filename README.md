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

## Dependencies
Because of pip quirks - to install with thw following command:
```bash
pip install cython
pip install numpy
pip install -r requirements.txt
```