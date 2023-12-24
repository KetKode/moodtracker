from sqlalchemy import create_engine, Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from moodtracker.config_data.config import DATABASE, POSTGRES_USER, POSTGRES_PASSWORD, ip

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{ip}/{DATABASE}"

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


engine = create_engine(DATABASE_URL, echo=True)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# example
new_user = User(user_id=1, username="testuser")
session.add(new_user)
session.commit()

new_mood = Mood(user_id=1, mood_value="Happy", sub_mood_value="Content", note="Feeling good today")
session.add(new_mood)
session.commit()
