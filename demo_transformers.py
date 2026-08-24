"""
PaddleOCR-VL-1.5 via Hugging Face Transformers.

Bypasses the PaddleOCR pipeline and drives the model directly, which is what you
want when integrating into an existing PyTorch stack.
"""

import os

import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForImageTextToText

MODEL_PATH = "PaddlePaddle/PaddleOCR-VL-1.5"

# Task prompts. The model switches behaviour based on this prefix.
PROMPTS = {
    "ocr": "OCR:",
    "table": "Table Recognition:",
    "formula": "Formula Recognition:",
    "chart": "Chart Recognition:",
    "spotting": "Spotting:",
    "seal": "Seal Recognition:",
}


def preprocess_image(image_path, task):
    """
    Load the image, upscaling for text spotting.

    Spotting predicts coordinates, so it needs more pixels than plain OCR.
    Below 1500px on both axes the results degrade noticeably, so double it.
    """
    image = Image.open(image_path).convert("RGB")
    orig_w, orig_h = image.size

    if task == "spotting" and orig_w < 1500 and orig_h < 1500:
        try:
            resample_filter = Image.Resampling.LANCZOS
        except AttributeError:  # Pillow < 9.1
            resample_filter = Image.LANCZOS
        image = image.resize((orig_w * 2, orig_h * 2), resample_filter)

    return image


def main():
    print("=" * 60)
    print("PaddleOCR-VL-1.5 via Transformers")
    print("=" * 60)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\nDevice: {device}")
    if device == "cuda":
        print(f"GPU: {torch.cuda.get_device_name(0)}")

    print("\n[1/4] Loading model...")
    print("      First run downloads roughly 2 GB.")

    try:
        model = (
            AutoModelForImageTextToText.from_pretrained(
                MODEL_PATH, torch_dtype=torch.bfloat16
            )
            .to(device)
            .eval()
        )
        processor = AutoProcessor.from_pretrained(MODEL_PATH)
        print("      Model ready.")
    except Exception as e:
        print(f"      Failed to load model: {e}")
        return

    print("\n[2/4] Task:")
    task_list = list(PROMPTS)
    for i, key in enumerate(task_list, 1):
        print(f"  {i}. {key:<9} ({PROMPTS[key]})")

    choice = input("\nTask number (1-6, default 1): ").strip()
    try:
        task = task_list[int(choice) - 1] if choice else "ocr"
    except (ValueError, IndexError):
        print("Not a valid number, falling back to ocr.")
        task = "ocr"
    print(f"      Task: {task}")

    image_path = input("\n[3/4] Image path: ").strip().strip('"')
    if not image_path or not os.path.exists(image_path):
        print("      Image not found.")
        return

    print(f"\n[4/4] Processing: {image_path}")

    try:
        image = preprocess_image(image_path, task)

        # Spotting needs a larger token budget for the coordinate output
        max_pixels = 2048 * 28 * 28 if task == "spotting" else 1280 * 28 * 28

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": PROMPTS[task]},
                ],
            }
        ]

        inputs = processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
            images_kwargs={
                "size": {
                    "shortest_edge": processor.image_processor.min_pixels,
                    "longest_edge": max_pixels,
                }
            },
        ).to(model.device)

        print("      Running inference...")
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=512)

        # Slice off the prompt tokens and the trailing EOS
        result = processor.decode(outputs[0][inputs["input_ids"].shape[-1] : -1])

        print("\n" + "=" * 60)
        print("Result")
        print("=" * 60)
        print(result)
        print("=" * 60)

        output_file = f"output_{task}.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"\nSaved to: {output_file}")

    except Exception as e:
        print(f"\nFailed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
