import time
from io import BytesIO
from typing import Tuple

import requests
from PIL import Image
import math


def download_image(url: str, max_attempts: int = 3, timeout: int = 60) -> Image.Image:
    """
    URL'den görüntü indirir, birkaç kez dener.
    """
    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        try:
            print(f"Görüntü indiriliyor (Deneme {attempt}/{max_attempts}): {url}")
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            img = Image.open(BytesIO(resp.content))
            img.load()
            print(f"Görüntü indirildi: {img.width}x{img.height}")
            return img
        except Exception as e:
            print(f"Deneme {attempt} hata: {e}")
            if attempt >= max_attempts:
                raise
            time.sleep(2)


def determine_cell_position(
    x: float, y: float, img_width: int, img_height: int, rows: int = 12, cols: int = 6
) -> str:
    """
    Koordinatlara göre panel hücresinin konumunu belirler (A1, B2, C3 vb.).
    """
    try:
        x = max(0, min(x, img_width))
        y = max(0, min(y, img_height))

        cell_width = img_width / cols
        cell_height = img_height / rows

        col_index = min(math.floor(x / cell_width), cols - 1)
        col_letter = chr(65 + col_index)  # A=65

        row_index = min(math.floor(y / cell_height), rows - 1)
        row_number = row_index + 1

        return f"{col_letter}{row_number}"
    except Exception as e:
        print(f"Hücre konumu hesaplarken hata: {e}")
        return "X0"


