FROM python:3.12-slim

ENV PEPPER="pepper_de_prueba"

WORKDIR /app

RUN apt update && apt upgrade -y

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]