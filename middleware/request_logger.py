import logging
import time
from flask import request, g

def configure_request_logger(app):
    @app.before_request
    def start_timer():
        g.start_time = time.time()

    @app.after_request
    def log_request(response):
        if request.path.startswith('/static'):
            return response
            
        now = time.time()
        duration = round(now - g.start_time, 2)
        
        ip_address = request.remote_addr
        method = request.method
        path = request.path
        status = response.status_code
        
        log_message = f"[{ip_address}] {method} {path} {status} - {duration}s"
        
        app.logger.info(log_message)
        
        return response
