# cta_orm.py - Payment Tracking System
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Passenger(Base):
    __tablename__ = 'passenger'
    pName = Column(String, primary_key=True)
    pBalance = Column(Float)
    pCurrentStation = Column(String)

class PaymentTransaction(Base):
    __tablename__ = 'payment_transaction'
    transaction_id = Column(Integer, primary_key=True)
    pName = Column(String, ForeignKey('passenger.pName'))
    amount = Column(Float, nullable=False)
    transaction_time = Column(DateTime, default=datetime.now)
    payment_method = Column(String(20))
    passenger = relationship("Passenger", backref="transactions")

def list_passenger_payments():
    # Connect to PostgreSQL (replace with your credentials)
    engine = create_engine('postgresql://cta_admin:cta123@localhost/cta_db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Your join query
    results = session.query(Passenger, PaymentTransaction)\
              .join(PaymentTransaction)\
              .order_by(PaymentTransaction.transaction_time.desc())\
              .limit(10).all()
    
    # Print formatted results
    print("\n=== CTA Payment History ===")
    for passenger, transaction in results:
        print(f"[{transaction.transaction_time.strftime('%m/%d %H:%M')}]")
        print(f"  {passenger.pName}:")
        print(f"  - Paid ${transaction.amount:.2f} ({transaction.payment_method})")
        print(f"  - Current balance: ${passenger.pBalance:.2f}")
        print("-" * 40)

if __name__ == "__main__":
    list_passenger_payments()
