import streamlit as st
import pandas as pd

from core_nlp import classify_sentiment, SENTIMENT_PIPELINE
from database import load_history, save_history

# =========================================================
# A. LOAD PIPELINE & CONFIG
# =========================================================
@st.cache_resource
def load_pipeline():
    return SENTIMENT_PIPELINE

NLP = load_pipeline()

st.set_page_config(
    page_title="Trợ Lý Phân Loại Cảm Xúc Tiếng Việt",
    layout="wide"
)

st.title("Trợ Lý Phân Loại Cảm Xúc Tiếng Việt")
st.caption("Nền tảng phân tích cảm xúc dựa trên Transformer – PhoBERT fine-tuned")

if "history_limit" not in st.session_state:
    st.session_state.history_limit = 50


# =========================================================
# B. UI: HIỂN THỊ SENTIMENT
# =========================================================
def render_sentiment(sentiment, score=None):
    palette = {
        "POSITIVE": ( "#28a745", "TÍCH CỰC"),
        "NEGATIVE": ( "#dc3545", "TIÊU CỰC"),
        "NEUTRAL": ( "#ffc107", "TRUNG TÍNH"),
        "ERROR": ( "gray", "LỖI")
    }

    icon, color, label = palette.get(sentiment, palette["ERROR"])
    score_text = f" (Độ tin cậy: {score*100:.2f}%)" if score else ""

    st.markdown(
        f"""
        <div style='background-color:{color}; padding:12px; border-radius:6px;
                    color:white; font-weight:bold; font-size:18px;'>
            {icon} KẾT QUẢ: {label}{score_text}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# C. KHỐI PHÂN TÍCH CẢM XÚC
# =========================================================
st.header("I. Phân Loại Cảm Xúc")

raw_text = st.text_area("Nhập câu tiếng Việt:", height=100)

if st.button("Phân Tích"):
    if not raw_text.strip():
        st.error("Vui lòng nhập nội dung văn bản.")
    elif NLP is None:
        st.error("Không tải được mô hình NLP. Vui lòng kiểm tra cấu hình.")
    else:
        with st.spinner("Đang phân tích..."):
            try:
                result = classify_sentiment(raw_text)

                st.info("👉 Chuỗi đã được xử lý (Preprocessed):")
                st.markdown(
                    f"<p style='color:#007bff; font-style:italic; font-weight:bold;'>{result['processed_text']}</p>",
                    unsafe_allow_html=True
                )

                render_sentiment(result['sentiment'], result.get('score'))
                save_history(raw_text, result["sentiment"])

            except Exception as e:
                st.error(f"Không xử lý được yêu cầu: {e}")


# =========================================================
# D. KHỐI LỊCH SỬ
# =========================================================
st.header("II. Lịch Sử Phân Loại")

history = load_history(st.session_state.history_limit)

if not history.empty:
    st.subheader(f"{len(history)} bản ghi gần nhất:")
    st.dataframe(history, use_container_width=True)

    if len(history) == st.session_state.history_limit:
        if st.button("Tải thêm dữ liệu"):
            st.session_state.history_limit += 50
            st.rerun()
else:
    st.info("Chưa có bản ghi lịch sử.")
