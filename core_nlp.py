from transformers import pipeline
from vietnamese_utils import preprocess_text


# =========================
# 1. CẤU HÌNH MÔ HÌNH
# =========================
PRIMARY_MODEL = "aiface/phobert-v2-3class_v1"
BACKUP_MODEL = "distilbert-base-multilingual-cased"

TOKENIZER_CONFIG = {
    "max_length": 128,
    "truncation": True
}


# =========================
# 2. TẢI PIPELINE NLP
# =========================
def _initialize_pipeline():
    """
    Khởi tạo pipeline PhoBERT. 
    Rơi về mô hình dự phòng nếu pipeline chính không nạp được.
    """
    try:
        print(f"Đang khởi tạo PhoBERT: {PRIMARY_MODEL}...")
        return pipeline(
            task="sentiment-analysis",
            model=PRIMARY_MODEL,
            tokenizer=PRIMARY_MODEL,
            tokenizer_kwargs=TOKENIZER_CONFIG
        )

    except Exception as error:
        print(f"Không thể tải PhoBERT ({PRIMARY_MODEL}): {error}")
        print("Chuyển sang pipeline dự phòng…")

        return pipeline(
            task="sentiment-analysis",
            model=BACKUP_MODEL,
            tokenizer_kwargs=TOKENIZER_CONFIG
        )


SENTIMENT_PIPELINE = _initialize_pipeline()


# =========================
# 3. ÁNH XẠ NHÃN DỰ ĐOÁN
# =========================
LABEL_MAP = {
    "LABEL_0": "NEGATIVE",
    "LABEL_1": "NEUTRAL",
    "LABEL_2": "POSITIVE",
    # Trường hợp mô hình trả về nhãn trực tiếp
    "NEGATIVE": "NEGATIVE",
    "NEUTRAL": "NEUTRAL",
    "POSITIVE": "POSITIVE"
}


# =========================
# 4. HÀM PHÂN LOẠI CẢM XÚC
# =========================
def classify_sentiment(raw_text: str) -> dict:
    """
    Pipeline phân loại cảm xúc cấp hệ thống:
    - Chuẩn hóa tiếng Việt
    - Gọi mô hình
    - Chuẩn hóa nhãn & xử lý logic score
    - Trả về kết quả dạng dict
    """

    if SENTIMENT_PIPELINE is None:
        raise RuntimeError("Pipeline NLP chưa được khởi tạo.")

    # --- Tiền xử lý đầu vào ---
    processed_text = preprocess_text(raw_text)

    try:
        # --- Gọi pipeline ---
        prediction = SENTIMENT_PIPELINE(processed_text)[0]
        raw_label = prediction["label"].upper()
        confidence = prediction["score"]

        print(f"[DEBUG] Raw label: {raw_label}")
        print(f"[DEBUG] Confidence score: {confidence}")

        # --- Xử lý logic dựa vào độ tin cậy ---
        if confidence < 0.5:
            final_label = "NEUTRAL"
        else:
            final_label = LABEL_MAP.get(raw_label, "NEUTRAL")

        # --- Trả kết quả ---
        return {
            "text": raw_text,
            "processed_text": processed_text,
            "sentiment": final_label,
            "score": confidence
        }

    except Exception as error:
        raise RuntimeError(f"Lỗi khi thực thi pipeline NLP: {error}")
