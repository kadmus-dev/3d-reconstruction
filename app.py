import io
import os
import subprocess as sb
from typing import Union
from itertools import filterfalse
from shlex import split

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from obj2html import obj2html
import pathlib as pt

import runner

def filter_hidden(seq):
    yield from filterfalse(lambda x: x.name.startswith("."), seq)

def main():
    st.title("3D Реконструкция")
    selected_mode = st.sidebar.radio("Выбирете режим", ['Face', 'Pose'])

    image_bytes = st.sidebar.file_uploader("Загрузить изображение",
                                           type=["png", "jpg", "jpeg"])

    data_dir = pt.Path("./data")
    result_dir = pt.Path("./results")

    data_dir.mkdir(exist_ok=True)
    result_dir.mkdir(exist_ok=True)

    if image_bytes is not None:

        for file in filter_hidden(data_dir.iterdir()):
            file.unlink()
        for file in filter_hidden(result_dir.iterdir()):
            file.unlink()

        img_name = image_bytes.name
        img = load_image(image_bytes)
        img.save(data_dir.joinpath(img_name))  # Put loaded image into folder data

        st.sidebar.image(img)

        runner.run(data_dir, result_dir, selected_mode)

        #make window with interactive 3d model
        paths = result_dir.glob("*.obj")
        obj_file_path = next(paths)
        # html_string = obj2html(obj_file_path, html_elements_only=True)
        # components.html(html_string)
        
        zip_path = result_dir.joinpath(obj_file_path.name.replace('obj', 'zip'))
        sb.run(split(f"zip -r {zip_path} ./results"))

        # download obj file
        with open(zip_path, "rb") as f:
            #img_name, ext = os.path.splitext(img_name)
            st.download_button('Download zip with obj file', f,
                               file_name=zip_path.name)

        #image
        if selected_mode == "Face":
            image = Image.open(next(result_dir.glob("*_2d.jpg")))
            st.image(image)
        
        # video
        #rendering_width = 500
        #rendering_height = 500
        #video_path = make_video(obj_file_path, rendering_width, rendering_height)
        #video_file = open(video_path, 'rb')
        #video_bytes = video_file.read()
        #st.video(video_bytes, format="video/mp4", start_time=0)


def make_video(obj_file_path: Union[str, pt.Path], render_width: int, render_height: int) -> str:
    sb.run(split(f'python -m pifuhd.apps.render_turntable, -f {obj_file_path} -ww {render_width} -hh {render_height}'))
    # тут надо достать видео, но я не смог сгенерить
    return 'tuc_pizza.mp4'


def load_image(img_bytes):
    img = Image.open(io.BytesIO(img_bytes.getvalue()))
    img = img.convert('RGB')
    return img


if __name__ == "__main__":
    main()
