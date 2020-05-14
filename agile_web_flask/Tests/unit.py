import unittest
from app import app, db
from app.models import User, Post

class UserModelTest(unittest.TestCase):

  def setUp(self):
    self.app = app.test_client()
    #make sure database is empty
    db.session.query(User).delete()
    db.create_all()
    u = User(id=1, username='Tom', email='tom@smoker.com')
    db.session.add(u)
    db.session.commit()

  def tearDown(self):
    db.session.remove()

  def test_set_pw(self):  
    u = User.query.get(1)
    u.set_password('pw')
    self.assertFalse(u.check_password('passw0rd'))
    self.assertTrue(u.check_password('pw'))

  def test_set_pw2(self):  
    u = User.query.get(1)
    u.set_password('pw2')
    self.assertFalse(u.check_password('pw2'))
    self.assertTrue(u.check_password('pw'))

if __name__=='__main__':
  unittest.main(verbosity=2)
    