FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH=/app/models/f1.pt

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY handler.py model.py utils.py /app/
COPY models /app/models

CMD ["python", "handler.py"]


