FROM ubuntu:20.04

RUN ln -snf /usr/share/zoneinfo/Europe/Stockholm /etc/localtime && \
    echo "Europe/Stockholm" > /etc/timezone && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
    python3 \
    python3-pip \
    uwsgi \
    ruby-sass \
    unzip \
    curl \
    texlive-latex-base && \
    apt-get clean

RUN curl -Lo /bulma.zip https://github.com/jgthms/bulma/releases/download/0.9.2/bulma-0.9.2.zip

WORKDIR /app

COPY setup.py /app/
RUN python3 setup.py install

COPY . /app

RUN unzip /bulma.zip -d /app/static/

RUN sass --sourcemap=none sass/style.scss:css/style.css

ENV FLASK_APP rotary

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
