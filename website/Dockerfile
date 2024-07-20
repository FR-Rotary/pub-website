FROM ubuntu:23.04

RUN ln -snf /usr/share/zoneinfo/Europe/Stockholm /etc/localtime && \
    echo "Europe/Stockholm" > /etc/timezone && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
    python3 \
    python3-pip \
    uwsgi \
    uwsgi-plugin-python3 \
    nodejs \
    npm \ 
    unzip \
    curl \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-lang-european && \
    apt-get clean

RUN npm install -g sass jquery

RUN curl -Lo /bulma.zip https://github.com/jgthms/bulma/releases/download/1.0.1/bulma-1.0.1.zip

WORKDIR /app

COPY setup.py /app/
RUN python3 setup.py install

COPY . /app

RUN unzip /bulma.zip -d /app/rotary/static/ && \
    sass rotary/static/sass/style.scss:rotary/static/css/style.css

CMD ["uwsgi", "--ini=uwsgi.ini"]
