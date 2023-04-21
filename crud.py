# crud.py
import json
from model import db, User, Review, Sign, Category, SignCategory, connect_to_db
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
    review = Review(user_id=user, sign_id=sign, comment_text=comment_text)

    return review