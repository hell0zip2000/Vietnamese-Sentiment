

FROM python:3.11-slim


ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1 


WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 3600 -r requirements.txt


COPY . . 


EXPOSE 8501


CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.enableCORS", "false"]

