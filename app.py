from flask import Flask, render_template, request, jsonify
from config import Config
from extensions import db, migrate, talisman, init_extensions
from middleware.headers import configure_security_headers
from middleware.request_logger import configure_request_logger
from dashboard.routes import dashboard_bp
from services.security_service import SecurityService
from models.comment import Comment

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Extensions
    init_extensions(app)
    
    # Register Middleware
    configure_security_headers(app)
    configure_request_logger(app)
    
    # Register Blueprints
    app.register_blueprint(dashboard_bp)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            user_input = request.form.get('comment', '')
            
            # Security Service handles everything
            result = SecurityService.process_input(
                text=user_input,
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string
            )
            
            # Save valid comment
            # Note: In a real app we might not save if it's an attack, 
            # but here we save the *sanitized* version to show it working.
            if not result['detection'].is_suspicious or True: # Demo mode: save everything
                comment = Comment(
                    raw_text=result['original'],
                    sanitized_text=result['sanitized'],
                    is_flagged=result['detection'].is_suspicious
                )
                db.session.add(comment)
                db.session.commit()
            
            return render_template('index.html', result=result)

        # GET request
        comments = Comment.query.order_by(Comment.created_at.desc()).limit(10).all()
        return render_template('index.html', comments=comments)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', error=e), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error.html', error=e), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
