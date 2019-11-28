FROM python:slim
RUN mkdir /app
WORKDIR /app
EXPOSE 8888
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y build-essential && pip install -r requirements.txt
COPY . /app/
ENTRYPOINT ["python", "-m", "aep.app"]


