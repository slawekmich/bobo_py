import tkinter as tk
import datetime
import bobo_logic as logic
from tkinter import messagebox

# Funkcja obsługująca przyciski zdarzeń
def event_button_click(event_name):
    logic.save_event(event_name)
    messagebox.showinfo("Potwierdzenie", "Zdarzenie zapisane do bazy danych.")

# Funkcja obsługująca przyciski snu
def sleep_button_click(button_name):
    global sleep_start_time
    now = datetime.datetime.now()
    if button_name == "Start":
        sleep_start_time = now.strftime("%Y-%m-%d %H:%M:%S")
        messagebox.showinfo("Potwierdzenie", "Rozpoczęto pomiar czasu snu.")
    elif button_name == "Stop":
        sleep_end_time = now.strftime("%Y-%m-%d %H:%M:%S")
        sleep_duration = logic.calculate_sleep_duration(sleep_start_time, sleep_end_time)
        logic.save_sleep_time(sleep_start_time, sleep_end_time)
        messagebox.showinfo("Potwierdzenie", f"Czas snu: {sleep_duration}. Zapisano do bazy danych.")

# Tworzenie interfejsu użytkownika
root = tk.Tk()
root.title("Aplikacja Zdarzeń")
root.geometry("400x300")

# Przyciski dla zdarzeń
event_buttons_frame = tk.Frame(root)
event_buttons_frame.pack()

milk_button = tk.Button(event_buttons_frame, text="Mleko", command=lambda: event_button_click("Mleko"))
milk_button.pack(side=tk.LEFT)

pee_button = tk.Button(event_buttons_frame, text="Sik", command=lambda: event_button_click("Sik"))
pee_button.pack(side=tk.LEFT)

poop_button = tk.Button(event_buttons_frame, text="Kupa", command=lambda: event_button_click("Kupa"))
poop_button.pack(side=tk.LEFT)

# Przyciski dla snu
sleep_buttons_frame = tk.Frame(root)
sleep_buttons_frame.pack()

sleep_start_button = tk.Button(sleep_buttons_frame, text="Start", command=lambda: sleep_button_click("Start"))
sleep_start_button.pack(side=tk.LEFT)

sleep_stop_button = tk.Button(sleep_buttons_frame, text="Stop", command=lambda: sleep_button_click("Stop"))
sleep_stop_button.pack(side=tk.LEFT)

# Wyświetlanie podsumowania zdarzeń każdego dnia
summary_frame = tk.Frame(root)
summary_frame.pack()

def get_daily_summary():
    today = datetime.date.today()
    logic.c.execute("SELECT event_name, event_time FROM events WHERE DATE(event_time) = ?", (today,))
    events = logic.c.fetchall()

    summary = ""
    for event in events:
        event_name = event[0]
        event_time = event[1]
        if event_name.startswith("sen"):
            summary += f"{event_name}: {event_time}\n"
        else:
            summary += f"{event_name} - {event_time}\n"

    messagebox.showinfo("Podsumowanie zdarzeń", f"Podsumowanie zdarzeń dzisiaj:\n\n{summary}")

summary_button = tk.Button(summary_frame, text="Podsumowanie zdarzeń dzisiaj", command=get_daily_summary)
summary_button.pack()

