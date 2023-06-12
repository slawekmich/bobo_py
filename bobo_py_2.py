import tkinter as tk
import datetime
import sqlite3
from tkinter import messagebox

# Tworzenie połączenia z bazą danych
conn = sqlite3.connect('events.db')
c = conn.cursor()

# Tworzenie tabeli w bazie danych, jeśli nie istnieje
c.execute('''CREATE TABLE IF NOT EXISTS events
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              event_name TEXT,
              event_time TEXT)''')

# Zliczanie liczby zdarzeń snu
c.execute("SELECT COUNT(*) FROM events WHERE event_name LIKE 'sen%'")
sleep_event_count = c.fetchone()[0]

# Funkcja obsługująca zapisywanie zdarzeń do bazy danych
def save_event(event_name):
    now = datetime.datetime.now()
    event_time = now.strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO events (event_name, event_time) VALUES (?, ?)", (event_name, event_time))
    conn.commit()

# Funkcja obsługująca zapisywanie czasu snu do bazy danych
def save_sleep_time(start_time, end_time):
    global sleep_event_count
    sleep_event_count += 1
    sleep_event_name = "sen" + str(sleep_event_count)
    c.execute("INSERT INTO events (event_name, event_time) VALUES (?, ?)", (sleep_event_name, start_time))
    conn.commit()
    c.execute("INSERT INTO events (event_name, event_time) VALUES (?, ?)", (sleep_event_name, end_time))
    conn.commit()

# Funkcja obliczająca czas trwania snu
def calculate_sleep_duration(start_time, end_time):
    start_datetime = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_datetime = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    sleep_duration = end_datetime - start_datetime
    return str(sleep_duration)

# Funkcja obsługująca przyciski zdarzeń
def event_button_click(event_name):
    save_event(event_name)
    messagebox.showinfo("Potwierdzenie", "Zdarzenie zapisane do bazy danych.")

# Funkcja obsługująca przyciski snu
def sleep_button_click(button_name):
    now = datetime.datetime.now()
    if button_name == "Start":
        sleep_start_time = now.strftime("%Y-%m-%d %H:%M:%S")
        messagebox.showinfo("Potwierdzenie", "Rozpoczęto pomiar czasu snu.")
    elif button_name == "Stop":
        sleep_end_time = now.strftime("%Y-%m-%d %H:%M:%S")
        sleep_duration = calculate_sleep_duration(sleep_start_time, sleep_end_time)
        save_sleep_time(sleep_start_time, sleep_end_time)
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
    c.execute("SELECT event_name, event_time FROM events WHERE DATE(event_time) = ?", (today,))
    events = c.fetchall()

    messagebox.showinfo("Podsumowanie zdarzeń", "Podsumowanie zdarzeń dzisiaj:\n\n{}".format("\n".join([f"{event[0]} - {event[1]}" for event in events])))

summary_button = tk.Button(summary_frame, text="Podsumowanie zdarzeń dzisiaj", command=get_daily_summary)
summary_button.pack()

# Uruchomienie aplikacji
root.mainloop()
