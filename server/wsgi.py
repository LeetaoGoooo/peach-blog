from app import create_app
import os
application = create_app(os.environ.get('FLASK_ENV'))