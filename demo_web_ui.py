"""
PaddleOCR-VL-1.5 web UI.

Minimal Gradio front end for trying the model without writing code.
Binds to 0.0.0.0:7860, so it is reachable from other machines on the network.
"""

import json

try:
    import gradio as gr
except ImportError:
    print("Gradio is not installed. Install it with: pip install gradio")
    raise SystemExit(1)

from paddleocr import PaddleOCRVL

# Loaded lazily on first request, then reused
pipeline = None


def initialize_model():
    global pipeline
    if pipeline is None:
        print("Loading model...")
        pipeline = PaddleOCRVL()
        print("Model ready.")
    return pipeline


def process_image(image, output_format="text"):
    if not image:
        return "No image provided."

    try:
        model = initialize_model()
        output = model.predict(image)

        results = []
        for i, res in enumerate(output, 1):
            if output_format == "json":
                results.append(
                    json.dumps({"page": i, "content": str(res)}, ensure_ascii=False, indent=2)
                )
            else:
                results.append(f"=== page {i} ===\n{res}\n")

        return "\n".join(results)

    except Exception as e:
        return f"Error: {e}"


def create_ui():
    with gr.Blocks(title="PaddleOCR-VL-1.5") as demo:
        gr.Markdown(
            """
            # PaddleOCR-VL-1.5 document parsing

            Upload an image to parse. Handles plain text, tables, formulas,
            charts, text spotting, and seals.
            """
        )

        with gr.Row():
            with gr.Column():
                image_input = gr.Image(label="Image", type="filepath")

                output_format = gr.Radio(
                    choices=["text", "json"],
                    value="text",
                    label="Output format",
                )

                submit_btn = gr.Button("Run", variant="primary")

                gr.Markdown(
                    """
                    ### Supported tasks
                    - Text recognition (OCR)
                    - Table recognition
                    - Formula recognition
                    - Chart recognition
                    - Text spotting
                    - Seal recognition
                    """
                )

            with gr.Column():
                output_text = gr.Textbox(label="Result", lines=20, max_lines=30)

        submit_btn.click(
            fn=process_image,
            inputs=[image_input, output_format],
            outputs=output_text,
        )

        gr.Markdown(
            """
            ---
            ### Notes
            - The model loads on the first request, so expect a delay the first time.
            - 0.9B parameters, 94.5% on OmniDocBench v1.5.
            - Multilingual: Chinese, English, Tibetan, Bengali, and others.
            - Robust to scanning artifacts, skew, warping, and photographs of screens.
            """
        )

    return demo


def main():
    print("=" * 60)
    print("PaddleOCR-VL-1.5 web UI")
    print("=" * 60)
    print("\nStarting server on http://localhost:7860")

    demo = create_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        inbrowser=True,
    )


if __name__ == "__main__":
    main()
