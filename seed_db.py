"""Script to seed database."""
from random import choice, randint
import os
import model
import crud
import json
from model import User, Sign, Review, Category, SignCategory, connect_to_db
import server

os.system('dropdb sign_mapping')
os.system('createdb sign_mapping')

connect_to_db(crud.app)

crud.app.app_context().push()
crud.db.create_all()
# crud.create_categories()
# crud.create_sign_categories()

# Create 10 users; each user will make 10 ratings
for n in range(10):
    email = f"user{n}@test.com"  # Voila! A unique email!
    password = "test"

    user = crud.create_user(email, password)
    model.db.session.add(user)

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
        model.db.session.add(sign)

    # Commit the changes to the database
    model.db.session.commit()

# Query all sign ids and store in a list
sign_ids = [sign.sign_id for sign in Sign.query.all()]
user_ids = [user.user_id for user in User.query.all()]

for _ in range(10):
    # Use choice() function to randomly select a sign id from the list
    random_sign = choice(sign_ids)
    random_user = choice(user_ids)
    comment_text = randint(1, 5)

    review = crud.create_review(random_user, random_sign, comment_text)
    model.db.session.add(review)

model.db.session.commit()