FROM node:20-alpine
WORKDIR /app
# baileys ki native deps
RUN apk add --no-cache git python3 make g++ && rm -rf /var/cache/apk/*
COPY package.json ./
RUN npm install --omit=dev --no-audit --no-fund
COPY index.js ./
RUN mkdir -p /app/session
EXPOSE 3001
CMD ["node", "index.js"]
