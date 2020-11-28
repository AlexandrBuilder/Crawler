from gino import Gino

db = Gino()


class WordModel(db.Model):
    __tablename__ = 'word_collection'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(400))
    is_filtered = db.Column(db.Boolean, default=True)

    _idx_word = db.Index('word_collection_idx_day_room', 'word', unique=True)


class UrlModel(db.Model):
    __tablename__ = 'url_collection'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500))

    _idx_url = db.Index('url_collection_idx_url', 'url', unique=True)


class WordLocationModel(db.Model):
    __tablename__ = 'word_location_collection'

    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(None, db.ForeignKey('word_collection.id'))
    url_id = db.Column(None, db.ForeignKey('url_collection.id'))
    position = db.Column(db.Integer, default=0)


class LinkBetweenUrlModel(db.Model):
    __tablename__ = 'link_between_url_collection'

    id = db.Column(db.Integer, primary_key=True)
    url_from_id = db.Column(None, db.ForeignKey('url_collection.id'))
    url_to_id = db.Column(None, db.ForeignKey('url_collection.id'))


class LinkWordModel(db.Model):
    __tablename__ = 'link_word_collection'

    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(None, db.ForeignKey('word_collection.id'))
    between_url_id = db.Column(None, db.ForeignKey('link_between_url_collection.id'))
