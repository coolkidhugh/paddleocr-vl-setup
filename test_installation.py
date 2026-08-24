"""
Verify a PaddleOCR-VL-1.5 installation.

Checks imports, reports GPU availability, then loads the model and runs one
inference against the official sample image.

GPU is reported for information only. A CPU-only install is a valid install and
will not fail this script.
"""

import sys

SAMPLE_IMAGE = (
    "https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/"
    "demo_image/paddleocr_vl_demo.png"
)


def test_imports():
    print("=" * 60)
    print("Dependencies")
    print("=" * 60)

    required = [
        ("Python", lambda: sys.version.split()[0]),
        ("PaddlePaddle", lambda: __import__("paddle").__version__),
        ("PaddleOCR", lambda: __import__("paddleocr").__version__),
        ("NumPy", lambda: __import__("numpy").__version__),
        ("Pillow", lambda: __import__("PIL").__version__),
    ]

    optional = [
        ("OpenCV", lambda: __import__("cv2").__version__),
    ]

    ok = True

    for name, get_version in required:
        try:
            print(f"  ok       {name}: {get_version()}")
        except Exception as e:
            print(f"  MISSING  {name}: {e}")
            ok = False

    for name, get_version in optional:
        try:
            print(f"  ok       {name}: {get_version()} (optional)")
        except Exception:
            print(f"  absent   {name} (optional, not required)")

    return ok


def report_gpu():
    """Report GPU status. Informational: never fails the run."""
    print("\n" + "=" * 60)
    print("GPU")
    print("=" * 60)

    try:
        import paddle

        if not paddle.is_compiled_with_cuda():
            print("  This PaddlePaddle build has no CUDA support. Running on CPU.")
            return

        print(f"  CUDA:  {paddle.version.cuda()}")
        print(f"  cuDNN: {paddle.version.cudnn()}")

        count = paddle.device.cuda.device_count()
        if count == 0:
            print("  CUDA build present, but no GPU detected. Running on CPU.")
            return

        print(f"  Devices: {count}")
        for i in range(count):
            print(f"    GPU {i}: {paddle.device.cuda.get_device_name(i)}")

    except Exception as e:
        print(f"  Could not query GPU status: {e}")


def test_model_and_inference():
    print("\n" + "=" * 60)
    print("Model load and inference")
    print("=" * 60)

    try:
        from paddleocr import PaddleOCRVL

        print("  Loading model. First run downloads it, which can take a few minutes.")
        pipeline = PaddleOCRVL()
        print("  Model loaded.")

        print("  Running inference on the sample image...")
        output = pipeline.predict(SAMPLE_IMAGE)
        print(f"  Inference ok. {len(output)} page(s) returned.")
        return True

    except Exception as e:
        print(f"  Failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    print("\n" + "=" * 60)
    print("PaddleOCR-VL-1.5 installation check")
    print("=" * 60 + "\n")

    results = {"Dependencies": test_imports()}
    report_gpu()
    results["Model and inference"] = test_model_and_inference()

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    for name, passed in results.items():
        print(f"  {'PASS' if passed else 'FAIL'}  {name}")

    all_passed = all(results.values())

    print("=" * 60)
    print(
        "Installation looks good."
        if all_passed
        else "Something is wrong. See the failures above."
    )
    print("=" * 60)

    return all_passed


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
