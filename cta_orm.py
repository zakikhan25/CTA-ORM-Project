from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime

Base = declarative_base()

class PaymentTransaction(Base):
    __tablename__ = 'payment_transaction'
    
    transaction_id = Column(Integer, primary_key=True)
    pName = Column(String, ForeignKey('passenger.pName'))
    amount = Column(Float, nullable=False)
    transaction_time = Column(DateTime, default=datetime.now)
    payment_method = Column(String(20))
    
    passenger = relationship("Passenger", backref="transactions")

class Passenger(Base):
    __tablename__ = 'passenger'
    pName = Column(String, primary_key=True)
    pBalance = Column(Float)
    pCurrentStation = Column(String)

def list_passenger_payments():
    session = Session()
    results = session.query(Passenger, PaymentTransaction)\
              .join(PaymentTransaction)\
              .order_by(PaymentTransaction.transaction_time.desc())\
              .limit(10).all()
    
    print("\n=== CTA Payment History ===")
    for passenger, transaction in results:
        print(f"[{transaction.transaction_time.strftime('%m/%d %H:%M')}]")
        print(f"  {passenger.pName}:")
        print(f"  - Paid ${transaction.amount:.2f} ({transaction.payment_method})")
        print(f"  - Current balance: ${passenger.pBalance:.2f}")
        print(f"  - Current station: {passenger.pCurrentStation or 'N/A'}")
        print("-" * 40)

# Database setup
engine = create_engine('postgresql://cta_admin:cta123@localhost/cta_db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def initialize_sample_data():
    session = Session()

    # Clear old data
    session.query(PaymentTransaction).delete()
    session.query(Passenger).delete()

    # Add passengers
    passengers = [
        Passenger(pName="Arthur Morgan", pBalance=42.50, pCurrentStation="Howard"),
        Passenger(pName="Jane Doe", pBalance=15.75, pCurrentStation="Belmont"),
        Passenger(pName="John Smith", pBalance=8.00, pCurrentStation="O'Hare")
    ]

    # Add transactions in specific timestamp order
    transactions = [
        PaymentTransaction(pName="Arthur Morgan", amount=2.50, payment_method="card",
                           transaction_time=datetime(2025, 4, 15, 14, 10)),
        PaymentTransaction(pName="Jane Doe", amount=5.00, payment_method="mobile",
                           transaction_time=datetime(2025, 4, 15, 14, 15)),
        PaymentTransaction(pName="John Smith", amount=3.00, payment_method="cash",
                           transaction_time=datetime(2025, 4, 15, 14, 20)),
        PaymentTransaction(pName="Arthur Morgan", amount=1.75, payment_method="mobile",
                           transaction_time=datetime(2025, 4, 15, 14, 25)),
        PaymentTransaction(pName="Jane Doe", amount=2.25, payment_method="card",
                           transaction_time=datetime(2025, 4, 15, 14, 30)),
    ]

    session.add_all(passengers + transactions)
    session.commit()

if __name__ == "__main__":
    initialize_sample_data()
    list_passenger_payments()
