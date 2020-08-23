docker build -t sm .
docker run --name smcontainer --rm -it sm:latest success_metrics.py -u http://sola.local:8070 -a admin:admin123
FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3"]

CMD ["success_metrics.py", "-h"]


