from flask import Flask
from config import Config
from .extensions import db, bcrypt

def create_app(config_class=Config):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        # Import models to ensure they are registered with SQLAlchemy
        from . import models
        db.create_all()

    # Register Blueprints
    from .auth import auth_bp
    from .entries import entries_bp
    from .analytics import analytics_bp
    from .ai_routes import ai_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(entries_bp, url_prefix='/api/entries')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')

    # Also register without /api prefix to support current frontend
    # Note: Flask blueprints must have unique names if registered multiple times
    # We can use the 'name' parameter, but it's simpler to just expose everything at root if needed
    # or rely on frontend proxy. For now, let's fix the frontend to point to /api/auth
    # OR create alias routes.
    
    # Since we cannot register the same blueprint instance with the same name twice easily without 'name' override,
    # and override might break url_for(), let's just add CORS for everything and maybe redirect?
    
    # Actually, the error is because we registered the SAME blueprint instance twice.
    # Flask allows this if we don't change the name, but url_for might be ambiguous. 
    # Wait, the error explicitly says "The name 'auth' is already registered".
    
    # Let's just fix the frontend usage by implementing a redirect or alias?
    # No, the user probably just wants it to work.
    
    # Workaround: Register with different names for the root versions
    app.register_blueprint(auth_bp, url_prefix='/auth', name='auth_root')
    app.register_blueprint(entries_bp, url_prefix='/entries', name='entries_root')
    app.register_blueprint(analytics_bp, url_prefix='/analytics', name='analytics_root')
    app.register_blueprint(ai_bp, url_prefix='/ai', name='ai_root')

    from flask_cors import CORS
    CORS(
        app,
        supports_credentials=True,
        origins=["http://localhost:3000"]
    )

    @app.route('/health')
    def health_check():
        return {'status': 'ok'}

    # #region agent log
    @app.before_request
    def log_request_info():
        try:
            import json
            import time
            from flask import request
            with open('debug-5d68e9.log', 'a') as f:
                f.write(json.dumps({
                    'sessionId': '5d68e9',
                    'location': 'app/__init__.py:before_request',
                    'message': 'Incoming request',
                    'data': {
                        'method': request.method,
                        'path': request.path,
                        'headers': dict(request.headers),
                        'cookies': request.cookies,
                        'remote_addr': request.remote_addr
                    },
                    'timestamp': int(time.time() * 1000)
                }) + '\n')
        except Exception:
            pass
    # #endregion

    return app
