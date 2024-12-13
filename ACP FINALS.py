import tkinter as tk
from tkinter import messagebox
import datetime
import csv


start_time = None
usage_log = []
tracking = False
DAILY_LIMIT = datetime.timedelta(hours=2)

def start_tracking():
    global start_time, tracking
    if tracking:
        messagebox.showerror("Error", "Tracking is already in progress!")
        return

    start_time = datetime.datetime.now()
    tracking = True
    log_label["text"] = "Tracking started..."
    update_timer()

def stop_tracking():
    global start_time, tracking
    if not tracking:
        messagebox.showerror("Error", "No active tracking session.")
        return

    stop_time = datetime.datetime.now()
    duration = stop_time - start_time
    usage_log.append({"start": start_time, "end": stop_time, "duration": duration})
    tracking = False
    log_label["text"] = f"Last session duration: {duration}"
    total_usage_label["text"] = calculate_total_usage()
    check_daily_limit()

def calculate_total_usage():
    if not usage_log:
        return "Total Usage: 0 hours, 0 minutes"

    total_duration = sum([entry["duration"] for entry in usage_log], datetime.timedelta())
    hours, remainder = divmod(total_duration.total_seconds(), 3600)
    minutes, _ = divmod(remainder, 60)
    return f"Total Usage: {int(hours)} hours, {int(minutes)} minutes"

def check_daily_limit():
    total_duration = sum([entry["duration"] for entry in usage_log if entry["start"].date() == datetime.datetime.now().date()], datetime.timedelta())
    if total_duration >= DAILY_LIMIT:
        messagebox.showwarning("Warning", "You have exceeded your daily screen time limit!")

def update_timer():
    if tracking:
        elapsed = datetime.datetime.now() - start_time
        timer_label["text"] = f"Elapsed Time: {str(elapsed).split('.')[0]}"
        timer_label.after(1000, update_timer)

def export_usage_log():
    if usage_log:
        with open("usage_log.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Start Time", "End Time", "Duration"])
            for entry in usage_log:
                writer.writerow([entry["start"].strftime("%Y-%m-%d %H:%M:%S"), entry["end"].strftime("%Y-%m-%d %H:%M:%S"), entry["duration"]])
        messagebox.showinfo("Export", "Usage log exported to usage_log.csv successfully!")
    else:
        messagebox.showerror("Error", "No usage data to export.")

def view_usage_log():
    history_window = tk.Toplevel(root)
    history_window.title("Usage Log")
    for entry in usage_log:
        tk.Label(history_window, text=f"Start: {entry['start']}, End: {entry['end']}, Duration: {entry['duration']}").pack()

def reset_log():
    global usage_log
    if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset the usage log?"):
        usage_log = []
        log_label["text"] = "Usage log reset."
        total_usage_label["text"] = "Total Usage: 0 hours, 0 minutes"


root = tk.Tk()
root.title("ScreenTime Tracker")


bg_image = tk.PhotoImage(file=r"C:\Users\andre\Downloads\Motivational-Quotes-PNG-Image-Background.png")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1, y=174)  


timer_label = tk.Label(root, text="Elapsed Time: 00:00:00", font=("Helvetica", 20, "bold"), bg="lightyellow", fg="black")
timer_label.pack(pady=20)


button_style = {"font": ("Helvetica", 16, "bold"), "width": 25, "height": 2}

start_button = tk.Button(root, text="Start Tracking", command=start_tracking, bg="#E0F7FA", fg="black", **button_style)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Tracking", command=stop_tracking, bg="#FFCDD2", fg="black", **button_style)
stop_button.pack(pady=10)

export_button = tk.Button(root, text="Export Log", command=export_usage_log, bg="#F1F8E9", fg="black", **button_style)
export_button.pack(pady=10)

view_log_button = tk.Button(root, text="View Usage Log", command=view_usage_log, bg="#FFF9C4", fg="black", **button_style)
view_log_button.pack(pady=10)

reset_button = tk.Button(root, text="Reset Log", command=reset_log, bg="#D1C4E9", fg="black", **button_style)
reset_button.pack(pady=10)


log_label = tk.Label(root, text="", font=("Helvetica", 14, "italic"), fg="blue", bg="lightyellow")
log_label.pack(pady=20)

total_usage_label = tk.Label(root, text="Total Usage: 0 hours, 0 minutes", font=("Helvetica", 14, "italic"), fg="blue", bg="lightyellow")
total_usage_label.pack(pady=20)


root.mainloop()
