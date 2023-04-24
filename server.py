from flask import Flask, session, redirect, url_for, request, render_template
from model import connect_to_db, Sign, SignCategory, Review, User, JsonResult, Quiz, Question, UserQuizScore, UserAnswer, db
from interceptor import login_required
import json
import datetime




app = Flask(__name__)
app.secret_key = "dev"


#straight to index.html
@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return render_template('index.html')

#login
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(email=username, password=password).first()
    if user:
        session['user_id'] = user.user_id
        session['email'] = user.email
        return JsonResult.success("Login successful")
    else:
        return JsonResult.fail("Login failed, please check if your username or password is wrong")


@app.route('/logout', methods=['POST'])
def logout():
    if 'user_id' in session:
        session.clear()
        return JsonResult.success("You are logged out")
    else:
        return JsonResult.fail("You are not logged in")

#register
@app.before_request
def set_session_lifetime():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=5)


@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    user = User()
    user.email = request.form['username']
    user.password = request.form['password']
    db.session.add(user)
    db.session.commit()
    if user in db.session:
        return JsonResult.success('Register successfully, going to the login page soon')
    else:
        return JsonResult.fail('Registration failed')
    
#home
@app.route('/home', methods=['GET'])
@login_required
def sign_page():
    sign_categories = SignCategory.query.all()
    unique_signs = set()
    unique_categories = set()
    nodes = []
    links = []

    for sign_category in sign_categories:
        sign = sign_category.sign
        category = sign_category.category

        if sign not in unique_signs:
            nodes.append({'id': 's' + str(sign.sign_id), 'name': sign.name, 'category': 0})
            unique_signs.add(sign)

        if category not in unique_categories:
            nodes.append({'id': 'c' + str(category.category_id), 'name': category.name, 'category': 1})
            unique_categories.add(category)

        links.append({'source': 's' + str(sign.sign_id), 'target': 'c' + str(category.category_id)})

    nodedata = json.dumps(nodes)
    linkdata = json.dumps(links)
    return render_template('home.html', nodedata=nodedata, linkdata=linkdata)

#sign
# @app.route('/sign/<sign_id>', methods=['GET'])
# @login_required
# def sign_page(sign_id):
#     asl = Sign.query.get(sign_id)
#     return render_template('sign.html', asl=asl)


@app.route('/sign/<sign_id>', methods=['POST'])
def save_review(sign_id):
    review = Review()
    review.comment_text = request.form['review']
    review.user_id = session['user_id']
    review.sign_id = sign_id
    db.session.add(review)
    db.session.commit()
    if review in db.session:
        return JsonResult.success('Comment successfully, will refresh this page soon')
    else:
        return JsonResult.fail('Comment failed')


#quiz
@app.route('/quizzes', methods=['GET'])
@login_required
def quizzes_page():
    quizzes = Quiz.query.all()
    return render_template('quizzes.html', quizzes=quizzes)


# @app.route('/quiz/<quiz_id>', methods=['GET'])
# @login_required
# def sign_page(quiz_id):
#     questions = Question.query.filter_by(quiz_id=quiz_id).all()
#     quizzes = Quiz.query.get(quiz_id)
#     return render_template('quiz.html', questions=questions, quizzes=quizzes)


@app.route('/quiz/<quiz_id>', methods=['POST'])
@login_required
def save_quiz_score(quiz_id):
    userquizscore = UserQuizScore()
    userquizscore.user_id = session['user_id']
    userquizscore.quiz_id = quiz_id
    userquizscore.score = request.form.get('score')
    db.session.add(userquizscore)
    db.session.commit()

    useranswers = json.loads(request.form.get('answers'))
    for useranswer in useranswers:
        useranswer['userquiz_id'] = userquizscore.userquiz_id
        useranswer['quiz_id'] = quiz_id
    db.session.bulk_insert_mappings(UserAnswer, useranswers)
    db.session.commit()

    if userquizscore in db.session:
        return JsonResult.success('Submitted successfully, going to the score page soon')
    else:
        return JsonResult.fail('Submission failure')

#score
@app.route('/scores', methods=['GET'])
@login_required
def scores_page():
    userquizscores = UserQuizScore.query.filter_by(user_id=session['user_id']).all()
    return render_template('scores.html', userquizscores=userquizscores)


@app.route('/answer/<userquiz_id>', methods=['GET'])
@login_required
def answer_page(userquiz_id):
    userquizscore = UserQuizScore.query.get(userquiz_id)
    return render_template('answer.html', userquizscore=userquizscore)

#pay
@app.route('/price')
def price_page():
    return render_template('price.html')


@app.route('/pay')
def pay_success_page():
    return render_template('pay_success.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
