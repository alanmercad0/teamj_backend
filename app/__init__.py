from flask import Flask

app = Flask(__name__)

# Import routes
from app import routes
app.register_blueprint(routes.bp)
# def create_app():
    
#     return app

if __name__ == '__main__':
    app.run()