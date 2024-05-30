FROM python:3.10-slim
WORKDIR /app

COPY . /app

VOLUME /app/data
RUN pip3 install -r requirements.txt
# download model from link
# RUN gdown --fuzzy https://drive.google.com/file/d/........../view?usp=drive_link

RUN chmod +x /app/make_prediction.py

CMD ["python3","/app/make_prediction.py"]
