import sqlite3
import datetime
import pandas as pd

DB_NAME = "sentiment_history.db"


def init_db() -> None:
    """
    Khởi tạo cơ sở dữ liệu và tạo bảng lưu lịch sử phân tích cảm xúc.
    Hàm tự động được gọi khi hệ thống khởi chạy.
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sentiments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    sentiment TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            conn.commit()
    except sqlite3.Error as e:
        print(f"[DB ERROR] Không thể khởi tạo CSDL: {e}")


def save_history(text: str, sentiment: str) -> None:
    """
    Lưu lại một bản ghi phân tích cảm xúc vào cơ sở dữ liệu.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO sentiments (text, sentiment, timestamp)
                VALUES (?, ?, ?)
                """,
                (text, sentiment, timestamp)
            )
            conn.commit()
    except sqlite3.Error as e:
        print(f"[DB ERROR] Không thể lưu lịch sử: {e}")


def load_history(limit: int = 50) -> pd.DataFrame:
    """
    Tải lịch sử phân tích cảm xúc gần nhất.

    :param limit: Số lượng bản ghi muốn truy vấn (mặc định 50).
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            query = """
                SELECT timestamp, text, sentiment
                FROM sentiments
                ORDER BY id DESC
                LIMIT ?
            """
            df = pd.read_sql_query(query, conn, params=(limit,))
            return df
    except sqlite3.Error as e:
        print(f"[DB ERROR] Không thể tải lịch sử: {e}")
        return pd.DataFrame()


# Khởi tạo DB ngay khi module được import
init_db()
