FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

# Create the /db directory in the container
RUN mkdir /db

EXPOSE 5000

CMD ["python", "main.py"]
