from flask import request, current_app

def configure_security_headers(app):
    @app.after_request
    def add_security_headers(response):
        # Allow configuration to override defaults
        csp_policy = current_app.config.get('CSP_POLICY', {})
        
        # Construct CSP string
        csp_string = ""
        for key, value in csp_policy.items():
            csp_string += f"{key} {value}; "
        
        response.headers['Content-Security-Policy'] = csp_string.strip()
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response
