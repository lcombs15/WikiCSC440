import unittest
from wiki.core import File
import os


class TestFile(unittest.TestCase):
    """
    Various unit tests for wiki.core.File
    """

    def setUp(self):
        self.file = File()

    def test_get_file_name_and_type(self):
        self.assertEqual(self.file.get_file_name_and_type('example.png'), ('example', '.png'))
        self.assertNotEqual(self.file.get_file_name_and_type('example.png'), ('example', 'png'))

    def test_get_start_and_end_index(self):
        self.assertEqual(self.file.get_open_bracket_and_closing_bracket_index('example2[5]'), (8, 10))
        self.assertNotEqual(self.file.get_open_bracket_and_closing_bracket_index('example2[5]'), (7, 9))

    def test_get_newest_version_filename(self):
        self.assertEqual(self.file.get_newest_version_filename('example3.jpg', 32), "example3[32].jpg")
        self.assertNotEqual(self.file.get_newest_version_filename('example3[3].jpg', 4), "example3[4].jpg")

    def test_get_filename_without_version(self):
        self.assertEqual(self.file.get_filename_without_version('example4[32838].pdf'), 'example4')
        self.assertNotEqual(self.file.get_filename_without_version('example4[3].pdf'), 'example4.pdf')

    def test_get_version_number(self):
        self.assertEqual(self.file.get_version_number('example5[4378].pptx'), '4378')
        self.assertNotEqual(self.file.get_version_number('example5[239].pptx'), '[239]')

    def test_get_first_version_filename(self):
        self.assertEqual(self.file.get_first_version_filename('example6[1].docx'), 'example6[1][1].docx')
        self.assertNotEqual(self.file.get_first_version_filename('example6[1].docx'), 'example6[2].docx')

    def test_save_to(self):
        self.assertEqual(self.file.save_to('example7.txt', os.path.abspath('../content/files/')), os.path.abspath('../content/files/example7.txt'))
        # Temporarily creates three new files for testing
        file_folder = os.path.abspath('../content/files/')
        first_file = "/".join([file_folder, 'example8[5].txt'])
        second_file =  "/".join([file_folder, 'example9.txt'])
        third_file = "/".join([file_folder, 'example9[1].txt'])
        if not os.path.exists(file_folder):
            os.mkdir(file_folder)
        ff = open(first_file, "w+")
        ff.close()
        sf = open(second_file, "w+")
        sf.close()
        tf = open(third_file, "w+")
        tf.close()
        self.assertEqual(self.file.save_to('example8[5].txt', os.path.abspath('../content/files/')),
                         os.path.abspath('../content/files/example8[5][1].txt'))
        self.assertNotEqual(self.file.save_to('example8[5].txt', os.path.abspath('../content/files/')),
                            os.path.abspath('../content/files/example8[6].txt'))
        self.assertEqual(self.file.save_to('example9.txt', os.path.abspath('../content/files/')),
                         os.path.abspath('../content/files/example9[2].txt'))
        # Removes the three files created earlier
        os.remove(first_file)
        os.remove(second_file)
        os.remove(third_file)


if __name__ == '__main__':
    unittest.main()
