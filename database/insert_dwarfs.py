# Autorzy: Jonasz Lazar, Kacper Malinowski

from sqlalchemy import create_engine
import pandas as pd

# Ścieżka do pliku JSON
json_file_path = 'dwarfs.json'

# Ładowanie danych z pliku JSON do ramki danych
data = pd.read_json(json_file_path)

# Tworzenie silnika do połączenia z bazą danych
engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/dwarfsDB')

# Ładowanie danych do tabeli w bazie danych PostgreSQL
data.to_sql('dwarfs', engine, if_exists='append', index=False)
