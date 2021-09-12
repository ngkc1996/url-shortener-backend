import os
from app import create_app


if __name__ == "__main__":
    app = create_app()
    app.config['MONGO_URI'] = os.environ.get('DB_URI')

    app.run(debug=False)
