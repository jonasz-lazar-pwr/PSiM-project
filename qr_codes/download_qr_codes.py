import requests
import os

# Ustalamy liczbę krasnali
num_of_dwarfs = 33

# Tworzymy folder na pulpicie, jeśli jeszcze nie istnieje
folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "qr_codes")
os.makedirs(folder_path, exist_ok=True)

# Przechodzimy przez wszystkie kody QR dostępnych krasnali
for i in range(1, num_of_dwarfs + 1):
    # Tworzymy URL do kodu QR krasnala
    url = f"http://localhost:8000/dwarfs/{i}/qr/"

    # Wysyłamy zapytanie GET do serwera i pobieramy kod QR
    response = requests.get(url)

    # Sprawdzamy, czy zapytanie zakończyło się sukcesem
    if response.status_code == 200:
        # Zapisujemy kod QR do pliku
        with open(os.path.join(folder_path, f"dwarf_{i}_qr.png"), "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed to download QR code for dwarf {i}")
