FROM nginx:1.15.6

RUN apt-get update && apt-get install -y --no-install-recommends jekyll node-less && rm -rf /var/lib/apt/lists/*

RUN mkdir /site
WORKDIR /site
COPY . /site

RUN jekyll build -d  /usr/share/nginx/html
RUN lessc /usr/share/nginx/html/static/css/main.less /usr/share/nginx/html/static/css/main.css

COPY nginx.conf /etc/nginx/nginx.conf

