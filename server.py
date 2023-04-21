from flask import Flask, render_template
from model import connect_to_db, Sign, Category, SignCategory, Review
import crud

app = Flask(__name__)
app.secret_key = "dev"

# Route to render the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to get all signs sorted by category and render the signs.html template
@app.route('/signs', methods=['GET'])
def get_signs():
    signs_by_category = {}
    sign_categories = SignCategory.query.all()

    for sign_category in sign_categories:
        category_id = sign_category.category_id
        sign_id = sign_category.sign_id

        if category_id not in signs_by_category:
            signs_by_category[category_id] = []

        sign = Sign.query.filter_by(sign_id=sign_id).first()
        signs_by_category[category_id].append(sign)

    return render_template('signs.html', signs_by_category=signs_by_category)

# Route to get all categories and render the categories.html template
@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

@app.route("/users")
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("all_users.html", users=users)

@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
