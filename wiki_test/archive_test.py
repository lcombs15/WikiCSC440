import unittest
from datetime import datetime

from wiki.web import archive


class TestArchive(unittest.TestCase):
    """
        Various unit tests for wiki.web.archive

        Lucas Combs
        April 2019
    """

    def test_remove_file_extension(self):
        """
            Verify that the file extension is removed.
        """
        file = "readme.md"
        self.assertEqual("readme", archive.remove_file_extension(file))

    def test_get_file_extension(self):
        """
            Verify that only the file extension is returned.
        """
        file = "notes.txt"
        self.assertEqual(".txt", archive.get_file_extension(file))

    def test_normal_get_page_url_from_path(self):
        """
            Verify that the generated URL is correct. The path on disk is different from the wiki URL.
        """
        content = "content"
        path = "%s\\home.md" % content
        self.assertEqual("home", archive.get_page_url_from_path(path, content))

    def test_bad_get_page_url_from_path(self):
        """
            This is an edge case where the base directory is not present in the path.

            In the event that this is not handled, we will have an infinite loop. (Web page will never load)
        """
        path = "content\\home.md"
        self.assertEqual("content\\home", archive.get_page_url_from_path(path, "INVALID PATH"))

    def test_is_archived_page(self):
        """
            Test that a page with an /archive/ directory in it's path is considered to be an archived page.
        """
        _archive = "archive"

        class MockPage:
            path = "content\\stuff\\%s\\test.md" % _archive

        self.assertTrue(archive.is_archived_page(MockPage(), _archive))

    def test_get_timestamped_file_name(self):
        """
            Verify that a timestamped file name:
                1.) Doesn't contain the original file name
                    * get_timestamped_file_name(readme.md) does not contain "readme"
                2.) Has the same file extension
                    * get_timestamped_file_name(readme.md) ends with ".md"
                3.)  Contains the current year
                    * example: 2019
        """
        file = "readme"
        ext = ".md"
        name = archive.get_timestamped_file_name(file + ext)

        # Shouldn't contain actual name of file
        self.assertFalse(name.__contains__(file))

        # Should have the same file extension
        self.assertTrue(name.endswith(ext))

        # Should contain the year
        self.assertTrue(name.__contains__(datetime.now().year.__str__()))

    def test_get_file_archive_dir(self):
        """
            Verify that a pages archive directory as follows:
            Path to *P*: /staff/welcome
            Archive path for *P*: /staff/archive/welcome
        """
        path = "\\content\\info\\welcome.md"
        self.assertEqual("\\content\\info\\%s\\welcome" % archive.ARCHIVE_FOLDER, archive.get_file_archive_dir(path))


if __name__ == '__main__':
    unittest.main()
