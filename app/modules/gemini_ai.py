import google.generativeai as genai



def refine_transcript(text: str,api_key: str) -> str:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
    Câu sau được nhận diện tự động từ âm thanh, có thể chứa lỗi chính tả hoặc ngữ pháp:
    

    "{text}"

    Hãy sửa lại thành câu văn chuẩn, rõ ràng, đúng chính tả. Chỉ ghi lại câu đã được chỉnh sửa không ghi các comment thừa hoặc giải thích.
    Lưu ý: Đoạn văn sẽ chủ yếu sẽ nói về một cuộc họp chẳng hạn, không được tự ý xóa chữ nếu từ nào không hiểu ngữ cảnh thì phải giữ nguyên văn bản gốc
    """
    response = model.generate_content(prompt)
    return response.text.strip()