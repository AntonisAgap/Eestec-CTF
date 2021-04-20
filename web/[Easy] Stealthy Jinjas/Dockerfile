FROM ubuntu

RUN apt update && apt install -y python3 python3-pip

RUN pip3 install flask

ADD app /app

COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh

EXPOSE 1337
ENTRYPOINT ["/entrypoint.sh"]