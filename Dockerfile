FROM python:3.8.0
WORKDIR ./peach-blog
ENV FLASK_APP=./peach-blog/wsgi.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]