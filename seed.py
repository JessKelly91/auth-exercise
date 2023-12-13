from models import db, User, Feedback
from app import app

with app.app_context():
    db.drop_all()
    db.create_all()

    User.query.delete()
    Feedback.query.delete()

    u1 = User.register(username="DemoUser1", 
                       password="letstrythis1!", 
                       email="demouser1@aol.com", 
                       first_name="Demo", 
                       last_name="User")
    u2 = User.register(username="DemoUser2", 
                       password="herewegoagain2!", 
                       email="demouser2@hotmail.com", 
                       first_name="Demo2", 
                       last_name="User2")
    a1 = User.register(username="AdminUser1", 
                       password="adminpassword2321!", 
                       email="adminuser1@gmail.com", 
                       first_name="Admin", 
                       last_name="User",
                       is_admin=True)

    db.session.add_all([u1, u2, a1])
    db.session.commit()

    F1 = Feedback(title="Test Feedback Title",
                  content="Test feedback content.",
                  username="DemoUser1")
    F2 = Feedback(title="DemoUser2's Feedback Test",
                  content="DemoUser2's Feedback content",
                  username="DemoUser2")
    
    db.session.add_all([F1, F2])
    db.session.commit()