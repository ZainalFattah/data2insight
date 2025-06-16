# -------- Base image Python slim --------
    FROM python:3.10-slim

    # Install poppler library (agar pdfplumber bisa membaca PDF)
    RUN apt-get update && apt-get install -y \
            libpoppler-cpp-dev \
        && rm -rf /var/lib/apt/lists/*
    
    # -------- Workdir & dependencies --------
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    # -------- Copy source code --------
    COPY app/ ./app
    
    # -------- Expose port Streamlit --------
    EXPOSE 8501
    
    # -------- Entry point --------
    CMD ["streamlit", "run", "app/main.py", \
         "--server.port=8501", "--server.address=0.0.0.0"]
    