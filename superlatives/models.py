# CSH Superlatives Models
from sqlalchemy import Column, Integer, String, Boolean, Text
from superlatives import db

class Person(db.Model):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    uid = Column(String(64), nullable=False)
    voted = Column(Boolean, nullable=False)
    quote = Column(String(100))
    fav_history = Column(String(100))

    def __init__(self, name, uid):
        self.name = name
        self.uid = uid
        self.voted = False

class SuperlativeVote(db.Model):
    __tablename__ = 'superlatives'
    id = Column(Integer, primary_key=True)
    # 0 and 1 are for the couple entry
    data = Column(Text, nullable=False)

    def __init__(self, answers):
        self.data = json.dumps(answers)
