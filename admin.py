from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView, fields
from flask_login import current_user
from flask import redirect, url_for, request, flash
from app.models import Post, Tag, Comment, User, History, MessageBoard, FriendLink
from flask_admin.form import Select2Widget

class PeachView(ModelView):

    page_size = 20
    list_template = 'admin/model/peach-list.html'
    edit_template = 'admin/model/peach-edit.html'
    create_template = 'admin/model/peach-create.html'

    def __init__(self, model, session, **kwargs):
        super(PeachView, self).__init__(model, session, **kwargs)

    def is_accessible(self):
        if current_user.is_authenticated:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))

    @property
    def can_create(self):
        return current_user.is_authenticated and current_user.level == 1

    @property
    def can_delete(self):
        return current_user.is_authenticated and current_user.level == 1

    @property
    def can_edit(self):
        return current_user.is_authenticated and current_user.level == 1


class PeachPostView(ModelView):

    page_size = 20
    list_template = 'admin/model/peach-list.html'
    create_template = 'admin/model/peach-post-create.html'
    edit_template = 'admin/model/peach-post-edit.html'
    column_searchable_list = ['title']
    column_exclude_list = ['content']

    def __init__(self, model, session, **kwargs):
        super(PeachPostView, self).__init__(model, session, **kwargs)

    def is_accessible(self):
        if current_user.is_authenticated:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))

    @property
    def can_create(self):
        return current_user.is_authenticated and current_user.level == 1

    @property
    def can_delete(self):
        return current_user.is_authenticated and current_user.level == 1

    @property
    def can_edit(self):
        return current_user.is_authenticated and current_user.level == 1

class PeachAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if current_user.is_authenticated:
            return super(PeachAdminIndexView, self).index()
        flash('没有权限访问该页面!')
        return redirect(url_for('auth.login', next=request.url))


class PeachAdmin:

    __slots__ = ['admin']   

    def __init__(self, name="Peach-Blog", template_mode="bootstrap3"):
        self.admin = Admin(name=name, template_mode=template_mode,
                           index_view=PeachAdminIndexView(), base_template='admin/peach-base.html')

    def init_app(self, app, db):
        self.admin.init_app(app)
        # https://github.com/flask-admin/flask-admin/issues/1474
        self.admin.add_view(PeachView(User, db.session, endpoint='PeachUser'))
        self.admin.add_view(PeachPostView(
            Post, db.session, endpoint='PeachPost'))
        self.admin.add_view(PeachView(Tag, db.session, endpoint='PeachTag'))
        self.admin.add_view(
            PeachView(Comment, db.session, endpoint='PeachComment'))
        self.admin.add_view(
            PeachView(History, db.session, endpoint='PeachHistory'))
        self.admin.add_view(
            PeachView(MessageBoard, db.session, endpoint='PeachMessageBoard'))
        self.admin.add_view(
            PeachView(FriendLink, db.session, endpoint='PeachFriendLink'))
