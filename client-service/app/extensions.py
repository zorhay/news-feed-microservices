from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

swagger = Swagger(template_file='../apidoc/apidoc.yaml')
db = SQLAlchemy()
