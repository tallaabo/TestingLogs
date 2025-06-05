 📘 `README.txt` – Sample Checkout System

Overview
This is a simple desktop application built using Python, Tkinter, and SQLite. It allows a user to log sample pickups, view records, search by sample name, export to CSV, and clear logs — all from one window.

---

✅ Features

* Enter and save sample checkout details (name, date, time, sample)
* View all logged sample entries
* Search logs by sample name
* Export all data to a `.csv` spreadsheet
* Clear all logs with confirmation

---

💻 Requirements

* Python 3.x installed
* Works on Windows, Mac, or Linux

No extra libraries are needed — only standard Python modules are used.

---

📁 How to Run

1. Open your terminal or VS Code terminal.
2. Navigate to the folder containing `main.py`.
3. Run the following command:

   ```
   python main.py
   ```
4. The app window will open — ready to use.

---

🧠 File Descriptions

* `main.py` – The main application with all functionality
* `sample_log.db` – Auto-created database file that stores all log entries
* `README.txt` – Instructions and overview (this file)

---

📝 Notes

* All entries are stored locally in `sample_log.db`
* Use the **Export to CSV** button to save a backup or share logs
* Use **Clear All Logs** carefully — it deletes everything!

