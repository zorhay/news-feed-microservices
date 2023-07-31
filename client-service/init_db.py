import dotenv

from app import create_app
from app import db


dotenv.load_dotenv()

with create_app().app_context():
    db.drop_all()
    db.create_all()
