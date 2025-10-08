# Dockerfile

FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# start.sh fayliga bajarish huquqi berish
RUN chmod +x start.sh

CMD ["./start.sh"]
