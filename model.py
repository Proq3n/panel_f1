import os
from typing import List, Dict

import torch
import numpy as np
import cv2
from PIL import Image

from ultralytics import YOLO


CLASS_NAMES = [
    "Soldering Error",
    "Ribbon Offset",
    "Crack",
    "Broken Cell",
    "Broken Finger",
    "SEoR",
    "Stain",
    "Microcrack",
    "Scratch",
]


class PanelDefectDetector:
    """
    Runpod worker için basit YOLO sarmalayıcı.
    """

    def __init__(self, model_path: str):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model dosyası bulunamadı: {model_path}")

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = YOLO(model_path)
        self.model.to(self.device)

    def detect_defects(self, image: Image.Image) -> List[Dict]:
        """
        PIL Image üzerinde tespit yapar.
        Dönüş: [{bbox:[x1,y1,x2,y2], confidence, class_id, class}, ...]
        """
        # YOLO doğrudan PIL veya numpy alabiliyor
        results = self.model.predict(
            source=image, verbose=False, device=0 if self.device == "cuda" else "cpu"
        )
        if not results:
            return []

        result = results[0]
        detections: List[Dict] = []

        if hasattr(result, "boxes") and len(result.boxes) > 0:
            boxes = result.boxes
            for box in boxes:
                coords = box.xyxy[0].cpu().numpy()
                x1, y1, x2, y2 = coords
                conf = float(box.conf[0].cpu().numpy())
                class_id = int(box.cls[0].cpu().numpy())
                # Sınıf ismini bizim listeden eşle
                if 0 <= class_id < len(CLASS_NAMES):
                    class_name = CLASS_NAMES[class_id]
                else:
                    class_name = f"class_{class_id}"

                detections.append(
                    {
                        "bbox": [float(x1), float(y1), float(x2), float(y2)],
                        "confidence": conf,
                        "class_id": class_id,
                        "class": class_name,
                    }
                )

        return detections


