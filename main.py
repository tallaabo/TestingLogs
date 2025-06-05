import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk, filedialog, simpledialog
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import csv

# === Setup SQLite Database ===
conn = sqlite3.connect("sample_log.db")
cursor = conn.cursor()


# Create the table with updated schema
cursor.execute('''
    CREATE TABLE IF NOT EXISTS samples (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gid TEXT NOT NULL,
        test_number TEXT NOT NULL,
        primary_requester TEXT NOT NULL,
        your_name TEXT NOT NULL,
        date TEXT NOT NULL
    )
''')
conn.commit()

# === Automatically delete any row whose "date" is more than 365 days ago ===
one_year_ago = datetime.now() - timedelta(days=365)
threshold = one_year_ago.strftime("%Y-%m-%d")

cursor.execute("DELETE FROM samples WHERE date < ?", (threshold,))
conn.commit()

# === Function to Refresh Last 20 Logs in Treeview ===
def refresh_logs():
    for row in logs_tree.get_children():
        logs_tree.delete(row)
    cursor.execute(
        "SELECT gid, test_number, primary_requester, your_name, date "
        "FROM samples ORDER BY id DESC LIMIT 20"
    )
    for entry in cursor.fetchall():
        logs_tree.insert("", tk.END, values=entry)

# === Function to Parse Barcode Scan Input (semicolon‐separated) ===
def handle_scan(event=None):
    scanned = scan_entry.get().strip()
    if not scanned:
        return

    # Expecting format: GID#;Test#;PrimaryRequester
    parts = scanned.split(";")
    if len(parts) >= 3:
        gid_entry.delete(0, tk.END)
        test_entry.delete(0, tk.END)
        requester_entry.delete(0, tk.END)

        gid_entry.insert(0, parts[0].strip())
        test_entry.insert(0, parts[1].strip())
        requester_entry.insert(0, parts[2].strip())
    else:
        messagebox.showwarning(
            "Scan Error",
            "Barcode data not in expected format.\nUse GID#;Test#;PrimaryRequester"
        )

    scan_entry.delete(0, tk.END)

# === Function to Submit Entry ===
def submit_entry():
    gid = gid_entry.get().strip()
    test_number = test_entry.get().strip()
    primary_requester = requester_entry.get().strip()
    your_name = name_entry.get().strip()
    date = date_entry.get_date().strftime("%Y-%m-%d")

    if not gid or not test_number or not primary_requester or not your_name or not date:
        messagebox.showwarning("Missing Info", "Please fill in all fields.")
        return

    cursor.execute(
        "INSERT INTO samples (gid, test_number, primary_requester, your_name, date) "
        "VALUES (?, ?, ?, ?, ?)",
        (gid, test_number, primary_requester, your_name, date)
    )
    conn.commit()
    messagebox.showinfo("Success", "Entry saved!")
    gid_entry.delete(0, tk.END)
    test_entry.delete(0, tk.END)
    requester_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    date_entry.set_date(datetime.now())

    refresh_logs()

# === View All Entries Function ===
def view_all():
    top = tk.Toplevel(root)
    top.title("All Sample Checkouts")
    # top.geometry("700x400")

    tree = ttk.Treeview(top, columns=("GID#", "Test #", "Primary Requester", "Your Name", "Date"), show='headings')
    tree.heading("GID#", text="GID#")
    tree.heading("Test #", text="Test #")
    tree.heading("Primary Requester", text="Primary Requester")
    tree.heading("Your Name", text="Your Name")
    tree.heading("Date", text="Date")
    tree.pack(fill=tk.BOTH, expand=True)

    cursor.execute("SELECT gid, test_number, primary_requester, your_name, date FROM samples ORDER BY id DESC")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

# === Export All Entries to CSV ===
def export_to_csv():
    filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")])
    if filename:
        cursor.execute("SELECT gid, test_number, primary_requester, your_name, date FROM samples ORDER BY id DESC")
        rows = cursor.fetchall()
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["GID#", "Test #", "Primary Requester", "Your Name", "Date"])
            writer.writerows(rows)
        messagebox.showinfo("Exported", f"All logs exported to:\n{filename}")

