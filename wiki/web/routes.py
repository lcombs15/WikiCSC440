"""
    Routes
    ~~~~~~
"""
import os
from copy import deepcopy

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import send_file
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from wiki.web.rssfeed import get_rss_data, get_feed_title
from wiki.core import File
from wiki.core import Processor
from wiki.web import current_users
from wiki.web import current_wiki
from wiki.web.archive import archive, is_archived_page, get_archived_pages, restore as restore_page
from wiki.web.forms import ChangePasswordForm
from wiki.web.forms import ChangeTheme
from wiki.web.forms import EditorForm
from wiki.web.forms import RssfeedForm
from wiki.web.forms import LoginForm
from wiki.web.forms import SearchForm
from wiki.web.forms import URLForm
from wiki.web.sudoku import SudokuGame
from wiki.web.sudoku_gen import generate_sudoku
from wiki.web.user import protect

bp = Blueprint('wiki', __name__)


@bp.route('/')
@protect
def home():
    page = current_wiki.get('home')
    if page:
        return display('home')
    return render_template('home.html')


@bp.route('/sudoku/', methods=['GET', 'POST'])
@protect
def sudoku():
    post = request.form

    if len(post) != 0:
        board = []
        for i in range(0, 9):
            row = []
            for j in range(0, 9):
                row.append(int(post[str(i) + str(j)]))
            board.append(row)
    else:
        board = generate_sudoku(9)

    game = SudokuGame(board)
    return render_template('sudoku.html', form=game)


@bp.route('/index/')
@protect
def index():
    pages = current_wiki.index()
    return render_template('index.html', pages=pages)


@bp.route('/<path:url>/')
@protect
def display(url):
    page = current_wiki.get_or_404(url)
    return render_template('page.html',
                           page=page,
                           is_archive_page=is_archived_page(page),
                           archives=get_archived_pages(page))


@bp.route('/create/', methods=['GET', 'POST'])
@protect
def create():
    form = URLForm()
    if form.validate_on_submit():
        return redirect(url_for(
            'wiki.edit', url=form.clean_url(form.url.data)))
    return render_template('create.html', form=form)


@bp.route('/rssfeed/', methods=['GET', 'POST'])
@protect
def rssfeed():
    """
    The user can provide the RSS Feed's url that they wish to view title/link information
    for. To view a different RSS Feed's data they just need to enter another feed's url.

    :return: rssfeed.html and the feed data that was parsed (each entry's title and link)
    """
    form = RssfeedForm()
    if form.validate_on_submit():
        # save rssurl in file
        rssurl = form.rssurl.data
        if (get_feed_title(rssurl) != "PLEASE PROVIDE A DIFFERENT RSS FEED URL"):
            current_user.set('rssurl', rssurl)
    form.rssurl.data = current_user.get('rssurl')
    rssurl = form.rssurl.data
    rssdata = get_rss_data(rssurl)
    channeltitle = get_feed_title(rssurl)

    return render_template('rssfeed.html', form=form, rssdata=rssdata, channeltitle=channeltitle)


@bp.route('/edit/<path:url>/', methods=['GET', 'POST'])
@protect
def edit(url):
    page = current_wiki.get(url)
    form = EditorForm(obj=page)
    if form.validate_on_submit():
        is_new_page = False
        if not page:
            page = current_wiki.get_bare(url)
            is_new_page = True

        original_page = deepcopy(page)
        form.populate_obj(page)
        if not is_new_page and (original_page.body != page.body or original_page.title != page.title):
            archive(original_page.path)
        page.save()
        flash('"%s" was saved.' % page.title, 'success')
        return redirect(url_for('wiki.display', url=url))
    return render_template('editor.html', form=form, page=page)


@bp.route('/preview/', methods=['POST'])
@protect
def preview():
    data = {}
    processor = Processor(request.form['body'])
    data['html'], data['body'], data['meta'] = processor.process()
    return data['html']


