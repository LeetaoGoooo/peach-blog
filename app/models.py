from app import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

Post2Tag = db.Table("post2tag",
        db.Column('id', db.Integer, primary_key=True),
        db.Column('post_id', db.Integer, db.ForeignKey('posts.id', ondelete="cascade")),
        db.Column('tag_id', db.Integer, db.ForeignKey('tags.id', ondelete="cascade"))
    )

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(10), unique=True)
    email = db.Column(db.String(320))
    password_hash = db.Column(db.String(128))
    avatar = db.Column(db.String(128))
    level = db.Column(db.SmallInteger, default=0)

    @property
    def is_admin(self):
        return True if self.level > 0 else False

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def reset_password(self, old_password, new_password):
        if check_password_hash(self.password_hash, old_password):
            self.password = new_password
            return True
        return False

    def __repr__(self):
        return '<User %r>' % self.user_name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    content = db.Column(db.Text)
    create_at = db.Column(db.Date(), default=datetime.date)
    last_update = db.Column(db.DateTime(), default=datetime.now)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50), unique=True)
    posts = db.relationship('Post', secondary=Post2Tag, backref=db.backref('tags'))

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20))
    email = db.Column(db.String(320))
    website = db.Column(db.String(100))
    comment = db.Column(db.Text)
    comment_time = db.Column(db.DateTime(), default=datetime.now)
    platform = db.Column(db.String(20))
    browser = db.Column(db.String(100))

class PostView(db.Model):
    __tablename__ = 'postviews'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))
    views = db.Column(db.Integer, default=0)
    visit_date = db.Column(db.Date(), default=datetime.date)

class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(128))
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))
    visit_time = db.Column(db.DateTime(), default=datetime.now)