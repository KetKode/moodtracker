from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    user_id = Column(Integer)
    username = Column(String(50), unique=True)
    moods = relationship("Mood", back_populates="user")


class Mood(Base):
    __tablename__ = "moods"

    id = Column(Integer, Sequence("mood_id_seq"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    mood_value = Column(String(50))
    sub_mood_value = Column(String(50))
    note = Column(String(255), nullable=True)

    user = relationship("User", back_populates="moods")


# # example
# new_user = User(user_id=1, username="testuser")
# session.add(new_user)
# session.commit()
#
# new_mood = Mood(user_id=1, mood_value="Happy", sub_mood_value="Content", note="Feeling good today")
# session.add(new_mood)
# session.commit()
