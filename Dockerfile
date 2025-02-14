FROM python:3.12-slim-bullseye

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "-m", "gunicorn", "-w", "4", "-b", "0.0.0.0", "app:app"]