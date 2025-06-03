FROM python:3.12.3

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/application

RUN pip install --upgrade pip wheel

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "application.main:main_app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
