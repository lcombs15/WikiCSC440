from datetime import datetime
from os import path, makedirs, listdir
from shutil import copy2
from config import CONTENT_DIR

from wiki.core import Page

ARCHIVE_FOLDER = 'archive'


def archive(page):
    archive_dir = get_file_archive_dir(page.path)
    makedirs(archive_dir, exist_ok=True)
    copy2(page.path, path.join(archive_dir, get_timestamped_file_name(path.basename(page.path))))


def get_file_archive_dir(file_path):
    return path.join(path.dirname(file_path), ARCHIVE_FOLDER, path.splitext(path.basename(file_path))[0])


def get_timestamped_file_name(file_name):
    return datetime.now().strftime("%Y_%m_%d__%H_%M_%S") + path.splitext(file_name)[1]


def is_archived_page(page):
    is_archive_page = False
    head = None
    tail = path.dirname(page.path)
    while head != "" and (not is_archive_page):
        temp = path.split(tail)
        head = temp[1]
        tail = temp[0]
        is_archive_page = head == ARCHIVE_FOLDER
    return is_archive_page


def get_archived_pages(page):
    pages = []
    archive_dir = get_file_archive_dir(page.path)
    if path.isdir(archive_dir):
        for file in listdir(archive_dir):
            p = path.join(archive_dir, file)
            pages.append(Page(p, path.join(path.dirname(page.url), ARCHIVE_FOLDER, path.basename(archive_dir),
                                           path.splitext(file)[0])))
    return pages
