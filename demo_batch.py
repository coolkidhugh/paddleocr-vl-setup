"""
PaddleOCR-VL-1.5 batch example.

Processes every image in a directory, writes one output folder per file, and
records a batch_summary.json with per-file status.

    python demo_batch.py <input_dir> [output_dir]
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

from paddleocr import PaddleOCRVL

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"}


def find_images(input_dir):
    """Return every supported image directly under `input_dir`, without duplicates."""
    return sorted(
        {
            p
            for p in Path(input_dir).iterdir()
            if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
        }
    )


def process_batch(input_dir, output_dir="batch_output"):
    print("=" * 60)
    print("PaddleOCR-VL-1.5 batch processing")
    print("=" * 60)

    if not os.path.isdir(input_dir):
        print(f"Input directory not found: {input_dir}")
        return

    os.makedirs(output_dir, exist_ok=True)

    image_files = find_images(input_dir)
    if not image_files:
        print(f"No images found in: {input_dir}")
        return

    print(f"\nFound {len(image_files)} image(s).")

    print("\nLoading model...")
    pipeline = PaddleOCRVL()
    print("Model ready.\n")

    summary = {
        "total": len(image_files),
        "success": 0,
        "failed": 0,
        "start_time": datetime.now().isoformat(),
        "files": [],
    }

    for i, image_path in enumerate(image_files, 1):
        print(f"[{i}/{len(image_files)}] {image_path.name}")

        try:
            output = pipeline.predict(str(image_path))

            file_output_dir = os.path.join(output_dir, image_path.stem)
            os.makedirs(file_output_dir, exist_ok=True)

            for res in output:
                res.save_to_json(save_path=file_output_dir)
                res.save_to_markdown(save_path=file_output_dir)

            print(f"        ok -> {file_output_dir}/")
            summary["success"] += 1
            summary["files"].append(
                {
                    "name": image_path.name,
                    "status": "success",
                    "output_dir": file_output_dir,
                }
            )

        except Exception as e:
            print(f"        failed: {e}")
            summary["failed"] += 1
            summary["files"].append(
                {"name": image_path.name, "status": "failed", "error": str(e)}
            )

    summary["end_time"] = datetime.now().isoformat()
    summary_file = os.path.join(output_dir, "batch_summary.json")

    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print("Batch complete")
    print("=" * 60)
    print(f"Total:   {summary['total']}")
    print(f"Success: {summary['success']}")
    print(f"Failed:  {summary['failed']}")
    print(f"\nSummary: {summary_file}")
    print("=" * 60)


def main():
    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "batch_output"
    else:
        input_dir = input("Image directory: ").strip().strip('"')
        output_dir = input("Output directory (default batch_output): ").strip() or "batch_output"

    process_batch(input_dir, output_dir)


if __name__ == "__main__":
    main()
