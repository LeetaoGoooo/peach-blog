from app import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

def dump_datetime(value):
    return value.strftime("%Y-%m-%d %H:%M:%S")

def dump_date(value):
    return value.strftime("%Y-%m-%d")
    

def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = {"DATE":dump_date,"DATETIME":dump_datetime}
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if str(c.type) in convert.keys() and v is not None:
            try:
                d[c.name] = convert[str(c.type)](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[str(c.type)])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return json.dumps(d)

Post2Tag = db.Table("post2tag",
        db.Column('id', db.Integer, primary_key=True),
        db.Column('post_id', db.Integer, db.ForeignKey('posts.id', ondelete="cascade")),
        db.Column('tag_id', db.Integer, db.ForeignKey('tags.id', ondelete="cascade"))
    )

class User(db.Model):
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

    def get_user_id(self):
        return self.id
        
    def __repr__(self):
        return '<User %r>' % self.user_name

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True)
    content = db.Column(db.Text)
    create_at = db.Column(db.Date(), default=datetime.datetime.today())
    last_update = db.Column(db.DateTime(), default=datetime.datetime.now())
    postviews = db.relationship('PostView', backref='postviews', lazy='joined')
    comments = db.relationship('Comment', backref='comments', lazy='joined')
    
    @property
    def json(self):
        return to_json(self, self.__class__)

    def __repr__(self):
        return self.title

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50), unique=True)
    posts = db.relationship('Post', secondary=Post2Tag, backref=db.backref('tags'))

    def __repr__(self):
        return self.tag


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))
    user_name = db.Column(db.String(20))
    email = db.Column(db.String(320))
    website = db.Column(db.String(100))
    comment = db.Column(db.Text)
    comment_time = db.Column(db.DateTime(), default=datetime.datetime.now())
    platform = db.Column(db.String(50))
    browser = db.Column(db.String(100))
    
    def __repr__(self):
        return "{} commentted {} on {}".format(self.user_name,self.comment,self.comment_time)

class PostView(db.Model):
    __tablename__ = 'postviews'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))
    views = db.Column(db.Integer, default=0)
    visit_date = db.Column(db.Date(), default=datetime.date.today())

    def __repr__(self):
        return "on {} this post was total viewed {}".format(self.visit_date,self.views)


class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(128))
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))
    platform = db.Column(db.String(50))
    browser = db.Column(db.String(100))
    visit_time = db.Column(db.DateTime(), default=datetime.datetime.now())

class MessageBoard(db.Model):
    __tablename__ = 'messageboards'
    id = db.Column(db.Integer, primary_key=True)
    message_type = db.Column(db.SmallInteger, default=0) # 0 标识 about 页面 , 1 为 友链页面
    user_name = db.Column(db.String(20))
    email = db.Column(db.String(320))
    website = db.Column(db.String(100))
    message = db.Column(db.Text)
    message_time = db.Column(db.DateTime(), default=datetime.datetime.now())
    platform = db.Column(db.String(50))
    browser = db.Column(db.String(100))

class FriendLink(db.Model):
    __tablename__ = 'friendlinks'
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String(200))
    friend_name = db.Column(db.String(20))
    website = db.Column(db.String(100))
    introduction = db.Column(db.String(100))