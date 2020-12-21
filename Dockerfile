FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip


COPY . /app

RUN pip install -r /app/requirements.txt



EXPOSE 8888

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]