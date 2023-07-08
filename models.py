from pydantic import BaseModel
from sqlalchemy import Integer,String,Boolean,ForeignKey,Column
from sqlalchemy.orm import DeclarativeBase,relationship

class Base(DeclarativeBase):
  pass

class User(Base):
  __tablename__ = "user"
  id = Column(Integer(),primary_key=True,autoincrement=True,nullable=False)
  username = Column(String(40),unique=True,nullable=False)
  password = Column(String(150),nullable=False)
  
  def __repr__(self):
    return self.name

class Room(Base):
  __tablename__ = "room"
  Column("creator",ForeignKey("user.id"))
  id = Column(Integer(),primary_key=True,autoincrement=True,nullable=False)
  name = Column(String(10),unique=True,nullable=False)
  passkey = Column(String(10),unique=True,nullable=False)
  members = Column(Integer(),unique=False,nullable=False,default=0)
  creator = Column(Integer(),nullable=False)

  def __repr__(self):
    return f"Room {self.name} was created by {self.creator}"
  
