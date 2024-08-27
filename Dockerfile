FROM golang:alpine3.20

WORKDIR /app

COPY go.mod go.sum ./
COPY pkg ./pkg
COPY cmd ./cmd

RUN go mod download

RUN ls -la

RUN CGO_ENABLED=0 GOOS=linux go build -o /embedded-search cmd/*.go

EXPOSE 3000
CMD [ "/embedded-search" ]