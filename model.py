# model.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()



class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"

    @classmethod
    def create(cls, email, password):
        return cls(email=email, password=password)

    @classmethod
    def get_by_id(cls, email):
        return cls.query.filter(User.email == email).first()
    
    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(User.email == email).first()

    @classmethod
    def all_users(cls):
        return cls.query.all()


class Sign(db.Model):
    __tablename__ = 'signs'

    sign_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f"<Sign sign_id={self.sign_id} name={self.name}" \
               f"image_url={self.image_url} description={self.description}>"


class SignCategory(db.Model):
    __tablename__ = 'signcategories'

    signcategory_id = db.Column(db.Integer, primary_key=True)
    sign_id = db.Column(db.Integer, db.ForeignKey('signs.sign_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))

    sign = db.relationship('Sign', backref='sign_categories')
    category = db.relationship('Category', backref='sign_categories')

    def __repr__(self):
        return f'<SignCategory sign_id={self.sign_id} category_id={self.category_id}>'


class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Category category_id={self.category_id} name={self.name}>"


class Review(db.Model):
    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    sign_id = db.Column(db.Integer, db.ForeignKey('signs.sign_id'))
    comment_text = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="reviews")
    sign = db.relationship("Sign", backref="reviews")

    def __repr__(self):
        return f"<Review review_id={self.review_id} comment_text={self.comment_text} created_at={self.created_at}>"


class Question(db.Model):
    __tablename__ = "questions"

    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.quiz_id'))
    question_text = db.Column(db.String(200), nullable=False)
    option1 = db.Column(db.String(50), nullable=False)
    option2 = db.Column(db.String(50), nullable=False)
    option3 = db.Column(db.String(50), nullable=False)
    answer = db.Column(db.String(1), nullable=False)
    sign_id = db.Column(db.Integer, db.ForeignKey('signs.sign_id'))

    sign = db.relationship("Sign", backref="signs", uselist=False)

    def __repr__(self):
        return f"<Question question_id={self.question_id} question_text={self.question_text}"\
               f"option1={self.option1} option2={self.option2} option3={self.option3} answer={self.answer}>"


class Quiz(db.Model):
    __tablename__ = "quizzes"

    quiz_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quizname = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Quiz quiz_id={self.quiz_id} quizname={self.quizname}>"


class UserQuizScore(db.Model):
    __tablename__ = "userquizscores"

    userquiz_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.quiz_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    score = db.Column(db.Integer, default=0)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    useranswers = db.relationship("UserAnswer", backref="useranswers")
    quiz = db.relationship("Quiz", backref="quizzes", uselist=False)

    def __repr__(self):
        return f"<UserQuizScore userquiz_id={self.userquiz_id} quiz_id={self.quiz_id}" \
               f"user_id={self.user_id} score={self.score} time={self.time}>"


class UserAnswer(db.Model):
    __tablename__ = "useranswers"

    useranswer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userquiz_id = db.Column(db.Integer, db.ForeignKey('userquizscores.userquiz_id'))
    quiz_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    user_answer = db.Column(db.String(1))

    question = db.relationship("Question", backref=db.backref("questions", order_by=question_id), uselist=False)

    def __repr__(self):
        return f"<UserAnswer useranswer_id={self.useranswer_id} userquiz_id={self.userquiz_id}" \
               f"quiz_id={self.quiz_id} question_id={self.question_id} user_answer={self.user_answer}>"


class JsonResult:
    def __init__(self, status, message, data=None):
        self.status = status
        self.message = message
        self.data = data

    def to_dict(self):
        result_dict = {'status': self.status, 'message': self.message}
        if self.data is not None:
            result_dict['data'] = self.data
        return result_dict

    @classmethod
    def success(cls, message='OK', data=None):
        return cls(True, message, data).to_dict()

    @classmethod
    def fail(cls, message='Server Error', data=None):
        return cls(False, message, data).to_dict()

 

#database name is sign_mapping
def connect_to_db(flask_app, db_uri="postgresql:///sign_mapping", echo=False):
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