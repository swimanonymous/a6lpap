"""Flask application factory."""
import os
from flask import Flask
from flask_cors import CORS
from backend.routes.comments import comments_bp
from backend.routes.tasks import tasks_bp

def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__)
    
    # CORS configuration for React dev server
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite default port
            "methods": ["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Register blueprints with prefixes
    app.register_blueprint(comments_bp, url_prefix='/api/comments')
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    
    @app.route('/health')
    def health():
        return {'status': 'ok'}, 200
    
    return app

# For flask run command
app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
