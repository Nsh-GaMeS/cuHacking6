from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Define the User model
# email, username, password, accounts, goals

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True) # id is the primary key, unique for all users
    email = Column(String, index=True)
    username = Column(String, index=True)
    password = Column(String)
    money = Column(Float) # money is the total amount of money the user has
    accounts = relationship("Account", back_populates="user") 

# Define the Account model
# id, name, balance, user_id, transactions

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True, unique=True) # id is the primary key, unique for all accounts
    name = Column(String, index=True)
    curr_balance = Column(Float)
    final_goal = Column(Float, default=0) # final_goal is optional, if the user doesn't want it 
    time_frame = Column(DateTime, default=0) # time_frame is optional, if the user doesn't want it
    interest_rate = Column(Float, default=0) # interest_rate can be 0. if there is no interest. otherwise it's like a monthly interest rate
    fees = Column(Float, default=0) # fees can be 0. if there are no fees. otherwise it's like a monthly fee
    user_id = Column(Integer, ForeignKey('users.id')) # Add foreign key to link to User model
    user = relationship("User", back_populates="accounts")


