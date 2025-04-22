# CTA Database Project - Phase 3
## ORM Implementation for Chicago Transit Authority System

### Key Features
- **Payment Tracking System**: Records fare transactions with timestamps
- **1-N Relationship**: `Passenger` → `PaymentTransaction` mapping
- **Query**: Last 10 payments with passenger balance info

### ORM Structure
```python
class PaymentTransaction(Base):
    __tablename__ = 'payment_transaction'
    # Tracks: amount, payment method, timestamp
    # Links to Passenger via foreign key

def list_passenger_payments():
    # Join query showing payment history
