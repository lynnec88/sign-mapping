import os
import json

import crud
import model
import server

os.system("dropdb sign_mapping")
os.system("createdb sign_mapping")

model.connect_to_db(server.app)
model.db.create_all()

with open('data/signs.json') as f:
    sign_data = json.loads(f.read())

signs_in_db = []
for sign in sign_data['signs']:
    print(sign)  # Add this line to inspect the content of sign
    name, image_url, description =(
        sign["name"],
        sign["image_url"],
        sign["description"],
    )
    db_sign = crud.create_sign(name, image_url, description)
    signs_in_db.append(db_sign)

model.db.session.add_all(signs_in_db)
model.db.session.commit()

for n in range(10):
    email = f"user{n}@test.com"  # Voila! A unique email!
    password = "test"

    user = crud.create_user(email, password)
    model.db.session.add(user)

model.db.session.commit()