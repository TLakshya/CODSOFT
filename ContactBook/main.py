import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

# Database configuration
DATABASE_NAME = "contacts.db"

class ContactManager:
    def __init__(self):
        self.create_table()

    def create_table(self):
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    phone TEXT,
                    email TEXT,
                    address TEXT
                )
            ''')
            conn.commit()

    def add_contact(self, name, phone, email, address):
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO contacts (name, phone, email, address)
                VALUES (?, ?, ?, ?)
            ''', (name, phone, email, address))
            conn.commit()

    def view_contacts(self):
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM contacts')
            return cursor.fetchall()

    def search_contacts(self, search_term):
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM contacts WHERE name LIKE ?', (f'%{search_term}%',))
            return cursor.fetchall()

    def update_contact(self, contact_id, name, phone, email, address):
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE contacts
                SET name = ?, phone = ?, email = ?, address = ?
                WHERE id = ?
            ''', (name, phone, email, address, contact_id))
            conn.commit()

    def delete_contact(self, contact_id):
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
            conn.commit()


class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.contact_manager = ContactManager()

        self.setup_ui()
        self.refresh_contact_list()

    def setup_ui(self):
        # Contact List
        self.contact_listbox = tk.Listbox(self.root, height=15, width=50)
        self.contact_listbox.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Add Contact Button
        self.add_button = tk.Button(self.root, text="Add Contact", command=self.add_contact)
        self.add_button.grid(row=1, column=0, padx=10, pady=10)

        # Update Contact Button
        self.update_button = tk.Button(self.root, text="Update Contact", command=self.update_contact)
        self.update_button.grid(row=1, column=1, padx=10, pady=10)

        # Delete Contact Button
        self.delete_button = tk.Button(self.root, text="Delete Contact", command=self.delete_contact)
        self.delete_button.grid(row=1, column=2, padx=10, pady=10)

        # Search Box
        self.search_entry = tk.Entry(self.root, width=40)
        self.search_entry.grid(row=2, column=0, padx=10, pady=10)

        # Search Button
        self.search_button = tk.Button(self.root, text="Search", command=self.search_contact)
        self.search_button.grid(row=2, column=1, padx=10, pady=10)

    def refresh_contact_list(self):
        self.contact_listbox.delete(0, tk.END)
        for contact in self.contact_manager.view_contacts():
            self.contact_listbox.insert(tk.END, f"{contact[0]}: {contact[1]}, {contact[2]}, {contact[3]}, {contact[4]}")

    def add_contact(self):
        name = simpledialog.askstring("Input", "Enter Name:")
        phone = simpledialog.askstring("Input", "Enter Phone:")
        email = simpledialog.askstring("Input", "Enter Email:")
        address = simpledialog.askstring("Input", "Enter Address:")
        if name:
            self.contact_manager.add_contact(name, phone, email, address)
            self.refresh_contact_list()
        else:
            messagebox.showwarning("Input Error", "Name is required.")

    def update_contact(self):
        selected = self.contact_listbox.curselection()
        if selected:
            contact_id = self.contact_manager.view_contacts()[selected[0]][0]
            name = simpledialog.askstring("Input", "Enter New Name:")
            phone = simpledialog.askstring("Input", "Enter New Phone:")
            email = simpledialog.askstring("Input", "Enter New Email:")
            address = simpledialog.askstring("Input", "Enter New Address:")
            if name:
                self.contact_manager.update_contact(contact_id, name, phone, email, address)
                self.refresh_contact_list()
            else:
                messagebox.showwarning("Input Error", "Name is required.")
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to update.")

    def delete_contact(self):
        selected = self.contact_listbox.curselection()
        if selected:
            contact_id = self.contact_manager.view_contacts()[selected[0]][0]
            self.contact_manager.delete_contact(contact_id)
            self.refresh_contact_list()
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to delete.")

    def search_contact(self):
        search_term = self.search_entry.get()
        self.contact_listbox.delete(0, tk.END)
        for contact in self.contact_manager.search_contacts(search_term):
            self.contact_listbox.insert(tk.END, f"{contact[0]}: {contact[1]}, {contact[2]}, {contact[3]}, {contact[4]}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()
