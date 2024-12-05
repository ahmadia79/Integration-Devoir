import sqlite3

class OrderManagementSystem:
    def __init__(self, db_name="order_management.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.setup_tables()

    def setup_tables(self):
        """Create the necessary database tables."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Inventory (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            stock INTEGER NOT NULL
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            accounting_id INTEGER,
            payment_id INTEGER,
            order_status TEXT NOT NULL,
            FOREIGN KEY (product_id) REFERENCES Inventory(product_id)
        )
        """)
        self.conn.commit()

    def add_inventory(self, product_id, product_name, stock):
        """Add a product to the inventory."""
        self.cursor.execute("""
        INSERT OR REPLACE INTO Inventory (product_id, product_name, stock)
        VALUES (?, ?, ?)
        """, (product_id, product_name, stock))
        self.conn.commit()

    def create_order(self, product_id, quantity):
        """Create an order with local transaction handling."""
        try:
            self.conn.execute("BEGIN TRANSACTION")  # Start a transaction

            # Check inventory stock
            self.cursor.execute("SELECT stock FROM Inventory WHERE product_id = ?", (product_id,))
            result = self.cursor.fetchone()
            if not result:
                raise ValueError("Product does not exist in inventory.")

            stock = result[0]
            if stock < quantity:
                raise ValueError("Not enough stock available.")

            # Update inventory
            new_stock = stock - quantity
            self.cursor.execute("""
            UPDATE Inventory SET stock = ? WHERE product_id = ?
            """, (new_stock, product_id))

            # Create an order
            self.cursor.execute("""
            INSERT INTO Orders (product_id, quantity, order_status)
            VALUES (?, ?, ?)
            """, (product_id, quantity, "CONFIRMED"))

            self.conn.commit()  # Commit transaction
            print("Order created successfully!")

        except Exception as e:
            self.conn.rollback()  # Rollback transaction in case of an error
            print(f"Transaction failed: {e}")

    def update_accounting_id(self, order_id, accounting_id):
        """Update the accounting_id of an order."""
        try:
            self.conn.execute("BEGIN TRANSACTION")  # Start a transaction
            self.cursor.execute("""
            UPDATE Orders SET accounting_id = ? WHERE order_id = ?
            """, (accounting_id, order_id))
            self.conn.commit()  # Commit transaction
            print(f"Updated accounting_id for order {order_id} to {accounting_id}.")
        except Exception as e:
            self.conn.rollback()  # Rollback transaction in case of an error
            print(f"Transaction failed: {e}")

    def update_payment_id(self, order_id, payment_id):
        """Update the payment_id of an order."""
        try:
            self.conn.execute("BEGIN TRANSACTION")  # Start a transaction
            self.cursor.execute("""
            UPDATE Orders SET payment_id = ? WHERE order_id = ?
            """, (payment_id, order_id))
            self.conn.commit()  # Commit transaction
            print(f"Updated payment_id for order {order_id} to {payment_id}.")
        except Exception as e:
            self.conn.rollback()  # Rollback transaction in case of an error
            print(f"Transaction failed: {e}")

    def show_inventory(self):
        """Display current inventory."""
        self.cursor.execute("SELECT * FROM Inventory")
        return self.cursor.fetchall()

    def show_orders(self):
        """Display all orders."""
        self.cursor.execute("SELECT * FROM Orders")
        return self.cursor.fetchall()

# Main program for testing the Order Management System
if __name__ == "__main__":
    oms = OrderManagementSystem()

    # Add inventory
    oms.add_inventory(1, "Laptop", 10)

    # Create an order
    oms.create_order(1, 2)

    print("\nOrder Records Before Updates:")
    print(oms.show_orders())

    # Update accounting_id and payment_id
    print("\nUpdating Order Records:")
    oms.update_accounting_id(1, 101)  # Update accounting_id for order_id = 1
    oms.update_payment_id(1, 202)     # Update payment_id for order_id = 1

    print("\nOrder Records After Updates:")
    print(oms.show_orders())
