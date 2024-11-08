'''
For demo purposes, I'm going to nuke the user db
'''

from app import app, db, User
with app.app_context():
    db.session.query(User).delete()
    db.session.commit()

print("All user records have been deleted.")