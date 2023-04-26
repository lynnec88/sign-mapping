import os
import json
import random
import crud
import model
import server

os.system("dropdb sign_mapping")
os.system("createdb sign_mapping")

model.connect_to_db(server.app)
model.db.create_all()

# Signs
with open('data/signs.json') as f:
    sign_data = json.loads(f.read())

signs_in_db = []
for sign in sign_data['signs']:
    name, image_url, description =(
        sign["name"],
        sign["image_url"],
        sign["description"],
    )
    db_sign = crud.create_sign(name, image_url, description)
    signs_in_db.append(db_sign)

model.db.session.add_all(signs_in_db)
model.db.session.commit()

# Categories
# with open('data/categories.json') as f:
#     category_data = json.loads(f.read())

categories_in_db = []
for category in sign_data['categories']:
    category_id, name =(
        category["category_id"],
        category["name"],
    )
    db_category = crud.create_category(category_id, name)
    categories_in_db.append(db_category)

model.db.session.add_all(categories_in_db)
model.db.session.commit()

# Sign categories
db_sign_categories = []
for sign in signs_in_db:
    # Assign each sign to a random category
    category = random.choice(categories_in_db)
    db_sign_category = crud.create_signcategory(sign_id=sign.sign_id, category_id=category.category_id)
    db_sign_categories.append(db_sign_category)

model.db.session.add_all(db_sign_categories)
model.db.session.commit()

#Quizzes
quizzes_in_db = []
for quiz in sign_data['quizzes']:
    quiz_id, quizname =(
        quiz["quiz_id"],
        quiz["quizname"],
    )
    db_quiz = crud.create_quiz(quiz_id, quizname)
    quizzes_in_db.append(db_quiz)

model.db.session.add_all(quizzes_in_db)
model.db.session.commit()


#Questions
questions_in_db = []
for question in sign_data['questions']:
    question_id, quiz_id, question_text, option1, option2, option3, answer, sign_id=(
        question["question_id"],
        question["quiz_id"],
        question["question_text"],
        question["option1"],
        question["option2"],
        question["option3"],
        question["answer"],
        question["sign_id"],
    )
    db_question = crud.create_question(question_id, quiz_id, question_text, option1, option2, option3, answer, sign_id)
    questions_in_db.append(db_question)

model.db.session.add_all(questions_in_db)
model.db.session.commit()

# Users
for n in range(10):
    email = f"user{n}@test.com"  # Voila! A unique email!
    password = "test"

    user = crud.create_user(email, password)
    model.db.session.add(user)

model.db.session.commit()
