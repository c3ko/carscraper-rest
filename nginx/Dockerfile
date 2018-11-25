FROM nginx-alpine

RUN rm /etc/nginx/nginx.cof
COPY config/nginx.conf /etc/nginx

RUN apk add certbot

COPY ./static ./static