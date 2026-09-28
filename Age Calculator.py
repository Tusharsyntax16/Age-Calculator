import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
import calendar


# =====================================================
# MONTHS
# =====================================================

months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]


# =====================================================
# CALENDAR POPUP
# =====================================================

def open_calendar(month_box, day_box, year_box):

    popup = tk.Toplevel(root)
    popup.title("Select Date")
    popup.geometry("330x350")
    popup.resizable(False, False)
    popup.transient(root)
    popup.grab_set()

    cal = Calendar(
        popup,
        selectmode="day",
        date_pattern="dd/mm/yyyy",
        font=("Arial", 12),
        background="#0f4c81",
        foreground="white",
        headersbackground="#0f4c81",
        headersforeground="white",
        selectbackground="#4b8125",
        selectforeground="white"
    )

    cal.pack(padx=15, pady=15)

    def select_date():

        selected = cal.get_date()

        day, month, year = selected.split("/")

        day_box.set(int(day))
        month_box.set(months[int(month) - 1])
        year_box.set(int(year))

        popup.destroy()

    tk.Button(
        popup,
        text="Select Date",
        command=select_date,
        font=("Arial", 12, "bold"),
        bg="#4b8125",
        fg="white",
        padx=25,
        pady=8,
        relief="flat",
        cursor="hand2"
    ).pack(pady=5)


# =====================================================
# CALCULATE AGE
# =====================================================

def calculate_age():

    try:

        # ---------------- DOB ----------------

        dob_day = int(dob_day_box.get())
        dob_month = dob_month_box.current() + 1
        dob_year = int(dob_year_box.get())

        # ---------------- PRESENT DATE ----------------

        present_day = int(present_day_box.get())
        present_month = present_month_box.current() + 1
        present_year = int(present_year_box.get())

        # =================================================
        # CREATE DOB
        # =================================================

        dob = datetime(
            dob_year,
            dob_month,
            dob_day,
            0,
            0,
            0
        )

        # =================================================
        # PRESENT DATE + CURRENT TIME
        # =================================================

        now = datetime.now()

        selected_date = datetime(
            present_year,
            present_month,
            present_day
        )

        # If selected date is today,
        # use current time

        if selected_date.date() == now.date():
            present = now

        else:
            present = selected_date

        # =================================================
        # VALIDATION
        # =================================================

        if present < dob:

            messagebox.showerror(
                "Invalid Date",
                "Present date cannot be before Date of Birth!"
            )

            return

        # =================================================
        # EXACT AGE
        # =================================================

        years = present.year - dob.year
        age_months = present.month - dob.month
        age_days = present.day - dob.day

        hours = present.hour - dob.hour
        minutes = present.minute - dob.minute
        seconds = present.second - dob.second

        # =================================================
        # BORROW SECONDS
        # =================================================

        if seconds < 0:

            seconds += 60
            minutes -= 1

        # =================================================
        # BORROW MINUTES
        # =================================================

        if minutes < 0:

            minutes += 60
            hours -= 1

        # =================================================
        # BORROW HOURS
        # =================================================

        if hours < 0:

            hours += 24
            age_days -= 1

        # =================================================
        # BORROW DAYS
        # =================================================

        if age_days < 0:

            age_months -= 1

            if present.month == 1:

                previous_month = 12
                previous_year = present.year - 1

            else:

                previous_month = present.month - 1
                previous_year = present.year

            age_days += calendar.monthrange(
                previous_year,
                previous_month
            )[1]

        # =================================================
        # BORROW MONTHS
        # =================================================

        if age_months < 0:

            years -= 1
            age_months += 12

        # =================================================
        # TOTAL VALUES
        # =================================================

        difference = present - dob

        total_seconds = int(
            difference.total_seconds()
        )

        total_minutes = total_seconds // 60

        total_hours = total_seconds // 3600

        total_days = total_seconds // 86400

        total_weeks = total_days // 7

        extra_days = total_days % 7

        total_months = years * 12 + age_months

        # =================================================
        # RESULT
        # =================================================

        result = (
            f"AGE\n\n"

            f"{years} Years   "
            f"{age_months} Months   "
            f"{age_days} Days\n"

            f"{hours} Hours   "
            f"{minutes} Minutes   "
            f"{seconds} Seconds\n\n"

            f"──────────────────────────────\n\n"

            f"Total Months   : {total_months:,}\n"
            f"Total Weeks    : {total_weeks:,} Weeks "
            f"{extra_days} Days\n"
            f"Total Days     : {total_days:,}\n"
            f"Total Hours    : {total_hours:,}\n"
            f"Total Minutes  : {total_minutes:,}\n"
            f"Total Seconds  : {total_seconds:,}"
        )

        result_label.config(
            text=result,
            fg="#333333"
        )

    except ValueError:

        messagebox.showerror(
            "Invalid Date",
            "Please select a valid date."
        )


# =====================================================
# MAIN WINDOW
# =====================================================

root = tk.Tk()

root.title("Age Calculator")

root.geometry("850x780")

