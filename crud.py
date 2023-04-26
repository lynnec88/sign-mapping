from model import db, User, Sign, SignCategory, Category, Review, Question, Quiz, UserQuizScore, UserAnswer, JsonResult, connect_to_db

def create_sign(name, image_url, description):
    """Create and return a new sign."""
    sign = Sign(name=name, image_url=image_url, description=description)
    return sign

def create_category(category_id, name):
    """Create and return a new category."""
    category = Category(category_id=category_id, name=name)
    return category

def create_signcategory(sign_id, category_id):
    """Create and return a new signcategory."""
    signcategory = SignCategory(sign_id=sign_id, category_id=category_id)
    db.session.add(signcategory)
    db.session.commit()
    return signcategory

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def get_users():
    return User.query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

if __name__ == "__main__":
    from server import app

    connect_to_db(app)