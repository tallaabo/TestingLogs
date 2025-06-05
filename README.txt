📘 README.txt – Sample Checkout System

Overview
--------
This is a desktop application built with Python, Tkinter, tkcalendar, and SQLite. 
It lets you log “pickup” events by entering GID#, Test #, Primary Requester, Your Name, and Date (via a calendar picker). 
All data is saved persistently, automatically pruned after one year, and can be viewed or downloaded from a single window.

---

✅ Features
-----------
* **Barcode scanning (semicolon-separated)**  
  Scan or type a barcode string in the format to auto-fill GID#, Test #, and Primary Requester fields.

* **Manual entry and calendar picker**  
Manually enter Your Name and pick a Date from a calendar widget (`tkcalendar.DateEntry`).

* **Persistent storage with automatic pruning**  
On startup, any record with a saved Date more than 365 days earlier is automatically deleted. 
New entries are saved into a local SQLite database (`sample_log.db`), 
but in production will be swapped out for the company’s cloud database.

* **Last 20 entries always visible**  
The main window displays the 20 most recent saved entries for quick confirmation.

* **View All Logs in a resizable window**  
Click **“View All Logs”** to open a separate, resizable window showing every record in descending order.

* **Download all logs as CSV**  
Click **“Download All Logs (CSV)”** to export the entire log history to a `.csv` file.

* **Delete All Logs (password-protected)**  
Click **“Delete All Logs”**, enter the admin password (`admin123` by default), and 
confirm to remove every entry in the database.

---

💻 Requirements
---------------
* **Python 3.x**  
* **tkcalendar** (install with `pip install tkcalendar`)  
* Standard library modules: `tkinter`, `sqlite3`, `csv`, `datetime`, etc.

Works on Windows, macOS, or Linux. Ensure your Python environment has `tkcalendar` installed before running.

---

📁 How to Run
-------------
1. Open a terminal or VS Code integrated terminal.  
2. Navigate to the folder containing `main.py`.  
3. Run:

4. The application will open, automatically delete any entries older than one year (based on their saved Date), 
and display the last 20 saved entries. You’re ready to scan or type barcodes, fill in the remaining fields, and save.

---

🧠 File Descriptions
--------------------
* **`main.py`**  
- Contains all application logic, GUI setup, and database routines.  
- On startup:
 1. Creates (or reuses) `sample_log.db`.  
 2. Automatically deletes any entry whose saved Date is more than 365 days before today.  
 3. Displays the 20 most recent entries in the main window.  
- Implements:
 - Semicolon-based barcode parsing (`handle_scan`)
 - Calendar date picker (`tkcalendar.DateEntry`)
 - “Last 20 Entries” list
 - “View All Logs” window
 - CSV export
 - Password-protected “Delete All Logs”

* **`sample_log.db`**  
- An auto-created SQLite database that persistently stores every submitted record.  
- Table schema:
 ```
 id                INTEGER PRIMARY KEY AUTOINCREMENT
 gid               TEXT    NOT NULL
 test_number       TEXT    NOT NULL
 primary_requester TEXT    NOT NULL
 your_name         TEXT    NOT NULL
 date              TEXT    NOT NULL  (format YYYY-MM-DD)
 ```

* **`README.txt`**  
- This file. Provides an overview, feature list, requirements, and instructions.

---

📝 Notes
--------
* **Barcode scanning is not fully integrated yet.**  
Once approved, we will connect barcode input and all reads/writes to the company’s central database 
(rather than local SQLite) so that GID#, Test #, and Primary Requester can be verified and stored in the cloud.

* **Current storage is local SQLite.**  
In a future rollout, `sample_log.db` will be replaced by the company’s remote database. 
That change requires minimal code updates to swap the `sqlite3` calls for the company’s database client.

* **Barcode format**  
Expect exactly three fields separated by semicolons (e.g., `ABC123;T456;Alice Smith`). 
If your scanner only provides a single code, you can type that into the “Scan Barcode” field—then manually 
fill in Test # and Primary Requester before submitting.

* **Date selection**  
The Date field uses a calendar picker (`tkcalendar.DateEntry`) so you can click to choose a date in `YYYY-MM-DD` format.

* **Last 20 saved entries**  
The main window always shows the 20 most recent rows sorted by insertion time for quick confirmation that 
your last submissions were saved.

* **“View All Logs”**  
Opens a separate, resizable window listing every saved record in descending order of entry ID.

* **“Download All Logs (CSV)”**  
Creates a CSV backup containing all fields (`GID#`, `Test #`, `Primary Requester`, `Your Name`, `Date`).

* **“Delete All Logs”**  
Prompts for the admin password (`admin123` by default). Upon confirmation, it deletes every record from 
the `samples` table and refreshes the main window.

* **Automatic pruning**  
On each startup, the app runs a single SQL command:
```sql
DELETE FROM samples WHERE date < '<YYYY-MM-DD threshold>'

## License
This project is proprietary to 3M.  
Do not redistribute or modify without permission.

## Contributing
1. Fork or clone this repo.  
2. Create a new branch for your feature or fix.  
3. Submit a pull request to `main`.
