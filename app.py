import io
import os
import subprocess as sb
from typing import Union

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from obj2html import obj2html
from pathlib import Path




def main():
    st.title("3D Реконструкция")
    selected_mode = st.sidebar.radio("Выберете режим", ['Face', 'Pose'])

    image_bytes = st.sidebar.file_uploader("Загрузить изображение",
                                           type=["png", "jpg", "jpeg"])

    data_dir = os.path.abspath('data')
    result_dir = os.path.abspath('result')


    if image_bytes is not None:

        img_name = image_bytes.name
        img = load_image(image_bytes)
        img.save(os.path.join(data_dir, img_name))  # Put loaded image into folder data

        st.sidebar.image(img)


        # RUN PIPELINE
        # todo


        # make window with interactive 3d model
        paths = Path(result_dir).glob("*.obj")
        obj_file_path = next(paths)
        html_string = obj2html(obj_file_path, html_elements_only=True)
        components.html(html_string)

        # download obj file
        with open(obj_file_path) as f:
            img_name, ext = os.path.splitext(img_name)
            st.download_button('Download obj file', f,
                               file_name=img_name + '.obj')

        # video
        rendering_width = 500
        rendering_height = 500
        video_path = make_video(obj_file_path, rendering_width, rendering_height)
        video_file = open(video_path, 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes, format="video/mp4", start_time=0)


def make_video(obj_file_path: Union[str, Path], render_width: int, render_height: int) -> str:
    sb.run(['python', f'-m pifuhd.apps.render_turntable -f {obj_file_path} -ww {render_width} -hh {render_height}'])
    # тут надо достать видео, но я не смог сгенерить
    return 'tuc_pizza.mp4'


def load_image(img_bytes):
    img = Image.open(io.BytesIO(img_bytes.getvalue()))
    img = img.convert('RGB')
    return img


if __name__ == "__main__":
    main()