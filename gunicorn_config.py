command = '/usr/local/bin/gunicorn'
pythonpath = '/home/sally/app/glynk-webapp'
bind = '127.0.0.1:8003'
workers = 3
timeout = 30
# worker_class = 'gevent'
# worker_connections = 2000