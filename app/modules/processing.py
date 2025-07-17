import os
from  faster_whisper import WhisperModel, BatchedInferencePipeline
import re



def clean_text(text: str) -> str:
    """
    Thực hiện tiền xử lý văn bản:
      - Loại bỏ khoảng trắng thừa giữa các từ.
      - Cắt bỏ khoảng trắng đầu/cuối.
    Có thể mở rộng thêm các bước xử lý (ví dụ: chuẩn hóa dấu câu) nếu cần.
    """
    text = re.sub(r'\s+', ' ', text)
    return text.strip()





def preprocess_transcript(segments: list):
    """
    Tiền xử lý transcript, trả về dict với data:
    -text: đoạn văn được transcript
    """

    processed_segments = []
    for segment in segments:
        processed_segments.append({
            'start': segment.start,
            'end': segment.end,
            'text': segment.text,
        })

    return processed_segments


def transcript_audio (
        input_audio: str = "audio.mp3",
        model_size: str = "base",
        device: str = "cpu",
        compute_type: str = "int8",
        beam_size: int = 8,
        vad_filter: bool = False,
):
    """
    
    :param input_audio: 
    :param model_size: 
    :param device: 
    :param compute_type:  float 16,32 (chứa nhiều thông tin -> chính xác hơn)
    :param beam_size:  tăng độ chính xác
    :param vad_filter: nhận diện xem có giọng nói trong file không
    :return: 
    """

    if not os.path.exists(input_audio):
        raise FileNotFoundError(f"File '{input_audio}' không tồn tại.")

        # Khởi tạo model Faster Whisper với các tham số lấy từ config
    model = WhisperModel(model_size, device=device, compute_type=compute_type)

    # Cấu hình tham số cho quá trình transcription
    transcription_kwargs = {"beam_size": beam_size}
    if vad_filter:
        transcription_kwargs["vad_filter"] = True

    # Chạy quá trình transcription
    batched_model = BatchedInferencePipeline(model=model)
    segments, info = batched_model.transcribe(input_audio, **transcription_kwargs, batch_size=32)
    segments = list(segments)  # Ép generator thành list để dễ xử lý lại sau này
    processed_segments = preprocess_transcript(segments)
    return processed_segments, info




def save_transcript(segments: list, output_file: str) -> None:
    """
    Lưu transcript đã tiền xử lý vào file văn bản.
    Mỗi đoạn được lưu theo định dạng:
      [start_time -> end_time] transcript_text
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for seg in segments:
            # f.write(f"[{seg['start']:.2f}s -> {seg['end']:.2f}s] {seg['text']}\n")
            f.write(f"{seg['text']}\n")