root.minsize(700, 700)

root.configure(
    bg="#f4f4f4"
)


# =====================================================
# TITLE
# =====================================================

tk.Label(
    root,
    text="Age Calculator",
    font=("Arial", 32, "bold"),
    fg="#064b7a",
    bg="#f4f4f4"
).pack(
    anchor="w",
    padx=30,
    pady=(20, 15)
)


# =====================================================
# YEARS / DAYS
# =====================================================

current_year = datetime.now().year

years = list(
    range(1900, current_year + 1)
)

days = list(
    range(1, 32)
)


# =====================================================
# DATE ROW CREATOR
# =====================================================

def create_date_row(
    parent,
    default_month,
    default_day,
    default_year
):

    frame = tk.Frame(
        parent,
        bg="#f4f4f4"
    )

    frame.pack(
        pady=3
    )

    # ---------------- MONTH ----------------

    month_box = ttk.Combobox(
        frame,
        values=months,
        width=11,
        font=("Arial", 14),
        state="readonly"
    )

    month_box.current(
        default_month
    )

    month_box.grid(
        row=0,
        column=0,
        padx=4,
        ipady=6
    )

    # ---------------- DAY ----------------

    day_box = ttk.Combobox(
        frame,
        values=days,
        width=5,
        font=("Arial", 14),
        state="readonly"
    )

    day_box.set(
        default_day
    )

    day_box.grid(
        row=0,
        column=1,
        padx=4,
        ipady=6
    )

    # ---------------- YEAR ----------------

    year_box = ttk.Combobox(
        frame,
        values=years,
        width=8,
        font=("Arial", 14),
        state="readonly"
    )

    year_box.set(
        default_year
    )

    year_box.grid(
        row=0,
        column=2,
        padx=4,
        ipady=6
    )

    return (
        frame,
        month_box,
        day_box,
        year_box
    )


# =====================================================
# DATE OF BIRTH
# =====================================================

tk.Label(
    root,
    text="Date of Birth",
    font=("Arial", 19, "bold"),
    bg="#f4f4f4",
    fg="#444444"
).pack(
    anchor="w",
    padx=30,
    pady=(3, 2)
)


dob_frame, dob_month_box, dob_day_box, dob_year_box = create_date_row(
    root,
    0,
    1,
    2000
)


# =====================================================
# DOB CALENDAR BUTTON
# =====================================================

tk.Button(
    dob_frame,
    text="📅",
    font=("Arial", 14),
    command=lambda: open_calendar(
        dob_month_box,
        dob_day_box,
        dob_year_box
    ),
    bg="#286090",
    fg="white",
    relief="flat",
    cursor="hand2",
    width=3
).grid(
    row=0,
    column=3,
    padx=6,
    ipady=4
)


# =====================================================
# PRESENT DATE
# =====================================================

tk.Label(
    root,
    text="Age at the Date of",
    font=("Arial", 19, "bold"),
    bg="#f4f4f4",
    fg="#555555"
).pack(
    anchor="w",
    padx=30,
    pady=(12, 2)
)


today = datetime.now()


present_frame, present_month_box, present_day_box, present_year_box = create_date_row(
    root,
    today.month - 1,
    today.day,
    today.year
)


# =====================================================
# PRESENT DATE CALENDAR BUTTON
# =====================================================

tk.Button(
    present_frame,
    text="📅",
    font=("Arial", 14),
    command=lambda: open_calendar(
        present_month_box,
        present_day_box,
        present_year_box
    ),
    bg="#286090",
    fg="white",
    relief="flat",
    cursor="hand2",
    width=3
).grid(
    row=0,
    column=3,
    padx=6,
    ipady=4
)


# =====================================================
# CALCULATE BUTTON
# =====================================================

tk.Button(
    root,
    text="Calculate  ▶",
    command=calculate_age,
    font=("Arial", 17, "bold"),
    bg="#4b8125",
    fg="white",
    activebackground="#39651c",
    activeforeground="white",
    padx=35,
    pady=8,
    relief="flat",
    cursor="hand2"
).pack(
    pady=15
)


# =====================================================
# RESULT BOX
# =====================================================

result_box = tk.Frame(
    root,
    bg="white",
    bd=1,
    relief="solid"
)

result_box.pack(
    padx=30,
    pady=2,
    fill="both",
    expand=True
)


# =====================================================
# RESULT HEADER
# =====================================================

tk.Label(
    result_box,
    text="Result",
    font=("Arial", 20, "bold"),
    fg="white",
    bg="#4b8125",
    anchor="w",
    padx=15,
    pady=5
).pack(
    fill="x"
)


# =====================================================
# RESULT TEXT
# =====================================================

result_label = tk.Label(
    result_box,
    text="Enter your dates and click Calculate",
    font=("Arial", 14),
    bg="white",
    fg="#555555",
    justify="left",
    anchor="nw",
    padx=20,
    pady=10
)

result_label.pack(
    fill="both",
    expand=True
)


# =====================================================
# START PROGRAM
# =====================================================

root.mainloop()