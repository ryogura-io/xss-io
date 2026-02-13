from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_talisman import Talisman
import logging

db = SQLAlchemy()
migrate = Migrate()
talisman = Talisman()

def init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    # Talisman is initialized in the app factory to allow for configuration
    
    logging.basicConfig(level=app.config['LOG_LEVEL'])
