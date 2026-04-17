from flask import Flask
from flask_cors import CORS
from routes.poi_routes import poi_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(poi_bp, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)