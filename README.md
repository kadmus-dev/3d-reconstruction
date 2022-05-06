# 3D Reconstruction

Person's 2D to 3D shapes reconstruction.  

![](imgs/pipeline.png)

### Cloning

To clone this repository and its submodules, run the following command:
```bash
git clone --recurse-submodules git@github.com:kadmus-dev/3d-reconstruction.git
```

If your submodule folders are empty, run:
```bash
git submodule init
git submodule update
```

### Downloading models
To download models, simply run
```bash
python3 deploy.py
```

### Installing dependencies
Because of pip quirks - to install with thw following command:
```bash
pip install cython
pip install numpy
pip install -r requirements.txt
```

### Application

```
streamlit run app.py
```

![](imgs/streamlit.jpg)

### Running specific models

PIFuHD is run on all files inside input_directory and outputs results to output_directory
```bash
python run_pifu.py -i {input_directory} -o {output_directory}
```

3DDFA_V2 is run on all files inside input_directory and outputs results to output_directory
```bash
python run_3ddfa.py -i {input_directory} -o {output_directory}
```
