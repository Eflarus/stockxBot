FROM python:3.12
WORKDIR /stockx_bot
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD python -m stockx_bot