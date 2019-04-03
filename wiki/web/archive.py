from datetime import datetime
from os import path, makedirs, listdir, remove
from shutil import copy2

from config import CONTENT_DIR
from wiki.core import Page

# Default archive folder name
ARCHIVE_FOLDER = 'archive'

# Default number of saves to keep
NUM_ARCHIVES_TO_KEEP = 10

# For archive file names
DEFAULT_DATE_FORMAT = "%Y_%m_%d__%H_%M_%S"

# For use with GUI
DISPLAY_DATE_FORMAT = "%d %B %Y %I:%M %p"


def archive(page_path):
    """
    Makes a backup of given page P in the same directory as P under /ARCHIVE_FOLDER

    :param page_path: Disk path to md file
    """
    archive_dir = get_file_archive_dir(page_path)
    makedirs(archive_dir, exist_ok=True)
    copy2(page_path, path.join(archive_dir, get_timestamped_file_name(path.basename(page_path))))


def get_file_archive_dir(file_path):
    """
    Given path to page .md file, returns the destination directory for all archives of file_path

    :param file_path: Path on disk
    :return: archive_dir_string
    """
    return path.join(path.dirname(file_path), ARCHIVE_FOLDER, remove_file_extension(path.basename(file_path)))


def get_timestamped_file_name(file_name):
    """
    Given README.md, returns 2019_04_02__23_00_04.md

    :param file_name: No path, just file name
    :return string_stamp_file:  2019_04_02__23_00_04.<file_ext>
    """
    return datetime.now().strftime(DEFAULT_DATE_FORMAT) + get_file_extension(file_name)


def is_archived_page(page, archive_path=ARCHIVE_FOLDER):
    """
    Returns true if page.path contains archive_path
    :param page: Wiki Page object
    :param archive_path: (optional) Archive sub-directory
    :return: boolean_is_archive
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
    Only keep <num_to_keep> most recent archives
    :param page: Wiki Page object
    :param num_to_keep: (optional) Number of saves to preserve (delete the rest)
    """
    archive_dir = get_file_archive_dir(page.path)

    if path.isdir(archive_dir):
        files = listdir(archive_dir)
        files.sort()

        for i in range(0, files.__len__() - num_to_keep):
            remove(path.join(archive_dir, files[i]))


def get_archived_pages(page):
    """
    Given page P, returns array of archive pages for P
    :param page: Wiki Page Object
    :return: page[] - Array of wiki page objects in archive
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
    Given file path on disk, returns web accessible URL
    :param file_path: String path on disk
    :param root: Base content directory with all .md
    :return string_URL: String wiki url to <file_path>
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
    :param file_name: File name without path
    :return: String extension-less file

    >>> remove_file_extension("index.html")
    index
    >>> remove_file_extension("readme.md")
    readme
    """
    return path.splitext(file_name)[0]


def get_file_extension(file_name):
    """
    :param file_name: String file name without path
    :return: file_ext - String extension only of <file_name>

    > get_file_extension("File.txt")
    .txt
    > get_file_extension("home.md")
    .md
    """
    return path.splitext(file_name)[1]


def restore(url, root=CONTENT_DIR):
    """
    on Disk:
        - Archive //content//pages/home.md
        - Copy requested restore point into prod: //content//pages/home.md
    :param url: String ; /pages/home
    :param root: On Disk base directory for wiki content
    """
    backup_file_path = path.join(root, url + ".md")
    folder_for_current_file = path.join(root, path.dirname(path.dirname(path.dirname(url))))
    current_file_name = path.basename(path.dirname(url)) + ".md"
    restore_path = path.join(folder_for_current_file, current_file_name)

    # Make a backup for current file.md before copying over it
    if path.isfile(restore_path):
        copy2(restore_path, path.join(path.dirname(backup_file_path), get_timestamped_file_name(current_file_name)))
    copy2(backup_file_path, restore_path)
    return get_page_url_from_path(restore_path)
