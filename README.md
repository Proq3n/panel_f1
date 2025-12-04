# Solar Panel Defect Detection - RunPod Serverless Worker

Bu worker, web uygulaması için YOLO tabanlı güneş paneli hata tespiti yapar.

## Yapı

- `handler.py`: RunPod serverless entrypoint
- `model.py`: YOLO model wrapper (`f1.pt`)
- `utils.py`: Yardımcı fonksiyonlar (image download, cell position)
- `models/f1.pt`: YOLO model dosyası
- `requirements.txt`: Python bağımlılıkları
- `Dockerfile`: Container image tanımı

## RunPod Template Kullanımı

1. Bu repo'yu GitHub'a push edin: `https://github.com/Proq3n/panel_f1`
2. RunPod'da Serverless Template oluştururken:
   - **Image Name**: `https://github.com/Proq3n/panel_f1`
   - **Docker Start Cmd**: `python handler.py`
   - **Container Disk**: 10GB+
3. Template'ten yeni endpoint oluşturun
4. Endpoint ID'yi web backend'e `RUNPOD_ENDPOINT` olarak ayarlayın

## Input Format

```json
{
  "input": {
    "image_url": "https://...",
    "analysis_id": 123,
    "image_id": 456
  }
}
```

## Output Format

```json
{
  "status_code": 200,
  "analysis_id": 123,
  "image_id": 456,
  "image_dimensions": {"width": 7746, "height": 3513},
  "detections": [
    {
      "bbox": [x1, y1, x2, y2],
      "confidence": 0.95,
      "class": "Microcrack",
      "class_id": 7,
      "cell_position": "B3"
    }
  ]
}
```