# === Clear All Logs with Password Confirmation ===
def clear_logs():
    password = simpledialog.askstring("Password Required", "Enter admin password to delete ALL logs:", show='*')
    if password == "admin123":  # Change to your own secure password if needed
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete ALL logs?"):
            cursor.execute("DELETE FROM samples")
            conn.commit()
            messagebox.showinfo("Cleared", "All logs have been deleted.")
            refresh_logs()
    else:
        messagebox.showerror("Access Denied", "Incorrect password. Logs not deleted.")

# === Main GUI Setup ===
root = tk.Tk()
root.title(f"{datetime.now().year} Pickup of Accelerated Weathered Samples Log")
# root.geometry("700x700")
root.resizable(True, True)

# === Scan Section ===
scan_frame = ttk.LabelFrame(root, text="Scan Barcode (GID#;Test#;PrimaryRequester)")
scan_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
scan_entry = ttk.Entry(scan_frame, width=60)
scan_entry.pack(padx=10, pady=5)
scan_entry.bind("<Return>", handle_scan)

# === Form Fields ===
form_frame = ttk.Frame(root)
form_frame.pack(fill=tk.X, padx=10, pady=10)

ttk.Label(form_frame, text="GID#:").grid(row=0, column=0, sticky=tk.W, pady=5)
gid_entry = ttk.Entry(form_frame, width=40)
gid_entry.grid(row=0, column=1, pady=5, padx=(0, 10))

ttk.Label(form_frame, text="Test #:").grid(row=1, column=0, sticky=tk.W, pady=5)
test_entry = ttk.Entry(form_frame, width=40)
test_entry.grid(row=1, column=1, pady=5, padx=(0, 10))

ttk.Label(form_frame, text="Primary Requester:").grid(row=2, column=0, sticky=tk.W, pady=5)
requester_entry = ttk.Entry(form_frame, width=40)
requester_entry.grid(row=2, column=1, pady=5, padx=(0, 10))

ttk.Label(form_frame, text="Your Name:").grid(row=3, column=0, sticky=tk.W, pady=5)
name_entry = ttk.Entry(form_frame, width=40)
name_entry.grid(row=3, column=1, pady=5, padx=(0, 10))

ttk.Label(form_frame, text="Date:").grid(row=4, column=0, sticky=tk.W, pady=5)
date_entry = DateEntry(
    form_frame, width=37, background='darkblue',
    foreground='white', borderwidth=2, date_pattern='yyyy-MM-dd'
)
date_entry.grid(row=4, column=1, pady=5, padx=(0, 10))
date_entry.set_date(datetime.now())

# === Buttons for Submit and Log Management ===
button_frame = ttk.Frame(root)
button_frame.pack(fill=tk.X, padx=10)

submit_btn = ttk.Button(button_frame, text="Submit Entry", command=submit_entry)
submit_btn.grid(row=0, column=0, padx=(0, 10), pady=(0, 10))

view_all_btn = ttk.Button(button_frame, text="View All Logs", command=view_all)
view_all_btn.grid(row=0, column=1, padx=(0, 10), pady=(0, 10))

export_btn = ttk.Button(button_frame, text="Download All Logs (CSV)", command=export_to_csv)
export_btn.grid(row=0, column=2, padx=(0, 10), pady=(0, 10))

clear_btn = ttk.Button(button_frame, text="Delete All Logs", command=clear_logs)
clear_btn.grid(row=0, column=3, padx=(0, 10), pady=(0, 10))

# === Logs List (Last 20) ===
logs_frame = ttk.LabelFrame(root, text="Last 20 Entries")
logs_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

columns = ("GID#", "Test #", "Primary Requester", "Your Name", "Date")
logs_tree = ttk.Treeview(logs_frame, columns=columns, show="headings", height=10)
for col in columns:
    logs_tree.heading(col, text=col)
    logs_tree.column(col, width=130, anchor=tk.CENTER)
logs_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Populate initial logs
refresh_logs()

# === Start the App ===
root.mainloop()

# === Close Database on Exit ===
conn.close()
