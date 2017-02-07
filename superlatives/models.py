# CSH Superlatives Models
from sqlalchemy import Column, Integer, String, Boolean
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
    superlative_0 = Column(Integer, nullable=False)
    superlative_1 = Column(Integer, nullable=False)
    superlative_2 = Column(Integer, nullable=False)
    superlative_3 = Column(Integer, nullable=False)
    superlative_4 = Column(Integer, nullable=False)
    superlative_5 = Column(Integer, nullable=False)
    superlative_6 = Column(Integer, nullable=False)
    superlative_7 = Column(Integer, nullable=False)
    superlative_8 = Column(Integer, nullable=False)
    superlative_9 = Column(Integer, nullable=False)
    superlative_10 = Column(Integer, nullable=False)
    superlative_11 = Column(Integer, nullable=False)
    superlative_12 = Column(Integer, nullable=False)
    superlative_13 = Column(Integer, nullable=False)
    superlative_14 = Column(Integer, nullable=False)
    superlative_15 = Column(Integer, nullable=False)
    superlative_16 = Column(Integer, nullable=False)
    superlative_17 = Column(Integer, nullable=False)
    superlative_18 = Column(Integer, nullable=False)
    superlative_19 = Column(Integer, nullable=False)
    superlative_20 = Column(Integer, nullable=False)
    superlative_21 = Column(Integer, nullable=False)
    superlative_22 = Column(Integer, nullable=False)
    superlative_23 = Column(Integer, nullable=False)
    superlative_24 = Column(Integer, nullable=False)
    superlative_25 = Column(Integer, nullable=False)
    superlative_26 = Column(Integer, nullable=False)
    superlative_27 = Column(Integer, nullable=False)

    def __setitem__(self, item, value):
        self.__dict__[item] = value

    def __getitem__(self, item):
        return self.__dict__[item]

    def __init__(self, answers):
        i = 0
        for answer in answers:
            self.__setitem__("superlative_" + str(i), answer)
            i += 1
