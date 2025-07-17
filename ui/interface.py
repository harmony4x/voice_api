import gradio as gr

import os
from app.modules.processing import transcript_audio, save_transcript
from app.config import *


def proces_audio_to_doc (audio_path: str) -> str:
    """
    Nhận 1 file audio -> text
    :param audio_path:
    :return:
    """


    if not audio_path:
        raise ValueError("Không có âm thanh")

    transcript, _ = transcript_audio(audio_path, device=WHISPER_DEVICE,
                                     vad_filter=WHISPER_USE_VAD,
                                     beam_size=WHISPER_BEAM_SIZE,
                                     model_size=WHISPER_MODEL_SIZE)  # lấy phần tử đầu của tuple
    print(transcript)
    temp_path = "temp_transcript.txt"
    save_transcript(transcript, temp_path)

    return temp_path

# Xây dựng giao diện Gradio với output type là "filepath"
iface = gr.Interface(
    fn=proces_audio_to_doc,
    inputs=gr.Audio(type="filepath", label="Tải lên file audio"),
    outputs=gr.File(label="Tải xuống biên bản họp (.docx)"),
    title="Meeting Minutes Generator",
    description="Tải lên file audio để tạo biên bản cuộc họp (DOCX). Kết quả sẽ trả về đường dẫn tới file .docx."
)


if __name__ == "__main__":
    iface.launch()