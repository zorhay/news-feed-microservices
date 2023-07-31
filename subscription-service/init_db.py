import dotenv

from app import create_app
from app import db
from app.models import Plan


dotenv.load_dotenv()

with create_app().app_context():
    db.drop_all()
    db.create_all()
    db.session.add(Plan(name="Android-All", price=1.99, device="android", country="Unknown"))
    db.session.add(Plan(name="iOS-UK", price=4.99, device="ios", country="UK"))
    db.session.add(Plan(name="iOS-US", price=7.99, device="ios", country="US"))
    db.session.commit()
