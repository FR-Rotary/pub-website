FROM debian:bookworm

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
    texlive-latex-base \
    texlive-latex-extra \
    texlive-lang-european && \
    apt-get clean

WORKDIR /app

COPY package.json /app/
RUN npm install

COPY setup.py /app/
RUN python3 setup.py install

COPY . /app

RUN npm run build
COPY ./rotary/static/css /app/rotary/static/css

EXPOSE 80
CMD ["uwsgi", "--ini=uwsgi.ini"]
