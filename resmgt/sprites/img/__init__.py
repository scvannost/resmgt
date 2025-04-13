import os
from typing import List


def sprite_image_filepath(filename: str) -> str:
    return os.path.join(
        os.path.dirname(__file__),
        filename,
    )


def get_supported_img_filenames() -> List[str]:
    return os.listdir(os.path.dirname(__file__))
