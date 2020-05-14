import unittest, os, time
from app import app, db
from app.models import User, Post
from selenium import webdriver
basedir = os.path.abspath(os.path.dirname(__file__))

class SystemTest(unittest.TestCase):
  driver = None

  def setUp(self):
    self.driver = webdriver.Firefox(executable_path=os.path.join(basedir,'geckodriver'))
    if not self.driver:
      self.skipTest
    else:
      db.init_app(app)
      db.create_all()
      db.session.query(User).delete()
      db.session.query(Post).delete()
      u = User(id=1, username='Tom', email='tom@smoker.com')
      u.set_password('pw')
      db.session.add(u)
      db.session.commit()
      self.driver.maximize_window()
      self.driver.get('http://localhost:5000/')

  def tearDown(self):
    if self.driver:
      self.driver.close()
      db.session.query(User).delete()
      db.session.query(Post).delete()
      db.session.commit()
      db.session.remove()

  def test_login(self):
    self.driver.get('http://localhost:5000')
    time.sleep(1)
    user_field = self.driver.find_element_by_id('username') 
    password_field = self.driver.find_element_by_id('password')  
    submit = self.driver.find_element_by_id('submit')

    user_field.send_keys('Tom')
    password_field.send_keys('pw')
    submit.click()
    time.sleep(1)

    greeting = self.driver.find_element_by_id('greeting').get_attribute('innerHTML')
    self.assertEqual(greeting, 'Hi, Tom!')

if __name__=='__main__':
  unittest.main(verbosity=2)
    