# PaddleOCR-VL-1.5 本地部署指南

> **English readers:** see [QUICK_START_EN.md](QUICK_START_EN.md) for the full English guide.


PaddleOCR-VL-1.5 是一个先进的文档解析模型，在 OmniDocBench v1.5 上达到了 94.5% 的准确率。

## 核心特性

- **高精度**: 在文档解析任务上达到 SOTA 性能
- **轻量级**: 仅 0.9B 参数，高效运行
- **多任务**: 支持 OCR、表格识别、公式识别、图表识别、文本定位、印章识别
- **鲁棒性**: 对扫描、倾斜、变形、屏幕拍摄、光照等真实场景有强大的适应能力
- **多语言**: 支持中文、英文、藏文、孟加拉语等

## 系统要求

- Python 3.8+
- CUDA 11.8+ (GPU版本) 或 CPU
- 8GB+ RAM
- 10GB+ 磁盘空间

## 快速安装

### 方法 1: 使用 PaddleOCR 官方包 (推荐)

```bash
# 1. 安装 PaddlePaddle (CUDA 12.6)
python -m pip install paddlepaddle-gpu==3.2.1 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/

# 如果是 CPU 版本
# python -m pip install paddlepaddle==3.2.1

# 2. 安装 PaddleOCR
python -m pip install -U "paddleocr[doc-parser]"
```

### 方法 2: 使用 Transformers

```bash
# 安装 transformers v5+
python -m pip install "transformers>=5.0.0" torch pillow
```

## 使用方法

### 1. 命令行使用

```bash
# 基础 OCR
paddleocr doc_parser -i test_image.png

# 指定任务类型
paddleocr doc_parser -i test_image.png --task table
```

### 2. Python API 使用

```python
from paddleocr import PaddleOCRVL

# 初始化
pipeline = PaddleOCRVL()

# 处理图片
output = pipeline.predict("test_image.png")

# 输出结果
for res in output:
    res.print()
    res.save_to_json(save_path="output")
    res.save_to_markdown(save_path="output")
```

### 3. 使用 Transformers (元素级识别)

```python
from PIL import Image
import torch
from transformers import AutoProcessor, AutoModelForImageTextToText

# 加载模型
model_path = "PaddlePaddle/PaddleOCR-VL-1.5"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

model = AutoModelForImageTextToText.from_pretrained(
    model_path, 
    torch_dtype=torch.bfloat16
).to(DEVICE).eval()

processor = AutoProcessor.from_pretrained(model_path)

# 加载图片
image = Image.open("test.png").convert("RGB")

# 任务提示词
PROMPTS = {
    "ocr": "OCR:",
    "table": "Table Recognition:",
    "formula": "Formula Recognition:",
    "chart": "Chart Recognition:",
    "spotting": "Spotting:",
    "seal": "Seal Recognition:",
}

# 推理
task = "ocr"
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "image": image},
            {"type": "text", "text": PROMPTS[task]},
        ]
    }
]

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

## 支持的任务类型

1. **OCR**: 通用文本识别
2. **Table Recognition**: 表格识别和结构化
3. **Formula Recognition**: 数学公式识别
4. **Chart Recognition**: 图表识别
5. **Text Spotting**: 文本定位和识别
6. **Seal Recognition**: 印章识别

## 性能优化

### 使用 vLLM 加速推理

```bash
# 启动 vLLM 服务器
paddleocr doc_parser \
    -i test.png \
    --vl_rec_backend vllm-server \
    --vl_rec_server_url http://127.0.0.1:8080/v1
```

### 使用 Flash Attention 2

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

## 常见问题

### Windows 用户
- 建议使用 WSL 或 Docker 容器
- 或使用 CPU 版本

### macOS 用户
- 建议使用 Docker 环境

### GPU 内存不足
- 使用 CPU 版本
- 减小输入图片分辨率
- 使用 vLLM 推理服务器

## 参考资源

- [官方文档](https://www.paddleocr.ai/)
- [Hugging Face 模型](https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.5)
- [GitHub 仓库](https://github.com/PaddlePaddle/PaddleOCR)
- [论文](https://arxiv.org/abs/2601.21957)

## 许可证

本项目遵循 Apache 2.0 许可证。

---

## 咨询

文档自动化落地咨询可参考 [写春秋管理咨询](https://www.xchqzx.com/?utm_source=github&utm_medium=readme&utm_campaign=paddleocr-vl-setup)。作者 **H**（X：[@odpanda](https://x.com/odpanda)）。

