import sqlite3
from tkinter import *
from tkinter import messagebox, ttk, filedialog
import csv
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import time


def connect_db():
    return sqlite3.connect("programmers.db")

def animate_add():
    for i in range(5):
        root.update_idletasks()
        tree.tag_configure("fade", background=f"#D1FF{5-i}F")
        time.sleep(0.1)

def add_programmer():
    name = entry_name.get()
    salary = entry_salary.get()
    pin = entry_pin.get()
    experience = entry_exp.get()
    email = entry_email.get()
    phone = entry_phone.get()

    if not all([name, salary, pin, experience, email, phone]):
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        salary = float(salary)
        pin = int(pin)
        experience = int(experience)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO programmers (name, salary, pin, experience, email, phone)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, salary, pin, experience, email, phone))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"{name} added successfully!")
        view_programmers()
        clear_fields()
        animate_add()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to add programmer: {e}")

def view_programmers():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM programmers")
    rows = cursor.fetchall()
    conn.close()

    for row in tree.get_children():
        tree.delete(row)

    for index, row in enumerate(rows):
        tag = "evenrow" if index % 2 == 0 else "oddrow"
        tree.insert("", "end", values=row, tags=(tag,))

    tree.tag_configure("evenrow", background="#f0f0f0")
    tree.tag_configure("oddrow", background="#e0e0e0")


