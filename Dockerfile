FROM python:3.9-slim

COPY . /src

WORKDIR /src

# Update pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "script.py"]