@bp.route('/move/<path:url>/', methods=['GET', 'POST'])
@protect
def move(url):
    page = current_wiki.get_or_404(url)
    form = URLForm(obj=page)
    if form.validate_on_submit():
        newurl = form.url.data
        current_wiki.move(url, newurl)
        return redirect(url_for('wiki.display', url=newurl))
    return render_template('move.html', form=form, page=page)


@bp.route('/delete/<path:url>/')
@protect
def delete(url):
    page = current_wiki.get_or_404(url)
    current_wiki.delete(url)
    flash('Page "%s" was deleted.' % page.title, 'success')
    return redirect(url_for('wiki.home'))


@bp.route('/tags/')
@protect
def tags():
    tags = current_wiki.get_tags()
    return render_template('tags.html', tags=tags)


@bp.route('/tag/<string:name>/')
@protect
def tag(name):
    tagged = current_wiki.index_by_tag(name)
    return render_template('tag.html', pages=tagged, tag=name)


@bp.route('/search/', methods=['GET', 'POST'])
@protect
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = current_wiki.search(form.term.data, form.ignore_case.data)
        return render_template('search.html', form=form,
                               results=results, search=form.term.data)
    return render_template('search.html', form=form, search=None)


@bp.route('/user/preferences/', methods=['GET', 'POST'])
@protect
def preferences():
    """
    Displays the Preferences page where users can change the theme of the page and update their password

    :return: preferences.html template
    """
    form = ChangeTheme(username=current_user.name, darkmode=current_user.is_darkmode())
    if request.method == 'POST':
        user = current_users.get_user(form.username.data)
        user.set('dark_mode', form.darkmode.data)
        return redirect(url_for('wiki.preferences'))

    return render_template('preferences.html', user=current_user, form=form)


@bp.route('/user/preferences/changepassword', methods=['GET', 'POST'])
@protect
def changepassword():
    """
    Displays the page where users can update their password

    :return: changepassword.html template
    """
    form = ChangePasswordForm(username=current_user.name)
    if form.validate_on_submit():
        flash('Password changed successfully', 'success')
        return redirect(request.args.get("next") or url_for('wiki.index'))
    return render_template('changepassword.html', user=current_user, form=form)


@bp.route('/user/login/', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = current_users.get_user(form.name.data)
        login_user(user)
        user.set('authenticated', True)
        flash('Login successful.', 'success')
        return redirect(request.args.get("next") or url_for('wiki.index'))
    return render_template('login.html', form=form)


@bp.route("/RESTORE_PAGE/<path:url>")
def restore(url):
    return redirect("/" + restore_page(url))


@bp.route('/user/logout/')
@login_required
def user_logout():
    current_user.set('authenticated', False)
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('wiki.index'))


@bp.route('/user/')
def user_index():
    pass


@bp.route('/user/create/')
def user_create():
    pass


@bp.route('/user/<int:user_id>/')
def user_admin(user_id):
    pass


@bp.route('/user/delete/<int:user_id>/')
def user_delete(user_id):
    pass


@bp.route('/files/', methods=['GET', 'POST'])
@protect
def files():
    """
    The user can select the files they want to save to the wiki. These files are saved to the folder named files in the
    wiki.

    :return: files.html and the list of the files saved
    """

    file = File()
    # Gets the location of files folder
    file_folder = os.path.abspath('./content/files/')
    # Checks that the files folder exists and creates it if it doesn't
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)
    # Goes through each file uploaded by the user
    for f in request.files.getlist('files'):
        # Retrieves the string name of the file
        filename = f.filename
        # Determines where and under what name the file is savedd
        destination = file.save_to(filename, file_folder)
        # Saves the file to the file folder
        f.save(destination)

    files_list = []
    for filename in os.listdir(file_folder):
        files_list.append(filename)
    return render_template('files.html', files=files_list)


@bp.route('/return-file/<path:url>/')
@protect
def return_file(url):
    """
    Opens or downloads the file.

    :param url: the name that the file is saved undered
    :return: the file saved
    """
    file_path = os.path.abspath('./content/files/%s' % url)
    return send_file(file_path)


"""
    Error Handlers
    ~~~~~~~~~~~~~~
"""


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
