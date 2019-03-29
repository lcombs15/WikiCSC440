import os
from shutil import copy2

ARCHIVE_FOLDER = 'archive'


def archive(page):
    archive_dir = os.path.join(os.path.dirname(page.path), ARCHIVE_FOLDER, os.path.basename(page.path).split(".")[0])
    os.makedirs(archive_dir)
    copy2(page.path, os.path.join(archive_dir, "_whatever.md"))
