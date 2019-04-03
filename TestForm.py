import unittest
from wiki.web.forms import ChangePasswordForm

'''
Maybe extend something and manual mock the check user and password methods
'''

class TestChangePasswordForm(unittest.TestCase):
    def test_givenUserTesting_User_WhenCheckPasswordCorrect_ThenTrue(self):
        self.assertTrue(ChangePasswordForm.check_new_passwords("new_password", "new_password"))


if __name__ == '__main__':
    unittest.main()
