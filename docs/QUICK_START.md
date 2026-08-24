# PaddleOCR-VL-1.5 Quick Start Guide

## 🎯 What is PaddleOCR-VL-1.5?

PaddleOCR-VL-1.5 is a state-of-the-art document parsing model that achieves **94.5% accuracy** on OmniDocBench v1.5 with only **0.9B parameters**.

### Key Features

✅ **High Accuracy**: SOTA performance on document parsing  
✅ **Lightweight**: Only 0.9B parameters, fast inference  
✅ **Multi-Task**: OCR, Table, Formula, Chart, Spotting, Seal recognition  
✅ **Robust**: Handles scanning, skew, warping, screen photography, illumination  
✅ **Multilingual**: Chinese, English, Tibetan, Bengali, etc.

## 🚀 Installation

### Option 1: Quick Install (Recommended)

```bash
# Install PaddlePaddle (GPU - CUDA 12.6)
python -m pip install paddlepaddle-gpu==3.2.1 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/

# Install PaddleOCR
python -m pip install -U "paddleocr[doc-parser]"
```

### Option 2: CPU Version

```bash
# Install PaddlePaddle (CPU)
python -m pip install paddlepaddle==3.2.1

# Install PaddleOCR
python -m pip install -U "paddleocr[doc-parser]"
```

### Option 3: Using Transformers

```bash
pip install "transformers>=5.0.0" torch pillow
```

## 📝 Basic Usage

### Command Line

```bash
# Basic OCR
paddleocr doc_parser -i test.png

# Table recognition
paddleocr doc_parser -i table.png --task table

# Formula recognition
paddleocr doc_parser -i formula.png --task formula
```

### Python API

```python
from paddleocr import PaddleOCRVL

# Initialize
pipeline = PaddleOCRVL()

# Process image
output = pipeline.predict("test.png")

# Output results
for res in output:
    res.print()
    res.save_to_json(save_path="output")
    res.save_to_markdown(save_path="output")
```

### Using Transformers

```python
from PIL import Image
import torch
from transformers import AutoProcessor, AutoModelForImageTextToText

# Load model
model_path = "PaddlePaddle/PaddleOCR-VL-1.5"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

model = AutoModelForImageTextToText.from_pretrained(
    model_path, 
    torch_dtype=torch.bfloat16
).to(DEVICE).eval()

processor = AutoProcessor.from_pretrained(model_path)

# Load image
image = Image.open("test.png").convert("RGB")

# Task prompts
PROMPTS = {
    "ocr": "OCR:",
    "table": "Table Recognition:",
    "formula": "Formula Recognition:",
    "chart": "Chart Recognition:",
    "spotting": "Spotting:",
    "seal": "Seal Recognition:",
}

# Inference
task = "ocr"
messages = [{
    "role": "user",
    "content": [
        {"type": "image", "image": image},
        {"type": "text", "text": PROMPTS[task]},
    ]
}]

inputs = processor.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
).to(model.device)

outputs = model.generate(**inputs, max_new_tokens=512)
result = processor.decode(outputs[0][inputs["input_ids"].shape[-1]:-1])
print(result)
```

## 🎨 Supported Tasks

| Task | Description | Prompt |
|------|-------------|--------|
| OCR | General text recognition | `OCR:` |
| Table | Table recognition & structuring | `Table Recognition:` |
| Formula | Mathematical formula recognition | `Formula Recognition:` |
| Chart | Chart recognition | `Chart Recognition:` |
| Spotting | Text localization & recognition | `Spotting:` |
| Seal | Seal recognition | `Seal Recognition:` |

## ⚡ Performance Optimization

### 1. Use vLLM for Faster Inference

```bash
paddleocr doc_parser \
    -i test.png \
    --vl_rec_backend vllm-server \
    --vl_rec_server_url http://127.0.0.1:8080/v1
```

### 2. Use Flash Attention 2

```bash
pip install flash-attn --no-build-isolation
```

```python
model = AutoModelForImageTextToText.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,
    attn_implementation="flash_attention_2"
).to(DEVICE).eval()
```

### 3. Batch Processing

```python
from pathlib import Path
from paddleocr import PaddleOCRVL

pipeline = PaddleOCRVL()

# Process all images in directory
for image_path in Path("images").glob("*.png"):
    output = pipeline.predict(str(image_path))
    # Process results...
```

## 🔧 Advanced Usage

### Process PDF Documents

```python
from pdf2image import convert_from_path
from paddleocr import PaddleOCRVL

# Convert PDF to images
images = convert_from_path("document.pdf")

# Initialize model
pipeline = PaddleOCRVL()

# Process each page
for i, image in enumerate(images):
    temp_path = f"temp_page_{i}.png"
    image.save(temp_path)
    
    output = pipeline.predict(temp_path)
    
    for res in output:
        res.save_to_markdown(save_path=f"output/page_{i}")
```

### Custom Configuration

```python
import os

# Specify GPU
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

# Use CPU
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
```

## 📊 Performance Benchmarks

| Model | OmniDocBench v1.5 | Parameters | Speed |
|-------|-------------------|------------|-------|
| **PaddleOCR-VL-1.5** | **94.5%** | 0.9B | Fast |
| PaddleOCR-VL | 93.2% | 0.9B | Fast |
| Other OSS Models | < 90% | > 1B | Slow |

## ❓ FAQ

### Q: Installation fails?
**A**: 
- Ensure Python >= 3.8
- Upgrade pip: `python -m pip install --upgrade pip`
- Use mirror sources for faster download

### Q: GPU out of memory?
**A**:
- Use CPU version
- Reduce image resolution
- Use vLLM inference server
- Enable mixed precision

### Q: Poor recognition results?
**A**:
- Ensure image clarity (recommend 1500px+)
- Rotate skewed images first
- Choose appropriate task type
- Use high-quality input images

## 📚 Resources

- [Official Documentation](https://www.paddleocr.ai/)
- [Hugging Face Model](https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.5)
- [GitHub Repository](https://github.com/PaddlePaddle/PaddleOCR)
- [Research Paper](https://arxiv.org/abs/2601.21957)

## 📄 License

Apache 2.0 License

## 🙏 Acknowledgments

Thanks to the PaddlePaddle team for developing PaddleOCR-VL-1.5.

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-30
