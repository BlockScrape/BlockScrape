FROM node:16.8-alpine as builder

COPY package*.json ./

RUN npm install && mkdir /react-ui && mv ./node_modules ./react-ui

WORKDIR /react-ui

COPY . .

RUN npm run build

FROM nginx:alpine-slim

COPY ./.nginx/nginx.conf /etc/nginx/nginx.conf

RUN rm -rf /usr/share/nginx/html/*

COPY --from=builder /react-ui/build /usr/share/nginx/html

EXPOSE 3000 99

ENTRYPOINT ["nginx", "-g", "daemon off;"]