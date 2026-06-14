import time
import socket
import redis
from flask import Flask, make_response

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count() -> int:
    return int(cache.get('hits') or 0)

def incr_hit_count() -> int:
    return cache.incr('hits')

@app.route('/')
def hello():
    incr_hit_count()
    count = get_hit_count()
    return f'Hello World! I have been seen {count} times. My name is: {socket.gethostname()}\n'

@app.route('/metrics')
def metrics():
    # Формат метрик Prometheus: тип и значение счётчика
    response = make_response(
        f'''# HELP view_count Flask-Redis-App visit counter
# TYPE view_count counter
view_count{{service="Flask-Redis-App"}} {get_hit_count()}
''', 200)
    response.mimetype = 'text/plain; charset=utf-8'
    return response
