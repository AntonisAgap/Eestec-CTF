FROM python:3-alpine

RUN apk add --update --no-cache gcc g++ make libffi-dev openssl-dev socat

RUN pip install pycryptodome

ADD app /app

WORKDIR /app

EXPOSE 1337
#CMD socat -dd TCP4-LISTEN:1337,reuseaddr,fork EXEC:"python3 /app/server.py",stderr
CMD ["python", "server.py"]