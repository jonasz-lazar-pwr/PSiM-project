# PSiM_project

## Struktura projektu

Projekt składa się z kilku głównych folderów i plików, które są opisane poniżej:

- **`app/`**: Główny folder aplikacji Django. Zawiera wszystkie pliki związane z logiką aplikacji.
  - **`app/static/`**: Folder zawierający statyczne pliki używane w projekcie, takie jak obrazy, skrypty JavaScript i arkusze stylów CSS.
    - **`app/static/css/`**: Folder zawierający arkusze stylów CSS używane w projekcie.
    - **`app/static/js/`**: Folder zawierający skrypty JavaScript używane w projekcie.
    - **`app/static/img/`**: Folder zawierający obrazy używane w projekcie.
  - **`app/templates/`**: Folder zawierający szablony HTML używane w projekcie.
    - **`app/templates/app/`**: Folder zawierający szablony HTML dla aplikacji.
      - **`app/templates/app/base.html`**: Główny szablon HTML, z którego dziedziczą inne szablony.
      - **`app/templates/app/comment_form.html`**: Szablon HTML reprezentujący formularz komentarza.
      - **`app/templates/app/dwarf_detail.html`**: Szablon HTML wyświetlający szczegóły krasnala.
      - **`app/templates/app/dwarfs.html`**: Szablon HTML wyświetlający listę krasnali.
      - **`app/templates/app/home.html`**: Szablon HTML dla strony głównej, z której można przejść do innych podstron.
      - **`app/templates/app/scan_qr_code.html`**: Szablon HTML dla funkcji skanowania kodów QR.
      - **`app/templates/app/user_achievements.html`**: Szablon HTML wyświetlający osiągnięcia użytkownika.
      - **`app/templates/app/user_comments.html`**: Szablon HTML wyświetlający komentarze użytkownika.
      - **`app/templates/app/user_ranking.html`**: Szablon HTML wyświetlający ranking użytkowników.
    - **`app/templates/registration/`**: Folder zawierający szablony HTML używane do obsługi rejestracji i logowania użytkowników.
      - **`app/templates/registration/login.html`**: Szablon HTML dla strony logowania.
      - **`app/templates/registration/register.html`**: Szablon HTML dla strony rejestracji.
  - `app/admin.py`: Plik konfigurujący panel administracyjny Django.
  - `app/forms.py`: Plik zawierający definicje formularzy Django używanych w projekcie.
  - `app/models.py`: Plik zawierający definicje modeli Django, które są używane do tworzenia tabel w bazie danych.
  - `app/views.py`: Plik zawierający definicje widoków Django, które są używane do obsługi żądań HTTP.
  - `app/urls.py`: Plik definiujący mapę adresów URL w aplikacji.

- **`database/`**: Folder zawierający pliki związane z bazą danych.
  - `database/create_database.sql`: Plik SQL używany do tworzenia struktury bazy danych.
  - `database/insert_data.sql`: Plik SQL używany do wstawiania danych do bazy danych.
  - `database/insert_dwarfs.py`: Plik Pythona używany do ładowania danych o krasnalach do bazy danych.
  - `database/dwarfs.json`: Plik JSON zawierający dane o krasnalach.

- **`PSiM_project/`**: Folder zawierający pliki konfiguracyjne Django.
  - `PSiM_project/settings.py`: Plik konfiguracyjny Django, zawierający ustawienia takie jak konfiguracja bazy danych, zainstalowane aplikacje, middleware i inne.
  - `PSiM_project/urls.py`: Plik definiujący główną mapę URL dla projektu Django.

- **`qr_codes/`**: Folder zawierający kody QR używane w projekcie.
  - `qr_codes/download_qr_codes.py`: Skrypt Pythona do pobierania kodów QR.
  - `qr_codes/*.png`: Pliki obrazów kodów QR.

- `README.md`: Plik zawierający podstawowe informacje o projekcie, takie jak opis, instrukcje instalacji i użycia.
- `.gitignore`: Plik używany przez Git do ignorowania określonych plików i folderów podczas śledzenia zmian.
- `requirements.txt`: Plik zawierający listę zależności Pythona wymaganych do uruchomienia projektu.

Pozostałe pliki i foldery wygenerowane automatycznie przez Django nie zostały modyfikowane i nie są wymienione powyżej.

## Instalacja i uruchomienie

1. **Sklonuj repozytorium na swoje lokalne środowisko.**

2. **Utwórz i skonfiguruj odpowiednie wirtualne środowisko, takie jak Conda lub venv (wirtualne środowisko Pythona).**

3. **Utwórz plik `.env` w głównym katalogu projektu i dodaj do niego następujące dane:**

    ```dotenv
    SECRET_KEY='your_secret_key'
    DB_ENGINE=your_db_engine
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=your_db_host
    DB_PORT=your_db_port
    ```

    Zastąp powyższe wartości rzeczywistymi danymi twojej bazy danych i projektu.

4. **Zainstaluj wymagane pakiety za pomocą pliku `requirements.txt`. Możesz to zrobić za pomocą następującej komendy:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Upewnij się, że masz zainstalowany pakiet `python-decouple`, który pozwoli na odczytanie zmiennych środowiskowych z pliku `.env`. Możesz to zrobić za pomocą następującej komendy:**

    ```bash
    pip install python-decouple
    ```

6. **Po utworzeniu pliku `.env` i zainstalowaniu `python-decouple`, upewnij się, że zmienne środowiskowe są odpowiednio umieszczone w pliku `settings.py` projektu Django:**

    ```python
    SECRET_KEY = config('SECRET_KEY')

    DATABASES = {
        'default': {
            'ENGINE': config('DB_ENGINE'),
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT'),
        }
    }
    ```

7. **Uruchom migracje, aby utworzyć tabele w bazie danych:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

8. **Uruchom serwer deweloperski Django:**

    ```bash
    python manage.py runserver
    ```

9. **Otwórz przeglądarkę internetową i przejdź do odpowiedniego adresu `http://localhost:8000/`.**
