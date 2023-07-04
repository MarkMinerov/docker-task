FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod a+x entry.sh

CMD ["./entry.sh"]

# CMD ["python", "run-spider.py", "&&", "python", "main.py"]