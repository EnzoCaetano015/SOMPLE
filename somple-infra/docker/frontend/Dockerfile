FROM node:22-alpine AS build

WORKDIR /app

RUN apk add --no-cache git && npm install --global pnpm@11.22.0

COPY somple-frontend/package.json \
     somple-frontend/pnpm-lock.yaml \
     somple-frontend/pnpm-workspace.yaml ./

RUN pnpm install --frozen-lockfile

COPY somple-frontend/ .

ARG VITE_API_BASE_URL=http://localhost:8000/api/v1
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

RUN pnpm build

FROM nginx:1.27-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY somple-infra/docker/frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
