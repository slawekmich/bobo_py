import datetime
import sqlite3

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

# Zmienna globalna przechowująca czas rozpoczęcia snu
sleep_start_time = None

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

# Funkcja pobierająca zdarzenia dla określonej daty
def get_events_by_date(date):
    c.execute("SELECT event_name, event_time FROM events WHERE DATE(event_time) = ?", (date,))
    return c.fetchall()
