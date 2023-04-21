# crud.py
import json
from model import db, User, Sign, Review, Category, SignCategory, connect_to_db
from server import app

connect_to_db(app)

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)

def get_sign_by_id(sign_id):
    return Sign.query.get(sign_id)

def get_signs_by_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return []
    return category.signs

def load_data():
    # Get the path to the JSON file and open it
    with open('data/signs.json') as f:
        sign_data = json.loads(f.read())
        for data in sign_data['signs']:
            # Create a new Sign object for each sign
            sign = Sign(
                name=data['name'],
                image_url=data['image_url']
            )

            # Add the Sign object to the database session
            db.session.add(sign)

        # Commit the changes to the database
        db.session.commit()

def create_categories():
    cat1 = Category(name="Category 1")
    cat2 = Category(name="Category 2")
    db.session.add_all([cat1, cat2])
    db.session.commit()

def create_sign_categories():
    sc1 = SignCategory(sign=1, category=1)
    sc2 = SignCategory(sign=1, category=2)
    sc3 = SignCategory(sign=2, category=2)
    db.session.add_all([sc1, sc2, sc3])
    db.session.commit()

def create_review(user, sign, comment_text):
    review = Review(user=user, sign=sign, comment_text=comment_text)

    return review