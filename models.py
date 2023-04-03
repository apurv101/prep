from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Root(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    meaning = db.Column(db.String(1000))


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    meaning = db.Column(db.String(1000))
    part_of_speech = db.Column(db.String(50))
    example = db.Column(db.Text)
    level = db.Column(db.Integer)
    root_id = db.Column(db.Integer, db.ForeignKey('root.id'))
    root = db.relationship('Root', backref='words', lazy=True)

    def __repr__(self):
        return '<Word {}>'.format(self.name)


class AppUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=True)
     
    def __repr__(self):
        return '<User {}>'.format(self.name)


class UserWordStrength(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'app_user.id'), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)
    strength = db.Column(db.Integer, nullable=False)

    user = db.relationship('AppUser', backref=db.backref(
        'user_word_strengths', lazy=True))
    word = db.relationship('Word', backref=db.backref(
        'user_word_strengths', lazy=True))

    def __repr__(self):
        return '<UserWordStrength user_id:{} word_id:{} strength:{}>'.format(self.user_id, self.word_id, self.strength)


class WordPassage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)
    passage = db.Column(db.Text, nullable=False)

    word = db.relationship(
        'Word', backref=db.backref('word_passages', lazy=True))

    def __repr__(self):
        return '<WordPassage {}>'.format(self.id)


class WordMultipleOptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)
    openai_output = db.Column(db.Text, nullable=False)

    word = db.relationship(
        'Word', backref=db.backref('word_mutiple_options', lazy=True))

    def __repr__(self):
        return '<WordMultipleOptions {}>'.format(self.openai_output)


class WordPrompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<WordPrompt {}>'.format(self.id)
