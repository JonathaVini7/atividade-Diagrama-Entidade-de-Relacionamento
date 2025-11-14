from datetime import datetime
from app import db

panel_tag_association = db.Table(
    'panel_tag_association',
    db.Column('panel_id', db.Integer, db.ForeignKey('panel.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    role = db.relationship('Role', back_populates='users')
    comments = db.relationship('Comment', back_populates='author')
    visits = db.relationship('Visit', back_populates='visitor')

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    users = db.relationship('User', back_populates='role')

class Exhibit(db.Model):
    __tablename__ = 'exhibit'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    panels = db.relationship('Panel', back_populates='exhibit', cascade='all, delete-orphan')

class Panel(db.Model):
    __tablename__ = 'panel'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    position = db.Column(db.Integer, default=0)
    exhibit_id = db.Column(db.Integer, db.ForeignKey('exhibit.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    exhibit = db.relationship('Exhibit', back_populates='panels')
    images = db.relationship('Image', back_populates='panel', cascade='all, delete-orphan')
    tags = db.relationship('Tag', secondary=panel_tag_association, back_populates='panels')
    comments = db.relationship('Comment', back_populates='panel')

class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300), nullable=False)
    caption = db.Column(db.String(300))
    panel_id = db.Column(db.Integer, db.ForeignKey('panel.id'))

    panel = db.relationship('Panel', back_populates='images')

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    panels = db.relationship('Panel', secondary=panel_tag_association, back_populates='tags')

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    panel_id = db.Column(db.Integer, db.ForeignKey('panel.id'))

    author = db.relationship('User', back_populates='comments')
    panel = db.relationship('Panel', back_populates='comments')

class Visit(db.Model):
    __tablename__ = 'visit'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    exhibit_id = db.Column(db.Integer, db.ForeignKey('exhibit.id'))
    visited_at = db.Column(db.DateTime, default=datetime.utcnow)

    visitor = db.relationship('User', back_populates='visits')
    exhibit = db.relationship('Exhibit')
