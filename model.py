# model.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"

class Sign(db.Model):
    __tablename__ = 'signs'

    sign_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(200))
    categories = db.relationship('Category', secondary='signcategories', back_populates='signs')

    def __repr__(self):
        return f"<Sign sign_id={self.sign_id} name={self.name}>"

class SignCategory(db.Model):
    __tablename__ = 'signcategories'
    signcategory_id = db.Column(db.Integer, primary_key=True)
    sign = db.Column(db.Integer, db.ForeignKey('signs.sign_id'))
    category = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    
    sign = db.relationship('Sign', backref='sign_categories')
    category = db.relationship('Category', backref='sign_categories')

    def __repr__(self):
        return f'<SignCategory sign_id={self.sign_id} category_id={self.category_id}>'

class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    signs = db.relationship('Sign', secondary='signcategories', back_populates='categories')

    def __repr__(self):
        return f"<Category category_id={self.category_id} name={self.name}>"
    
class Review(db.Model):
    """A model for user reviews of signs."""

    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    sign_id = db.Column(db.Integer, db.ForeignKey('signs.sign_id'))
    comment_text = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("reviews", order_by=review_id))
    sign = db.relationship("Sign", backref=db.backref("reviews", order_by=review_id))

    def __repr__(self):
        return f"<Review review_id={self.review_id} comment_text={self.comment_text}>"
 

#database name is sign_mapping
def connect_to_db(flask_app, db_uri="postgresql:///sign_mapping", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)