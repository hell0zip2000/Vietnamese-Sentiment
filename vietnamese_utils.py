from underthesea import word_tokenize

# ============================
#  A. TỪ ĐIỂN CHUẨN HÓA
# ============================
# Bộ từ điển này dùng để quy đổi các biến thể teencode, lỗi chính tả,
# hoặc các cụm từ thiếu dấu thành dạng tiếng Việt chuẩn hóa.
NORMALIZATION_MAP = {
    # Teencode – viết tắt thông dụng
    'đc': 'được', 'tk': 'thằng', 'uk': 'ừ', 
    'nx': 'nhận xét', 'qá': 'quá', 't': 'tôi',
    'ko': 'không', 'k': 'không', 
    'bt': 'bình thường', 
    'cx': 'cũng',
    'nhju': 'nhiều', 'j': 'gì', 'vs': 'với', 
    'r': 'rồi',
    'lun': 'luôn',
    

    # Các dạng lặp hoặc nhấn mạnh
    'rất rất rất': 'rất rất',
    'vcl': 'vãi cả linh hồn',

    # Lỗi chính tả & thiếu dấu phổ biến
    'khong': 'không', 
    'gian': 'gian', 'on': 'ồn', 
    'ao': 'ào', 'tuy': 'tuy',
    'thik': 'thích', 'dz': 'dễ thương', 
    'nhien': 'nhiên', 'qua': 'quá', 
    'mon': 'món', 'an': 'ăn',
    'mng': 'mọi người', 'do': 'dở',
    'rat': 'rất', 'hom': 'hôm', 
    'ghet': 'ghét', 'pùn': 'buồn',
    
    

    # Các cụm từ không dấu
    'mon an': 'món ăn',
    'khong gian': 'không gian',
    'on ao': 'ồn ào',
    'tuy nhien': 'tuy nhiên'
}


def preprocess_text(raw_text: str) -> str:
    """
    Chuẩn hóa một câu tiếng Việt theo pipeline:
    - Kiểm tra độ dài đầu vào
    - Chuẩn hóa chữ thường
    - Thay thế teencode/lỗi chính tả bằng dạng chuẩn
    - Tách từ bằng underthesea
    """

    # --- Kiểm soát chất lượng dữ liệu đầu vào ---
    if len(raw_text.strip()) < 5:
        raise ValueError("Câu quá ngắn, yêu cầu tối thiểu 5 ký tự hợp lệ.")

    # --- Đưa về chữ thường để tránh sai lệch khi khớp từ ---
    text = raw_text.lower()

    # --- Thêm khoảng trắng để đảm bảo khớp đúng cụm từ ---
    buffer_text = f" {text} "

    # Ưu tiên xử lý các cụm dài trước để tránh xung đột với từ đơn
    normalized_pairs = sorted(
        NORMALIZATION_MAP.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    # --- Áp dụng chuẩn hóa ---
    for original, standardized in normalized_pairs:
        buffer_text = buffer_text.replace(f" {original} ", f" {standardized} ")

    # Loại bỏ khoảng trắng phụ
    cleaned_text = buffer_text.strip()

    # --- Tách từ (tokenization) ---
    tokens = word_tokenize(cleaned_text)

    # --- Ghép lại thành chuỗi hoàn chỉnh ---
    final_text = " ".join(tokens)

    return final_text