def update_programmer():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "No programmer selected!")
        return

    item = tree.item(selected[0])
    programmer_id = item["values"][0]

    name = entry_name.get()
    salary = entry_salary.get()
    pin = entry_pin.get()
    experience = entry_exp.get()
    email = entry_email.get()
    phone = entry_phone.get()

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE programmers
        SET name=?, salary=?, pin=?, experience=?, email=?, phone=?
        WHERE id=?
        ''', (name, salary, pin, experience, email, phone, programmer_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Programmer updated successfully!")
        view_programmers()
        clear_fields()
        animate_add()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to update programmer: {e}")


def delete_programmer():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "No programmer selected!")
        return

    item = tree.item(selected[0])
    programmer_id = item["values"][0]

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM programmers WHERE id=?", (programmer_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Programmer deleted successfully!")
        view_programmers()

        
        for i in range(5):
            root.update_idletasks()
            tree.tag_configure("fade", background=f"#FF{5-i}D1")
            time.sleep(0.1)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete programmer: {e}")


def export_to_csv():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM programmers")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        messagebox.showerror("Error", "No data to export!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

    if not file_path:
        return

    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Salary", "PIN", "Experience", "Email", "Phone"])
        writer.writerows(rows)

    messagebox.showinfo("Success", "Data exported successfully!")


def clear_fields():
    entry_name.delete(0, END)
    entry_salary.delete(0, END)
    entry_pin.delete(0, END)
    entry_exp.delete(0, END)
    entry_email.delete(0, END)
    entry_phone.delete(0, END)


root = ThemedTk(theme="arc")
root.title("Programmer Management System")
root.geometry("1200x800")
root.minsize(900, 600)


main_frame = Frame(root, bg="#ADD8E6")
main_frame.pack(fill=BOTH, expand=True)

form_frame = Frame(main_frame, bg="#D1E8FF", padx=20, pady=20)
form_frame.grid(row=0, column=0, sticky="ew")

labels = ["Name", "Salary", "PIN", "Experience", "Email", "Phone"]
entries = []

for idx, label in enumerate(labels):
    Label(form_frame, text=label, font=("Helvetica", 12, "bold"), bg="#D1E8FF").grid(row=idx, column=0, padx=10, pady=5, sticky="w")
    entry = Entry(form_frame, font=("Helvetica", 12))
    entry.grid(row=idx, column=1, padx=10, pady=5, sticky="ew")
    entries.append(entry)

entry_name, entry_salary, entry_pin, entry_exp, entry_email, entry_phone = entries

btn_frame = Frame(main_frame, bg="#ADD8E6", pady=10)
btn_frame.grid(row=1, column=0, sticky="ew")

buttons = [
    ("Add", add_programmer),
    ("Update", update_programmer),
    ("Delete", delete_programmer),
    ("Export CSV", export_to_csv),
    ("Clear", clear_fields)
]

for idx, (text, command) in enumerate(buttons):
    btn = Button(btn_frame, text=text, font=("Helvetica", 12, "bold"), bg="#87CEEB", command=command)
    btn.grid(row=0, column=idx, padx=10, pady=5, sticky="ew")

table_frame = Frame(main_frame)
table_frame.grid(row=2, column=0, sticky="nsew")

scroll_y = Scrollbar(table_frame, orient=VERTICAL)
tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Salary", "PIN", "Experience", "Email", "Phone"), show="headings", yscrollcommand=scroll_y.set)
import sqlite3
from tkinter import *
from tkinter import messagebox, ttk, filedialog
import csv
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import time

class ProgrammerManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Programmer Management System")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)

        self.main_frame = Frame(self.root, bg="#ADD8E6")
        self.main_frame.pack(fill=BOTH, expand=True)

        self.form_frame = Frame(self.main_frame, bg="#D1E8FF", padx=20, pady=20)
        self.form_frame.grid(row=0, column=0, sticky="ew")

        self.labels = ["Name", "Salary", "PIN", "Experience", "Email", "Phone"]
        self.entries = []

        for idx, label in enumerate(self.labels):
            Label(self.form_frame, text=label, font=("Helvetica", 12, "bold"), bg="#D1E8FF").grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            entry = Entry(self.form_frame, font=("Helvetica", 12))
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky="ew")
            self.entries.append(entry)

        self.entry_name, self.entry_salary, self.entry_pin, self.entry_exp, self.entry_email, self.entry_phone = self.entries

        self.btn_frame = Frame(self.main_frame, bg="#ADD8E6", pady=10)
        self.btn_frame.grid(row=1, column=0, sticky="ew")

        self.buttons = [
            ("Add", self.add_programmer),
            ("Update", self.update_programmer),
            ("Delete", self.delete_programmer),
            ("Export CSV", self.export_to_csv),
            ("Clear", self.clear_fields)
        ]

        for idx, (text, command) in enumerate(self.buttons):
            btn = Button(self.btn_frame, text=text, font=("Helvetica", 12, "bold"), bg="#87CEEB", command=command)
            btn.grid(row=0, column=idx, padx=10, pady=5, sticky="ew")

        self.table_frame = Frame(self.main_frame)
        self.table_frame.grid(row=2, column=0, sticky="nsew")

        self.scroll_y = Scrollbar(self.table_frame, orient=VERTICAL)
        self.tree = ttk.Treeview(self.table_frame, columns=("ID", "Name", "Salary", "PIN", "Experience", "Email", "Phone"), show="headings", yscrollcommand=self.scroll_y.set)

        self.scroll_y.config(command=self.tree.yview)
        self.scroll_y.pack(side=RIGHT, fill=Y)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(fill=BOTH, expand=True)

        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.view_programmers()

    def connect_db(self):
        return sqlite3.connect("programmers.db")

    def animate_add(self):
        for i in range(5):
            self.root.update_idletasks()
            self.tree.tag_configure("fade", background=f"#D1FF{5-i}F")
            time.sleep(0.1)

    def add_programmer(self):
        name = self.entry_name.get()
        salary = self.entry_salary.get()
        pin = self.entry_pin.get()
        experience = self.entry_exp.get()
        email = self.entry_email.get()
        phone = self.entry_phone.get()

        if not all([name, salary, pin, experience, email, phone]):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            salary = float(salary)
            pin = int(pin)
            experience = int(experience)

            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO programmers (name, salary, pin, experience, email, phone)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, salary, pin, experience, email, phone))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"{name} added successfully!")
            self.view_programmers()
            self.clear_fields()
            self.animate_add()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add programmer: {e}")

    def view_programmers(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM programmers")
        rows = cursor.fetchall()
        conn.close()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for index, row in enumerate(rows):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=row, tags=(tag,))

        self.tree.tag_configure("evenrow", background="#f0f0f0")
        self.tree.tag_configure("oddrow", background="#e0e0e0")

    def update_programmer(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "No programmer selected!")
            return

        item = self.tree.item(selected[0])
        programmer_id = item["values"][0]

        name = self.entry_name.get()
        salary = self.entry_salary.get()
        pin = self.entry_pin.get()
        experience = self.entry_exp.get()
        email = self.entry_email.get()
        phone = self.entry_phone.get()

        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE programmers
            SET name=?, salary=?, pin=?, experience=?, email=?, phone=?
            WHERE id=?
            ''', (name, salary, pin, experience, email, phone, programmer_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Programmer updated successfully!")
            self.view_programmers()
            self.clear_fields()
            self.animate_add()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update programmer: {e}")

    def delete_programmer(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "No programmer selected!")
            return

        item = self.tree.item(selected[0])
        programmer_id = item["values"][0]

        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM programmers WHERE id=?", (programmer_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Programmer deleted successfully!")
            self.view_programmers()

            for i in range(5):
                self.root.update_idletasks()
                self.tree.tag_configure("fade", background=f"#FF{5-i}D1")
                time.sleep(0.1)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete programmer: {e}")

    def export_to_csv(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM programmers")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            messagebox.showerror("Error", "No data to export!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        if not file_path:
            return

        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Salary", "PIN", "Experience", "Email", "Phone"])
            writer.writerows(rows)

        messagebox.showinfo("Success", "Data exported successfully!")

    def clear_fields(self):
        self.entry_name.delete(0, END)
        self.entry_salary.delete(0, END)
        self.entry_pin.delete(0, END)
        self.entry_exp.delete(0, END)
        self.entry_email.delete(0, END)
        self.entry_phone.delete(0, END)

if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    app = ProgrammerManagementSystem(root)
    root.mainloop()
scroll_y.config(command=tree.yview)
scroll_y.pack(side=RIGHT, fill=Y)

for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(fill=BOTH, expand=True)

main_frame.grid_rowconfigure(2, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

view_programmers()

root.mainloop()
