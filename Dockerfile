FROM alpine:3.7

WORKDIR /usr/src/app

RUN adduser -u 9000 -D app

RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python3-dev py-pip gcc musl-dev linux-headers g++

RUN apk add --no-cache python3

COPY requirements.txt /usr/src/app
RUN pip3 install -r requirements.txt

COPY . /usr/src/app
RUN chown -R app:app /usr/src/app

RUN chmod +x codeclimate-mypy.py

USER app

WORKDIR /code

CMD ["/usr/src/app/codeclimate-mypy.py"]
