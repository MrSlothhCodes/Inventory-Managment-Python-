import tkinter as tk
from tkinter import ttk
import sqlite3

class InventoryManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Manager")

        # Create and connect to the database
        self.conn = sqlite3.connect("inventory.db")
        self.create_table()

        # GUI components
        self.label = ttk.Label(root, text="Inventory Manager", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, columnspan=7, pady=10)

        self.tree = ttk.Treeview(root, columns=("ID", "Item", "Quantity", "Price", "Sold To", "Bought From", "Total"))
        self.tree.heading("#0", text="")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", anchor=tk.CENTER, width=50)
        self.tree.heading("Item", text="Item")
        self.tree.column("Item", anchor=tk.W, width=150)
        self.tree.heading("Quantity", text="Quantity")
        self.tree.column("Quantity", anchor=tk.CENTER, width=100)
        self.tree.heading("Price", text="Price")
        self.tree.column("Price", anchor=tk.CENTER, width=100)
        self.tree.heading("Sold To", text="Sold To")
        self.tree.column("Sold To", anchor=tk.W, width=150)
        self.tree.heading("Bought From", text="Bought From")
        self.tree.column("Bought From", anchor=tk.W, width=150)
        self.tree.heading("Total", text="Total")
        self.tree.column("Total", anchor=tk.CENTER, width=100)
        self.tree.grid(row=1, column=0, columnspan=7, padx=10)

        self.add_button = ttk.Button(root, text="Purchase", command=self.add_item)
        self.add_button.grid(row=2, column=0, pady=10)

        self.update_button = ttk.Button(root, text="Update/Sell", command=self.update_quantity)
        self.update_button.grid(row=2, column=1, pady=10)

        self.delete_button = ttk.Button(root, text="Delete", command=self.delete_item)
        self.delete_button.grid(row=2, column=2, pady=10)

        self.credits_button = ttk.Button(root, text="Credits", command=self.credits)
        self.credits_button.grid(row=2, column=3, pady=10)

        # Display inventory when the program runs
        self.display_inventory()
    def credits(self):
         add_window = tk.Toplevel(self.root)
         add_window.title("Credits")
         bold_font = ("Helvetica", 10, "bold")
         text_label = tk.Label(add_window, text="Made By", font=bold_font, fg="Black", bg="lightgray")
         text_label.grid(row=0, column=0, columnspan=1, pady=10, padx=(20, 20), sticky='nsew')  # Centered horizontally

         name = tk.Label(add_window, text="Suryansh Ahuja", font=bold_font, fg="Black", bg="lightgray")
         name.grid(row=1, column=0, columnspan=1, pady=10, padx=(20, 20), sticky='nsew')

         name1 = tk.Label(add_window, text=" ", font=bold_font, fg="Black", bg="lightgray")
         name1.grid(row=2, column=0, columnspan=1, pady=10, padx=(20, 20), sticky='nsew')

         name2 = tk.Label(add_window, text=" ", font=bold_font, fg="Black", bg="lightgray")
         name2.grid(row=3, column=0, columnspan=1, pady=10, padx=(20, 20), sticky='nsew')

         text_label2 = tk.Label(add_window, text="As a Class 12 CSE project", font=bold_font, fg="Black", bg="lightgray")
         text_label2.grid(row=4, column=0, columnspan=1, pady=10, padx=(20, 20), sticky='nsew')  # Centered horizontally
         add_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))


    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                sold_to TEXT,
                bought_from TEXT
            )
        ''')
        self.conn.commit()

    def add_item(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Purchase Item")

        item_label = ttk.Label(add_window, text="Item:")
        item_label.grid(row=0, column=0, padx=10, pady=10)

        item_entry = ttk.Entry(add_window)
        item_entry.grid(row=0, column=1, padx=10, pady=10)

        quantity_label = ttk.Label(add_window, text="Quantity:")
        quantity_label.grid(row=1, column=0, padx=10, pady=10)

        quantity_entry = ttk.Entry(add_window)
        quantity_entry.grid(row=1, column=1, padx=10, pady=10)

        price_label = ttk.Label(add_window, text="Price:")
        price_label.grid(row=2, column=0, padx=10, pady=10)

        price_entry = ttk.Entry(add_window)
        price_entry.grid(row=2, column=1, padx=10, pady=10)

        bought_from_label = ttk.Label(add_window, text="Bought From:")
        bought_from_label.grid(row=4, column=0, padx=10, pady=10)

        bought_from_entry = ttk.Entry(add_window)
        bought_from_entry.grid(row=4, column=1, padx=10, pady=10)

        save_button = ttk.Button(add_window, text="Save", command=lambda: self.save_item(item_entry.get(), quantity_entry.get(), price_entry.get(), "", bought_from_entry.get(), add_window))
        save_button.grid(row=5, column=0, columnspan=2, pady=10)

    def save_item(self, item, quantity, price, sold_to, bought_from, add_window):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO inventory (item, quantity, price, sold_to, bought_from) VALUES (?, ?, ?, ?, ?)", (item, quantity, price, sold_to, bought_from))
        self.conn.commit()
        add_window.destroy()

        # Display inventory after adding an item
        self.display_inventory()

    def update_quantity(self):
        update_window = tk.Toplevel(self.root)
        update_window.title("Update/Sell")

        id_label = ttk.Label(update_window, text="ID:")
        id_label.grid(row=0, column=0, padx=10, pady=10)
        
        id_entry = ttk.Entry(update_window)
        id_entry.grid(row=0, column=1, padx=10, pady=10)

        quantity_label = ttk.Label(update_window, text="New Quantity:")
        quantity_label.grid(row=1, column=0, padx=10, pady=10)

        quantity_entry = ttk.Entry(update_window)
        quantity_entry.grid(row=1, column=1, padx=10, pady=10)

        sold_to_label = ttk.Label(update_window, text="Sold To:")
        sold_to_label.grid(row=2, column=0, padx=10, pady=10)

        sold_to_entry = ttk.Entry(update_window)
        sold_to_entry.grid(row=2, column=1, padx=10, pady=10)

        bought_from_label = ttk.Label(update_window, text="Bought From:")
        bought_from_label.grid(row=3, column=0, padx=10, pady=10)

        bought_from_entry = ttk.Entry(update_window)
        bought_from_entry.grid(row=3, column=1, padx=10, pady=10)

        save_button = ttk.Button(update_window, text="Save", command=lambda: self.save_quantity(id_entry.get(), quantity_entry.get(), sold_to_entry.get(), bought_from_entry.get(), update_window))
        save_button.grid(row=4, column=0, columnspan=2, pady=10)

    def save_quantity(self, item_id, new_quantity, sold_to, bought_from, update_window):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE inventory SET quantity = ?, sold_to = ?, bought_from = ? WHERE id = ?", (new_quantity, sold_to, bought_from, item_id))
        self.conn.commit()
        update_window.destroy()

        # Display inventory after updating quantity
        self.display_inventory()

    def delete_item(self):
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Item")

        id_label = ttk.Label(delete_window, text="ID:")
        id_label.grid(row=0, column=0, padx=10, pady=10)

        id_entry = ttk.Entry(delete_window)
        id_entry.grid(row=0, column=1, padx=10, pady=10)

        delete_button = ttk.Button(delete_window, text="Delete", command=lambda: self.delete_item_by_id(id_entry.get(), delete_window))
        delete_button.grid(row=1, column=0, columnspan=2, pady=10)

    def delete_item_by_id(self, item_id, delete_window):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
        self.conn.commit()

        # Display inventory after deleting an item
        self.display_inventory()

        delete_window.destroy()

    def display_inventory(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT *, quantity * price as total FROM inventory")
        rows = cursor.fetchall()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in rows:
            self.tree.insert("", "end", values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManager(root)
    root.mainloop()
