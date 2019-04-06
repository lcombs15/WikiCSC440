import unittest
import os
from wiki.web.forms import ChangePasswordForm
from wiki.web.user import UserManager


class TestChangePasswordForm(unittest.TestCase):
    def setUp(self):
        self.sut = UserManager(os.path.abspath('./Tests')).get_user("name")

    def test_givenTwoIdenticalPasswords_WhenCheckPasswordCorrect_ThenTrue(self):
        self.assertTrue(ChangePasswordForm.check_new_passwords("new_password", "new_password"))

    def test_givenTwoDifferentPasswords_WhenCheckPasswordCorrect_ThenFalse(self):
        self.assertFalse(ChangePasswordForm.check_new_passwords("old_password", "new_password"))


class TestChangeDarkMode(unittest.TestCase):

    def setUp(self):
        self.sut = UserManager(os.path.abspath('./Tests')).get_user("testing_user")
        self.sut.set('password', "test")
        self.sut.set('dark_mode', False)

    def test_givenUserWithPasswordTest_When_ThenTrue(self):
        self.assertEqual("test", self.sut.get('password'))


if __name__ == '__main__':
    unittest.main()
