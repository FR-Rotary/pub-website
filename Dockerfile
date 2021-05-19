FROM ubuntu:20.04

RUN ln -snf /usr/share/zoneinfo/Europe/Stockholm /etc/localtime && \
    echo "Europe/Stockholm" > /etc/timezone && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
    python3 \
    python3-pip \
    texlive-latex-base && \
    apt-get clean

COPY setup.py /app/setup.py

WORKDIR /app

COPY . /app

RUN python3 setup.py install

ENV FLASK_APP rotary

CMD ["flask", "run"]
