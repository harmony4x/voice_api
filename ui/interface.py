import gradio as gr
from PIL import Image

import os

from app.modules.processing import transcript_audio, save_transcript
from app.config import *


def proces_audio_to_doc (audio_path: str, api_key: str) -> str:
    """
    Nhận 1 file audio -> text
    :param api_key:
    :param audio_path:
    :return:
    """
    try:

        if not audio_path:
            raise ValueError("Không có âm thanh")

        transcript, _ = transcript_audio(audio_path, device=WHISPER_DEVICE,
                                         vad_filter=WHISPER_USE_VAD,
                                         beam_size=WHISPER_BEAM_SIZE,
                                         model_size=WHISPER_MODEL_SIZE)  # lấy phần tử đầu của tuple
        print(transcript)

        # Ghi file sau khi sửa từng dòng bằng Gemini
        temp_path = "temp_transcript.docx"
        save_transcript(transcript, temp_path, api_key=api_key)  # bên trong hàm này sẽ gọi Gemini từng dòng

        # kiểm tra file đã ghi thành công chưa
        if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
            raise RuntimeError("File rỗng hoặc chưa được ghi đúng.")

        return temp_path

    except Exception as e:
        # Ghi log lỗi
        with open("error.log", "a", encoding="utf-8") as f:
            f.write(f"Lỗi: {str(e)}\n")
        return "error.txt"  # hoặc trả về 1 file lỗi có sẵn

# Xây dựng giao diện Gradio với output type là "filepath"
# iface = gr.Interface(
#     fn=proces_audio_to_doc,
#     inputs=[gr.Audio(type="filepath", label="Tải lên file audio"), gr.Text(label="API Gemini")],
#     outputs=gr.File(label="Tải xuống biên bản họp (.docx)"),
#     title="Meeting Minutes Generator",
#     description="Tải lên file audio để tạo biên bản cuộc họp (DOCX). Kết quả sẽ trả về đường dẫn tới file .docx."
# )

with gr.Blocks() as iface:

    # Logo ở trên đầu
    gr.Image(
        value="../images/logo.jpg",
        width=100,
        height=100,
        show_label=False,
        show_download_button=False,
        elem_id="logo-img"
    )

    gr.Markdown("Tải lên file audio để tạo biên bản họp (.docx). Nhập API Gemini nếu muốn refine kết quả.")

    with gr.Row():
        with gr.Column(scale=1):
            audio_input = gr.Audio(type="filepath", label="🎵 Tải lên file audio")
            api_input = gr.Text(label="🔑 API Gemini (tuỳ chọn)")
            submit_btn = gr.Button("🚀 Submit")
        with gr.Column(scale=1):
            output_file = gr.File(label="📄 Tải xuống biên bản họp (.docx)")

    submit_btn.click(
        fn=proces_audio_to_doc,
        inputs=[audio_input, api_input],
        outputs=output_file
    )

if __name__ == "__main__":
    iface.launch()