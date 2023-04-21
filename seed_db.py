"""Script to seed database."""
from random import choice, randint
import os
import model
import crud
from model import Sign, Category, SignCategory, connect_to_db
import server

os.system('dropdb sign_mapping')
os.system('createdb sign_mapping')

connect_to_db(crud.app)

crud.app.app_context().push()
crud.db.create_all()
crud.load_data()
crud.create_categories()
crud.create_sign_categories()

# Create 10 users; each user will make 10 ratings
for n in range(10):
    email = f"user{n}@test.com"  # Voila! A unique email!
    password = "test"

    user = crud.create_user(email, password)
    model.db.session.add(user)

    # Query all sign ids and store in a list
    sign_ids = [sign.sign_id for sign in Sign.query.all()]

    for _ in range(10):
        # Use choice() function to randomly select a sign id from the list
        random_sign = choice(sign_ids)
        comment_text = randint(1, 5)

        review = crud.create_review(user, random_sign)
        model.db.session.add(review)

model.db.session.commit()