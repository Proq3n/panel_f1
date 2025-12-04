import os
import sys
import traceback
from typing import Any, Dict, List

import runpod

from model import PanelDefectDetector
from utils import download_image, determine_cell_position

# Global model nesnesi
MODEL: PanelDefectDetector | None = None


def load_model() -> PanelDefectDetector:
    global MODEL
    if MODEL is not None:
        return MODEL

    model_path = os.getenv("MODEL_PATH", "/app/models/f1.pt")
    print(f"Model PATH: {model_path}")
    MODEL = PanelDefectDetector(model_path)
    print("Model yüklendi.")
    return MODEL


def handler(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Runpod serverless handler.
    Beklenen giriş:
    {
      "input": {
        "image_url": "...",
        "analysis_id": 123,
        "image_id": 456
      }
    }

    Çıkış:
    {
      "detections": [...],
      "image_dimensions": {"width": W, "height": H}
    }
    """
    try:
        input_data = event.get("input", {}) or {}
        image_url = input_data.get("image_url")
        analysis_id = input_data.get("analysis_id")
        image_id = input_data.get("image_id")

        if not image_url:
            return {"status_code": 400, "error": "image_url gerekli"}

        print(f"Handler başladı. analysis_id={analysis_id}, image_id={image_id}")

        model = load_model()

        image = download_image(image_url)
        img_width, img_height = image.size

        raw_detections = model.detect_defects(image)
        detections: List[Dict[str, Any]] = []

        for det in raw_detections:
            bbox = det["bbox"]
            x1, y1, x2, y2 = bbox
            conf = float(det["confidence"])
            class_name = det["class"]
            class_id = det.get("class_id", 0)

            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            cell_position = determine_cell_position(center_x, center_y, img_width, img_height)

            detections.append(
                {
                    "bbox": bbox,
                    "confidence": conf,
                    "class": class_name,
                    "class_id": class_id,
                    "cell_position": cell_position,
                }
            )

        print(f"Toplam tespit: {len(detections)}")

        return {
            "status_code": 200,
            "analysis_id": analysis_id,
            "image_id": image_id,
            "image_dimensions": {"width": img_width, "height": img_height},
            "detections": detections,
        }
    except Exception as e:
        print(f"Handler hatası: {e}")
        traceback.print_exc()
        return {"status_code": 500, "error": str(e)}


if __name__ == "__main__":
    print("Runpod serverless handler başlatılıyor...")
    runpod.serverless.start({"handler": handler})


