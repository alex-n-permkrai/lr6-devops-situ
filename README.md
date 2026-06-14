# Лабораторная работа №6 — Многоконтейнерные приложения: Flask+Redis и Prometheus+Grafana

## Цель
Создать два стека Docker-контейнеров:
1. Веб-приложение на Flask со счётчиком посещений (Redis) и метриками Prometheus.
2. Система мониторинга (Prometheus + Grafana + Blackbox Exporter) для сбора и визуализации метрик.

## Машины
- **10.0.0.100** — Flask+Redis
- **10.0.0.110** — Prometheus+Grafana+Blackbox

## Стек 1: Flask + Redis (машина 10.0.0.100)

text

### Файлы
- **app.py** — Flask-приложение.  
  Endpoints:  
  - `GET /` — возвращает приветствие и обновляет счётчик в Redis.  
  - `GET /metrics` — отдаёт метрики в формате Prometheus (значение счётчика `view_count`).
- **requirements.txt** — `flask`, `redis`.
- **Dockerfile** — образ на `python:3.10-alpine`, запускает Flask на `0.0.0.0:5000`.
- **compose.yaml** — два сервиса: `web` (Flask, порт 8000:5000) и `redis` (официальный образ).

### Запуск

cd devops9compose
docker compose up -d --build

### Проверка:

curl http://10.0.0.100:8000              # счётчик
curl http://10.0.0.100:8000/metrics      # метрики для Prometheus

## Стек 2: Мониторинг (машина 10.0.0.110)

### Файлы
compose.yaml — сервисы:
prometheus (порт 9090), конфиг монтируется из ./prometheus.
grafana (порт 3000, логин admin/grafana), автонастройка источника данных через ./grafana.
blackbox (Blackbox Exporter, порт 9115) для проверки HTTP-доступности.
prometheus/prometheus.yml — конфигурация сбора метрик:
prometheus — сам Prometheus.
blackbox-http — проверка доступности http://10.0.0.100:8000 и https://student.psu.ru через Blackbox.
view_total — прямой сбор метрик с http://10.0.0.100:8000/metrics.
grafana/datasource.yml — автоматическое добавление источника Prometheus (http://prometheus:9090) с именем Prometheus.

Запуск

cd devops9prom
docker compose up -d

Интерфейсы:
Prometheus: http://10.0.0.110:9090
Grafana: http://10.0.0.110:3000 (admin / grafana)

Дашборд в Grafana
Создан вручную (без импорта ID 13659) со следующими панелями:
HTTP Probe Success — probe_success (статус проверок).
HTTP Probe Duration — probe_duration_seconds (время ответа).
Flask Visits — view_count (общее число посещений).
Flask Visits per Minute — rate(view_count[1m]) * 60 (скорость посещений в минуту).

Все метрики доступны благодаря описанным scrape-конфигурациям.

Результат
Приложение Flask+Redis корректно увеличивает счётчик и отдаёт метрики.
Prometheus собирает метрики как с самого приложения, так и через Blackbox.
Grafana отображает дашборд с целевыми показателями, включая график темпа посещений.
