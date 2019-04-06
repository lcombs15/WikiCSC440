import unittest
import os
from wiki.web.user import UserManager


class TestUserPreferences(unittest.TestCase):

    def setUp(self):
        self.sut = UserManager(os.path.abspath('./wiki_test')).get_user("testing_user")
        self.sut.set('password', "test")
        self.sut.set('dark_mode', False)

    def test_givenSetPassword_WhenMatchingPasswords_ThenNewPasswordSet(self):
        self.sut.set_password("example", "example")
        self.assertEqual("example", self.sut.get('password'))

    def test_givenSetPassword_WhenMisMatchPasswords_ThenNewPasswordNotSet(self):
        self.sut.set_password("example", "exampl")
        self.assertNotEqual("example", self.sut.get('password'))
        self.assertNotEqual("exampl", self.sut.get('password'))

    def test_givenUserWithoutDarkMode_WhenIsDarkMode_ThenFalse(self):
        self.assertFalse(self.sut.get('dark_mode'))

    def test_givenUserWithDarkMode_WhenIsDarkMode_ThenTrue(self):
        self.sut.set('dark_mode', True)
        self.assertTrue(self.sut.get('dark_mode'))


if __name__ == '__main__':
    unittest.main()
