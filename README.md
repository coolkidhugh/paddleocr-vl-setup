# PaddleOCR-VL Setup

A working deployment kit for **PaddleOCR-VL-1.5**, the 0.9B document parsing model that scores 94.5% on OmniDocBench v1.5.

The model is good. Getting it running is the annoying part: which PaddlePaddle build matches your CUDA, whether to use the pipeline API or drive it through Transformers, and how to confirm the install actually works before you build on top of it. This repo covers that.

> 中文文档见 [docs/zh/README.md](docs/zh/README.md)

---

## What the model does

One model handles six tasks, selected by prompt prefix:

| Task | Prompt |
|---|---|
| Text recognition | `OCR:` |
| Table recognition | `Table Recognition:` |
| Formula recognition | `Formula Recognition:` |
| Chart recognition | `Chart Recognition:` |
| Text spotting (text plus coordinates) | `Spotting:` |
| Seal recognition | `Seal Recognition:` |

Multilingual, including Chinese, English, Tibetan and Bengali. Robust against the things that break ordinary OCR: skew, warping, photographs of screens, uneven lighting.

---

## Install

**Windows:** run `install.bat` and pick your build. Or do it manually:

```bash
# GPU, CUDA 12.6
python -m pip install paddlepaddle-gpu==3.2.1 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/

# GPU, CUDA 11.8
python -m pip install paddlepaddle-gpu==3.2.1 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/

# CPU
python -m pip install paddlepaddle==3.2.1
```

Then:

```bash
python -m pip install -U "paddleocr[doc-parser]"
```

Verify before building anything on top:

```bash
python test_installation.py
```

It checks imports, reports GPU status, loads the model, and runs one real inference. **GPU is reported for information only.** A CPU-only install is valid and passes.

---

## Run

`start.bat` is a menu over everything below. Or call the scripts directly:

| Script | What it does |
|---|---|
| `demo_basic.py` | One image through the pipeline API, saves JSON and Markdown |
| `demo_batch.py` | A whole folder, one output directory per file, plus `batch_summary.json` |
| `demo_transformers.py` | Drives the model through Hugging Face Transformers, with task selection |
| `demo_web_ui.py` | Gradio UI on port 7860 |
| `test_installation.py` | Installation check |

```bash
python demo_basic.py
python demo_batch.py ./scans ./results
python demo_web_ui.py
```

---

## Two ways to call it

**Pipeline API.** Less code, saves structured output directly:

```python
from paddleocr import PaddleOCRVL

pipeline = PaddleOCRVL()
for res in pipeline.predict("invoice.png"):
    res.save_to_json(save_path="output")
    res.save_to_markdown(save_path="output")
```

**Transformers.** More control, and the right choice when fitting into an existing PyTorch stack:

```python
from transformers import AutoProcessor, AutoModelForImageTextToText

model = AutoModelForImageTextToText.from_pretrained(
    "PaddlePaddle/PaddleOCR-VL-1.5", torch_dtype=torch.bfloat16
).to("cuda").eval()
processor = AutoProcessor.from_pretrained("PaddlePaddle/PaddleOCR-VL-1.5")
```

See `demo_transformers.py` for the full call including the chat template.

---

## Two things worth knowing

**Text spotting needs more pixels than plain OCR.** Spotting predicts coordinates, and below roughly 1500px on both axes accuracy drops noticeably. `demo_transformers.py` upscales 2x automatically for that task, and raises the pixel budget from `1280 * 28 * 28` to `2048 * 28 * 28`.

**The first run downloads the model**, roughly 2 GB through Transformers. Expect a wait, and do not mistake it for a hang.

---

## Layout

```
├── install.bat              guided install (Windows)
├── start.bat                menu over everything below
├── run_web_ui.bat           launch the Gradio UI
├── test_installation.py     verify the install end to end
├── demo_basic.py            single image, pipeline API
├── demo_batch.py            folder, with a per-file summary
├── demo_transformers.py     Transformers path, six tasks
├── demo_web_ui.py           Gradio UI
└── docs/
    ├── QUICK_START.md       fuller English guide
    └── zh/                  中文文档
```

---

## Links

- Model: [PaddlePaddle/PaddleOCR-VL-1.5](https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.5)
- PaddleOCR: [github.com/PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)

The model and PaddleOCR carry their own licenses. This repo is the setup and demo code around them.

## License

MIT

---

## Consulting

Document-automation rollout questions? Soft intro via [写春秋管理咨询](https://www.xchqzx.com/?utm_source=github&utm_medium=readme&utm_campaign=paddleocr-vl-setup). Author: **H** ([@odpanda](https://x.com/odpanda)).

