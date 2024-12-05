# Order Management System
A Python-based system for managing orders and inventory using SQLite.

## Features
- Create and manage inventory
- Place orders with local transactions
- Update accounting and payment IDs atomically

## Requirements
- Python 3.x
- SQLite3 (pre-installed with Python)

## How to Run
1. Clone this repository.
2. Run the `order_management.py` script:
   ```bash
   python order_management.py

## Results
### Initial Order Records (Before Updates)
- **Order ID**: `1`
- **Product ID**: `1` (Laptop)
- **Quantity**: `2`
- **accounting_id**: `None`
- **payment_id**: `None`
- **Order Status**: `CONFIRMED`

### Updates to the Order

1. **Update accounting_id**:
   - Updated `accounting_id` to `101`.

2. **Update payment_id**:
   - Updated `payment_id` to `202`.

### Final Order Records (After Updates)

Order Records After Updates: [(1, 1, 2, 101, 202, 'CONFIRMED')]