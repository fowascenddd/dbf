FROM python:3.13-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git cmake g++ make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python deobf/build_luau.py --portable

CMD ["python", "bot.py"]
