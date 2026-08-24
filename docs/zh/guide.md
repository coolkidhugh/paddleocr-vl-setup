# PaddleOCR-VL-1.5 完整使用指南

## 📋 目录

1. [简介](#简介)
2. [安装步骤](#安装步骤)
3. [使用方法](#使用方法)
4. [高级功能](#高级功能)
5. [性能优化](#性能优化)
6. [常见问题](#常见问题)
7. [实战案例](#实战案例)

## 简介

PaddleOCR-VL-1.5 是百度飞桨团队开发的新一代文档解析模型，具有以下特点：

### 核心优势

- **SOTA 性能**: OmniDocBench v1.5 达到 94.5% 准确率
- **轻量高效**: 仅 0.9B 参数，推理速度快
- **多任务支持**: 
  - 📝 OCR 文本识别
  - 📊 表格识别与结构化
  - 🔢 数学公式识别
  - 📈 图表识别
  - 🎯 文本定位（Spotting）
  - 🔖 印章识别
- **强鲁棒性**: 适应扫描、倾斜、变形、屏幕拍摄、光照变化等真实场景
- **多语言**: 支持中文、英文、藏文、孟加拉语等

### 技术亮点

1. **不规则形状定位**: 支持多边形检测，适应倾斜和变形文档
2. **跨页处理**: 自动合并跨页表格和段落标题
3. **专业场景**: 增强对生僻字、古文、多语言表格、下划线、复选框的识别

## 安装步骤

### 方式一：一键安装（推荐）

Windows 用户直接运行：
```bash
快速开始.bat
```

选择"1. 安装 PaddleOCR-VL-1.5"

### 方式二：手动安装

#### 1. 安装 PaddlePaddle

**GPU 版本 (CUDA 12.6)**
```bash
python -m pip install paddlepaddle-gpu==3.2.1 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/
```

**GPU 版本 (CUDA 11.8)**
```bash
python -m pip install paddlepaddle-gpu==3.2.1 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/
```

**CPU 版本**
```bash
python -m pip install paddlepaddle==3.2.1
```

#### 2. 安装 PaddleOCR

```bash
python -m pip install -U "paddleocr[doc-parser]"
```

#### 3. 测试安装

```bash
python test_installation.py
```

## 使用方法

### 1. 命令行使用

最简单的使用方式：

```bash
# 基础 OCR
paddleocr doc_parser -i test.png

# 表格识别
paddleocr doc_parser -i table.png --task table

# 公式识别
paddleocr doc_parser -i formula.png --task formula
```

### 2. Python API 使用

```python
from paddleocr import PaddleOCRVL

# 初始化
pipeline = PaddleOCRVL()

# 处理单张图片
output = pipeline.predict("test.png")

# 输出结果
for res in output:
    res.print()  # 打印到控制台
    res.save_to_json(save_path="output")  # 保存为 JSON
    res.save_to_markdown(save_path="output")  # 保存为 Markdown
```

### 3. 批量处理

```bash
python demo_batch.py
```

或在代码中：

```python
from pathlib import Path
from paddleocr import PaddleOCRVL

pipeline = PaddleOCRVL()

# 批量处理目录中的所有图片
image_dir = Path("images")
for image_path in image_dir.glob("*.png"):
    output = pipeline.predict(str(image_path))
    # 处理结果...
```

### 4. Web 界面

启动 Web 界面进行可视化操作：

```bash
python demo_web_ui.py
```

或运行：
```bash
启动Web界面.bat
```

浏览器访问 http://localhost:7860

## 高级功能

### 1. 使用 Transformers 库

适合需要更灵活控制的场景：

```python
from PIL import Image
import torch
from transformers import AutoProcessor, AutoModelForImageTextToText

# 加载模型
model_path = "PaddlePaddle/PaddleOCR-VL-1.5"
model = AutoModelForImageTextToText.from_pretrained(
    model_path, 
    torch_dtype=torch.bfloat16
).to("cuda").eval()

processor = AutoProcessor.from_pretrained(model_path)

# 处理图片
image = Image.open("test.png").convert("RGB")

messages = [{
    "role": "user",
    "content": [
        {"type": "image", "image": image},
        {"type": "text", "text": "OCR:"},
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

### 2. 不同任务类型

```python
TASKS = {
    "ocr": "OCR:",                      # 通用文本识别
    "table": "Table Recognition:",      # 表格识别
    "formula": "Formula Recognition:",  # 公式识别
    "chart": "Chart Recognition:",      # 图表识别
    "spotting": "Spotting:",           # 文本定位
    "seal": "Seal Recognition:",       # 印章识别
}

# 使用不同任务
task = "table"
messages[0]["content"][1]["text"] = TASKS[task]
```

### 3. 处理 PDF 文档

```python
from pdf2image import convert_from_path
from paddleocr import PaddleOCRVL

# 转换 PDF 为图片
images = convert_from_path("document.pdf")

# 初始化模型
pipeline = PaddleOCRVL()

# 处理每一页
for i, image in enumerate(images):
    # 保存临时图片
    temp_path = f"temp_page_{i}.png"
    image.save(temp_path)
    
    # 识别
    output = pipeline.predict(temp_path)
    
    # 保存结果
    for res in output:
        res.save_to_markdown(save_path=f"output/page_{i}")
```

## 性能优化

### 1. 使用 vLLM 加速推理

启动 vLLM 服务器：

```bash
# 方法 1: 使用 PaddleOCR CLI
paddleocr doc_parser \
    -i test.png \
    --vl_rec_backend vllm-server \
    --vl_rec_server_url http://127.0.0.1:8080/v1
```

```python
# 方法 2: Python API
from paddleocr import PaddleOCRVL

pipeline = PaddleOCRVL(
    vl_rec_backend="vllm-server",
    vl_rec_server_url="http://127.0.0.1:8080/v1"
)
```

### 2. 使用 Flash Attention 2

```bash
pip install flash-attn --no-build-isolation
```

```python
model = AutoModelForImageTextToText.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,
    attn_implementation="flash_attention_2"
).to("cuda").eval()
```

### 3. 批量推理优化

```python
# 使用批处理
images = ["img1.png", "img2.png", "img3.png"]

# 并行处理
from concurrent.futures import ThreadPoolExecutor

def process_image(img_path):
    return pipeline.predict(img_path)

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_image, images))
```

### 4. 内存优化

```python
import torch

# 使用混合精度
with torch.cuda.amp.autocast():
    outputs = model.generate(**inputs)

# 清理缓存
torch.cuda.empty_cache()
```

## 常见问题

### Q1: 安装失败怎么办？

**A**: 
1. 确保 Python 版本 >= 3.8
2. 升级 pip: `python -m pip install --upgrade pip`
3. 使用国内镜像源
4. Windows 用户建议使用 WSL 或 Docker

### Q2: GPU 内存不足

**A**:
1. 使用 CPU 版本
2. 减小输入图片分辨率
3. 使用 vLLM 推理服务器
4. 启用混合精度训练

### Q3: 识别效果不好

**A**:
1. 确保图片清晰度足够
2. 对于倾斜图片，先进行旋转校正
3. 调整图片分辨率（推荐 1500px 以上）
4. 选择合适的任务类型

### Q4: 如何处理多页文档？

**A**:
```python
# 模型自动支持跨页表格合并和段落识别
output = pipeline.predict("multi_page.pdf")
```

### Q5: 支持哪些图片格式？

**A**: 支持常见格式：PNG, JPG, JPEG, BMP, TIFF, WebP

## 实战案例

### 案例 1: 发票识别

```python
from paddleocr import PaddleOCRVL
import json

pipeline = PaddleOCRVL()

# 识别发票
output = pipeline.predict("invoice.png")

# 提取关键信息
for res in output:
    # 保存为结构化数据
    res.save_to_json(save_path="invoice_data")
    
    # 可以进一步解析 JSON 提取字段
    with open("invoice_data/result.json", "r") as f:
        data = json.load(f)
        # 提取发票号、金额等信息
```

### 案例 2: 表格数据提取

```python
# 识别表格
output = pipeline.predict("table.png")

# 保存为 Markdown（包含表格结构）
for res in output:
    res.save_to_markdown(save_path="table_output")
    
# 可以进一步转换为 Excel
import pandas as pd
# 解析 Markdown 表格并转换为 DataFrame
```

### 案例 3: 学术论文解析

```python
# 处理包含公式和图表的论文
output = pipeline.predict("paper.pdf")

for res in output:
    # 保存完整结构
    res.save_to_markdown(save_path="paper_output")
    
    # Markdown 中会包含：
    # - 文本内容
    # - LaTeX 格式的公式
    # - 表格结构
    # - 图表描述
```

### 案例 4: 批量文档处理系统

```python
import os
from pathlib import Path
from paddleocr import PaddleOCRVL
from concurrent.futures import ProcessPoolExecutor

def process_document(doc_path):
    """处理单个文档"""
    pipeline = PaddleOCRVL()
    output = pipeline.predict(str(doc_path))
    
    # 保存结果
    output_dir = f"output/{doc_path.stem}"
    os.makedirs(output_dir, exist_ok=True)
    
    for res in output:
        res.save_to_json(save_path=output_dir)
        res.save_to_markdown(save_path=output_dir)
    
    return doc_path.name

# 批量处理
doc_dir = Path("documents")
doc_files = list(doc_dir.glob("*.png")) + list(doc_dir.glob("*.pdf"))

with ProcessPoolExecutor(max_workers=4) as executor:
    results = executor.map(process_document, doc_files)
    
    for result in results:
        print(f"✓ 处理完成: {result}")
```

## 参考资源

- [官方文档](https://www.paddleocr.ai/)
- [Hugging Face 模型](https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.5)
- [GitHub 仓库](https://github.com/PaddlePaddle/PaddleOCR)
- [论文](https://arxiv.org/abs/2601.21957)
- [AMD 优化指南](https://www.amd.com/en/developer/resources/technical-articles/2026/unlocking-high-performance-document-parsing-of-paddleocr-vl-1-5-.html)

## 技术支持

如有问题，可以：
1. 查看官方文档
2. 在 GitHub 提 Issue
3. 加入飞桨社区讨论

---

**版本**: PaddleOCR-VL-1.5  
**更新日期**: 2026-01  
**许可证**: Apache 2.0
