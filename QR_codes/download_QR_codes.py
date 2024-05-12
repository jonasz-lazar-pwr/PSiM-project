# Autorzy: Jonasz Lazar, Kacper Malinowski

import os
import requests
import base64
from pathlib import Path

# Tworzenie folderu na pulpicie
desktop = Path.home() / 'Desktop'
folder = desktop / 'qr_codes'
folder.mkdir(parents=True, exist_ok=True)

# Wysyłanie zapytania GET do endpointu API
response = requests.get('http://localhost:8000/dwarfs')

# Sprawdzanie, czy zapytanie zakończyło się sukcesem
if response.status_code == 200:
    dwarfs_data = response.json()
    dwarfs = dwarfs_data['dwarfs']

    # Pobieranie i zapisywanie obrazów kodów QR
    for dwarf in dwarfs:
        qr_code_response = requests.get(f'http://localhost:8000/dwarfs/{dwarf["id"]}/qr_code/')

        # Sprawdzanie, czy zapytanie zakończyło się sukcesem
        if qr_code_response.status_code == 200:
            qr_code_data = qr_code_response.json()['qr_code']
            qr_code_image = base64.b64decode(qr_code_data)

            # Zapisywanie obrazu na dysku
            with open(os.path.join(folder, f'{dwarf["name"]}.png'), 'wb') as f:
                f.write(qr_code_image)