from flask_admin import Admin, AdminIndexView, expose
from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, request, flash, current_app
from markupsafe import Markup

from app.models import Post, Tag, Comment, User, History, MessageBoard, FriendLink, Courses
from flask_admin.form.upload import thumbgen_filename, FileUploadField
import os
import imghdr

cover_path = f'{os.getcwd()}/app/static/covers'


def picture_validation(form, field):
    if isinstance(field.data, str):
        return True
    if field.data:
        filename = field.data.filename
        if not imghdr.what(field.data):
            flash('上传的不是图片!')
            return False
        path = f'{os.getcwd()}/app/static/covers'
        os.makedirs(path, exist_ok=True)
        field.data.save(f'{path}/{filename}')
        field.data = f'covers/{filename}'
        return True
    return False


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


class PeachCourseView(PeachView):

    def _thumbnail(view, context, model, name):
        if not model.cover:
            return ''
        return Markup(
            '<img src="%s">' % url_for('static', filename=thumbgen_filename(model.cover))
        )

    column_formatters = {
        'cover': _thumbnail
    }

    form_overrides = dict(cover=FileUploadField)
    form_args = dict(cover=dict(validators=[picture_validation]))

    def after_model_change(self, form, model, is_created):
        posts = form.data.get("posts")
        for index, post in enumerate(posts):
            post.order = index
        print(form, model, is_created)

    def on_model_change(self, form, model, is_created):
        model.cover = form.cover.data


class PeachPostView(ModelView):
    page_size = 20
    list_template = 'admin/model/peach-list.html'
    create_template = 'admin/model/peach-post-create.html'
    edit_template = 'admin/model/peach-post-edit.html'
    column_searchable_list = ['title']
    column_exclude_list = ['content']
    form_excluded_columns = ['postviews', 'historys']
    column_labels = dict(cover='Cover')
    column_default_sort = ('create_at', True)

    def _thumbnail(view, context, model, name):
        if not model.cover:
            return ''
        return Markup(
            '<img src="%s">' % url_for('static', filename=thumbgen_filename(model.cover))
        )

    column_formatters = {
        'cover': _thumbnail
    }

    form_overrides = dict(cover=FileUploadField)
    form_args = dict(cover=dict(validators=[picture_validation]))

    def __init__(self, model, session, **kwargs):
        self.model = model
        self.session = session
        super(PeachPostView, self).__init__(model, session, **kwargs)

    def is_accessible(self):
        if current_user.is_authenticated:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))

    @action("export", 'Export', 'Are you sure exported selected post')
    def action_export(self, ids):
        try:
            query = Post.query.filter(Post.id.in_(ids))
            count = 0
            for post in query.all():
                count += 1 if self.export_content_to_md(post) else 0
            flash('Posts was successfully exported {} posts were successfully exported.'.format(count))
        except Exception as e:
            if not self.handle_view_exception(e):
                raise
            flash('Failed to export posts. {} error'.format(str(e)))

    def export_content_to_md(self, post):
        title = post.title
        tag_list = [tag.tag for tag in post.tags]
        tags_str = ",".join(tag_list)
        date = post.create_at
        content = post.content
        export_directory = current_app.extensions['hexo'].directory
        export_post_data = "---\ntitle: {}\ntag: [{}]\ncomments: true\ndate: {}\n---\n\n{}".format(title, tags_str,
                                                                                                   date, content)
        if not os.path.exists(export_directory):
            return False
        export_post = os.path.join(export_directory, "{}.md".format(title))
        with open(export_post, 'w', encoding='utf-8') as f:
            f.write(export_post_data)
        return True

    def on_model_change(self, form, model, is_created):
        model.cover = form.cover.data

    def after_model_delete(self, model):
        # TODO after delete post, delete the match post.md
        pass

    @property
    def can_create(self):
        return current_user.is_authenticated and current_user.level == 1

    @property
    def can_delete(self):
        return current_user.is_authenticated and current_user.level == 1

    @property
    def can_edit(self):
        return current_user.is_authenticated and current_user.level == 1


class PeachCommentView(PeachView):
    column_filters = ['is_read']
    column_default_sort = ('comment_time', True)

    def __init__(self, model, session, **kwargs):
        self.session = session
        super(PeachView, self).__init__(model, session, **kwargs)

    @action("read", 'readAll', 'Are you sure make all comments read')
    def make_all_read(self, ids):
        for id in ids:
            comment = Comment.query.filter_by(id=id).first()
            comment.is_read = 1
        self.session.commit()


class PeachAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if current_user.is_authenticated:
            return super(PeachAdminIndexView, self).index()
        flash('没有权限访问该页面!')
        return redirect(url_for('auth.login', next=request.url))


class PeachAdmin:
    __slots__ = ['admin']

    def __init__(self, name="Peach-Blog Management", template_mode="bootstrap3"):
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
            PeachCommentView(Comment, db.session, endpoint='PeachComment'))
        self.admin.add_view(
            PeachView(History, db.session, endpoint='PeachHistory'))
        self.admin.add_view(
            PeachView(MessageBoard, db.session, endpoint='PeachMessageBoard'))
        self.admin.add_view(
            PeachView(FriendLink, db.session, endpoint='PeachFriendLink'))
        self.admin.add_view(PeachCourseView(Courses, db.session, endpoint='PeachCourse'))
