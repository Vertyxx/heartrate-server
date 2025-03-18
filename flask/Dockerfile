FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV JWT_SECRET_KEY=supertajnyklic

EXPOSE 5000

CMD ["python", "run.py"]