
# Golang-Image für Build-Umgebung
FROM golang:1.23 AS builder

# Setze das Arbeitsverzeichnis
WORKDIR /app

# Kopiere alle Dateien ins Image
COPY . .

# Baue die Anwendung
RUN go mod tidy && go build -o stock-publisher

# Finale Laufzeitumgebung
FROM ubuntu:22.04

WORKDIR /app

COPY --from=builder /app/stock-publisher /app/stock-publisher

ENTRYPOINT ["/app/stock-publisher"]
