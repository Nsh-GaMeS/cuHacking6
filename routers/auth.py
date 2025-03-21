
import sys
sys.path.append("..")

from pydantic import BaseModel 
from fastapi import APIRouter, Depends
from typing import List, Optional # use Optional to make a field optional in Pydantic. like email in CreateUser
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from passlib.context import CryptContext
from datetime import datetime  
import models

class transaction(BaseModel):
    amount: float = 0
    store: str = "Unknown"
    category: str = "Unknown"
    date: datetime = datetime.now()
    user_id: int

class account(BaseModel):
    name: str = "Cash"
    curr_balance: float = 0
    final_goal: Optional[float] = None
    time_frame: Optional[datetime] = None
    interest_rate: Optional[float] = None
    fees: Optional[float] = None

class CreateUser(BaseModel):
    email: Optional[str] = None
    username: str
    password: str
    money: float = 0
    accounts: Optional[List[account]] = None
    
class credentials(BaseModel):
    username: str
    password: str

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"user": "Not authorized"}}   
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register_user(user: CreateUser, db: Session = Depends(get_db)):
    create_user_model = models.User()
    create_user_model.email = user.email
    create_user_model.username = user.username
    create_user_model.password = get_password_hash(user.password)
    create_user_model.money = user.money
    
    if user.accounts:
        create_user_model.accounts = [
            models.Account(
                name=account.name,
                curr_balance=account.curr_balance,
                final_goal=account.final_goal,
                time_frame=account.time_frame,
                interest_rate=account.interest_rate,
                fees=account.fees,
            ) for account in user.accounts
        ]
    
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return create_user_model


def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

def get_password_hash(password):
    return bcrypt_context.hash(password)

def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User)\
        .filter(models.User.username == username)\
        .first()
    
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

@router.post("/login")
def login_user(creds: credentials, db: Session = Depends(get_db)):
    user = authenticate_user(creds.username, creds.password, db)
    if not user:
        return {"message": "Invalid Credentials"}
    return user

@router.post("/add_transaction")
def add_transaction(transaction: transaction, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == transaction.user_id).first()
    if not user:
        return {"message": "User not found"}

    new_transaction = models.Transaction(
        amount=transaction.amount,
        store=transaction.store,
        category=transaction.category,
        date=transaction.date,
        user_id=user.id
    )
    
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction    
    
@router.get("/get_transactions")
def get_transactions(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return {"message": "User not found"}
    
    return user.transactions

@router.get("/get_accounts")
def get_accounts(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return {"message": "User not found"}
    
    return user.accounts

@router.post("/add_account")
def add_account(account: account, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return {"message": "User not found"}
    
    new_account = models.Account(
        name=account.name,
        curr_balance=account.curr_balance,
        final_goal=account.final_goal,
        time_frame=account.time_frame,
        interest_rate=account.interest_rate,
        fees=account.fees,
        user_id=user.id
    )
    
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

@router.get("/delete_account")
def delete_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not account:
        return {"message": "Account not found"}
    
    db.delete(account)
    db.commit()
    return {"message": "Account deleted"}

@router.get("/get_account_details")
def get_account_details(account_id: int, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not account:
        return {"message": "Account not found"}
    
    return account

@router.get("/update_account_balance")
def update_account_balance(account_id: int, new_balance: float, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not account:
        return {"message": "Account not found"}
    
    account.curr_balance = new_balance
    db.commit()
    db.refresh(account)
    return account