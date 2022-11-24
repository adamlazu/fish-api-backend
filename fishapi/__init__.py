import os
from flask import *
from . import db
from flask_cors import CORS

def create_app():
    app = Flask(__name__,instance_relative_config= True)
    app.config.from_pyfile('settings.cfg',silent=False)
    CORS(app)


    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    db.init_app(app)
    
    from . import pond
    app.register_blueprint(pond.bp)
    return app
