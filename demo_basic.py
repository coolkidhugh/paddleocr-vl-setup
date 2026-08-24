"""
PaddleOCR-VL-1.5 basic example.

Parses a single document image and writes JSON plus Markdown to output/.
"""

import os

from paddleocr import PaddleOCRVL

SAMPLE_IMAGE = (
    "https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/"
    "demo_image/paddleocr_vl_demo.png"
)


def main():
    print("=" * 50)
    print("PaddleOCR-VL-1.5 basic example")
    print("=" * 50)

    print("\n[1/3] Loading model...")
    pipeline = PaddleOCRVL()
    print("Model ready.")

    image_path = input(
        "\n[2/3] Image path (press Enter to use the sample image): "
    ).strip()
    if not image_path:
        image_path = SAMPLE_IMAGE

    print(f"\n[3/3] Processing: {image_path}")

    try:
        output = pipeline.predict(image_path)

        print("\n" + "=" * 50)
        print("Result")
        print("=" * 50)

        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        for i, res in enumerate(output, 1):
            print(f"\n--- page {i} ---")
            res.print()
            res.save_to_json(save_path=output_dir)
            res.save_to_markdown(save_path=output_dir)

        print(f"\nSaved to {output_dir}/")
        print("=" * 50)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
