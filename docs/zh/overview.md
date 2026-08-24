# PaddleOCR-VL-1.5 本地部署项目

## 📦 项目结构

```
paddleocr-vl-1.5-setup/
├── README.md                 # 快速入门指南
├── 使用指南.md               # 完整使用文档
├── 项目说明.md               # 本文件
├── requirements.txt          # Python 依赖
├── install.bat              # Windows 安装脚本
├── 快速开始.bat             # 一键启动菜单
├── 启动Web界面.bat          # Web UI 启动脚本
├── test_installation.py     # 安装测试脚本
├── demo_basic.py            # 基础示例
├── demo_transformers.py     # Transformers 示例
├── demo_batch.py            # 批量处理示例
└── demo_web_ui.py           # Web 界面示例
```

## 🚀 快速开始

### 方式 1: 一键启动（推荐）

双击运行 `快速开始.bat`，按照菜单提示操作：

1. 选择"1"安装 PaddleOCR-VL-1.5
2. 选择"2"测试安装
3. 选择"3-6"运行不同示例

### 方式 2: 命令行

```bash
# 1. 安装
python -m pip install paddlepaddle-gpu==3.2.1 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/
python -m pip install -U "paddleocr[doc-parser]"

# 2. 测试
python test_installation.py

# 3. 运行示例
python demo_basic.py
```

## 📚 使用示例

### 示例 1: 基础 OCR

```python
from paddleocr import PaddleOCRVL

pipeline = PaddleOCRVL()
output = pipeline.predict("test.png")

for res in output:
    res.print()
```

### 示例 2: 表格识别

```bash
paddleocr doc_parser -i table.png --task table
```

### 示例 3: Web 界面

```bash
python demo_web_ui.py
# 访问 http://localhost:7860
```

### 示例 4: 批量处理

```bash
python demo_batch.py
# 输入图片目录路径
```

## 🎯 核心功能

### 支持的任务

| 任务 | 说明 | 命令 |
|------|------|------|
| OCR | 通用文本识别 | `--task ocr` |
| Table | 表格识别 | `--task table` |
| Formula | 公式识别 | `--task formula` |
| Chart | 图表识别 | `--task chart` |
| Spotting | 文本定位 | `--task spotting` |
| Seal | 印章识别 | `--task seal` |

### 性能指标

- **准确率**: OmniDocBench v1.5 达到 94.5%
- **模型大小**: 0.9B 参数
- **推理速度**: 快速（具体取决于硬件）
- **支持语言**: 中文、英文、藏文、孟加拉语等

## 💡 使用技巧

### 1. 提高识别准确率

- 确保图片清晰度足够（推荐 1500px 以上）
- 对倾斜图片进行预处理
- 选择合适的任务类型
- 使用高质量的输入图片

### 2. 优化性能

- 使用 GPU 加速
- 启用 Flash Attention 2
- 使用 vLLM 推理服务器
- 批量处理时使用多进程

### 3. 处理特殊场景

- **扫描文档**: 自动适应，无需特殊处理
- **倾斜文档**: 支持不规则形状定位
- **多页文档**: 自动跨页合并
- **低光照**: 模型具有鲁棒性

## 🔧 配置选项

### GPU 配置

```python
# 指定 GPU
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

# 使用 CPU
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
```

### 输出格式

```python
# JSON 格式
res.save_to_json(save_path="output")

# Markdown 格式
res.save_to_markdown(save_path="output")

# 打印到控制台
res.print()
```

## 📊 性能对比

| 模型 | OmniDocBench v1.5 | 参数量 | 推理速度 |
|------|-------------------|--------|----------|
| PaddleOCR-VL-1.5 | **94.5%** | 0.9B | 快 |
| PaddleOCR-VL | 93.2% | 0.9B | 快 |
| 其他开源模型 | < 90% | > 1B | 慢 |

## 🐛 常见问题

### 安装问题

**Q: 安装失败**
- 检查 Python 版本 >= 3.8
- 升级 pip: `python -m pip install --upgrade pip`
- 使用国内镜像源

**Q: CUDA 版本不匹配**
- 检查 CUDA 版本: `nvidia-smi`
- 安装对应版本的 PaddlePaddle

### 运行问题

**Q: GPU 内存不足**
- 使用 CPU 版本
- 减小图片分辨率
- 使用 vLLM 服务器

**Q: 识别效果不好**
- 提高图片质量
- 选择正确的任务类型
- 检查图片是否清晰

## 📖 文档索引

- [README.md](README.md) - 快速入门
- [使用指南.md](使用指南.md) - 完整文档
- [官方文档](https://www.paddleocr.ai/)
- [Hugging Face](https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.5)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

Apache 2.0 License

## 🙏 致谢

感谢百度飞桨团队开发的 PaddleOCR-VL-1.5 模型。

---

**最后更新**: 2026-01-30  
**版本**: 1.0.0
