from datetime import datetime
from os import path, makedirs, listdir, remove
from shutil import copy2

from config import CONTENT_DIR
from wiki.core import Page

ARCHIVE_FOLDER = 'archive'
"""
    Default archive folder name
"""

NUM_ARCHIVES_TO_KEEP = 10
"""
    Default number of saves to keep
"""

DEFAULT_DATE_FORMAT = "%Y_%m_%d__%H_%M_%S"
"""
    For archive file names
"""

DISPLAY_DATE_FORMAT = "%d %B %Y %I:%M %p"
"""
    For use with GUI
"""


def archive(page_path):
    """

    :param page_path:
    :param page:
    :return: None

        Makes a backup of given page P in the same directory as P under /ARCHIVE_FOLDER
    """
    archive_dir = get_file_archive_dir(page_path)
    makedirs(archive_dir, exist_ok=True)
    copy2(page_path, path.join(archive_dir, get_timestamped_file_name(path.basename(page_path))))


def get_file_archive_dir(file_path):
    """

    :param file_path:
    :return: archive_dir_string

    Given path to page .md file, returns the destination directory for all archives of file_path
    """
    return path.join(path.dirname(file_path), ARCHIVE_FOLDER, remove_file_extension(path.basename(file_path)))


def get_timestamped_file_name(file_name):
    """

    :param file_name:
    :return: string_stamp_file

    Given README.md, returns 2019_04_02__23_00_04.md
    """
    return datetime.now().strftime(DEFAULT_DATE_FORMAT) + get_file_extension(file_name)


def is_archived_page(page, archive_path=ARCHIVE_FOLDER):
    """

    :param page:
    :param archive_path: (optional)
    :return: boolean_is_archive

    Returns true if page.path contains archive_path
    """
    is_archive_page = False
    head = None
    tail = path.dirname(page.path)
    while head != "" and (not is_archive_page):
        temp = path.split(tail)
        head = temp[1]
        tail = temp[0]
        is_archive_page = head == archive_path
    return is_archive_page


def purge_old_pages(page, num_to_keep=NUM_ARCHIVES_TO_KEEP):
    """

    :param page:
    :param num_to_keep:
    :return: None

    Only keep <num_to_keep> must recent archives
    """
    archive_dir = get_file_archive_dir(page.path)

    if path.isdir(archive_dir):
        files = listdir(archive_dir)
        files.sort()

        for i in range(0, files.__len__() - num_to_keep):
            remove(path.join(archive_dir, files[i]))


def get_archived_pages(page):
    """

    :param page:
    :return: page[]

    Given page P, returns array of archive pages for P
    """
    purge_old_pages(page)
    pages = []
    archive_dir = get_file_archive_dir(page.path)
    if path.isdir(archive_dir):
        for file in listdir(archive_dir):
            p = path.join(archive_dir, file)
            new_page = Page(p, get_page_url_from_path(p))
            new_page.title = datetime.strptime(remove_file_extension(file), DEFAULT_DATE_FORMAT).strftime(
                DISPLAY_DATE_FORMAT)
            pages.append(new_page)
    return pages


def get_page_url_from_path(file_path, root=CONTENT_DIR):
    """

    :param file_path:
    :param root:
    :return string_URL:

    Given file path on disk, returns web accessible URL
    """
    head = ""
    tail = path.dirname(file_path)
    while (path.join(tail) != path.join(root)) and tail != "":
        temp = path.split(tail)
        head = path.join(temp[1], head)
        tail = temp[0]
    return path.join("", head, remove_file_extension(path.basename(file_path)))


def remove_file_extension(file_name):
    """
    :param file_name:
    :return: base_file_name

    > remove_file_extension("index.html")
    index
    > remove_file_extension("readme.md")
    readme
    """
    return path.splitext(file_name)[0]


def get_file_extension(file_name):
    """
    :param file_name:
    :return: file_ext

    > get_file_extension("File.txt")
    .txt
    > get_file_extension("home.md")
    .md
    """
    return path.splitext(file_name)[1]


def restore(url, root=CONTENT_DIR):
    """

    :param url:
    :param root:
    :return: None

    Given url: /pages/home

    on Disk:
        - Archive //content//pages/home.md
        - Copy requested restore point into prod: //content//pages/home.md
    """
    backup_file_path = path.join(root, url + ".md")
    folder_for_current_file = path.join(root, path.dirname(path.dirname(path.dirname(url))))
    current_file_name = path.basename(path.dirname(url)) + ".md"
    restore_path = path.join(folder_for_current_file, current_file_name)

    # Make a backup for current file.md before copying over it
    copy2(restore_path, path.join(path.dirname(backup_file_path), get_timestamped_file_name(current_file_name)))
    copy2(backup_file_path, restore_path)
    return get_page_url_from_path(restore_path)
