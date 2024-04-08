# PSiM_project

## Struktura projektu

Projekt składa się z kilku głównych części:

- **`app/`**: Główny folder aplikacji Django. Zawiera wszystkie pliki związane z logiką aplikacji.
  - **`app/static/`**: Folder zawierający statyczne pliki używane w projekcie, takie jak obrazy, skrypty JavaScript i arkusze stylów CSS.
    - **`app/static/css/`**: Folder zawierający arkusze stylów CSS używane w projekcie.
    - **`app/static/js/`**: Folder zawierający skrypty JavaScript używane w projekcie.
  - **`app/templates/`**: Folder zawierający szablony HTML używane w projekcie.
    - **`app/templates/app/`**: Folder zawierający szablony HTML specyficzne dla aplikacji.
    - **`app/templates/registration/`**: Folder zawierający szablony HTML używane do obsługi rejestracji i logowania użytkowników.
  - **Pliki:**
    - `app/admin.py`: Plik konfigurujący panel administracyjny Django.
    - `app/forms.py`: Plik zawierający definicje formularzy Django używanych w projekcie.
    - `app/models.py`: Plik zawierający definicje modeli Django, które są używane do tworzenia tabel w bazie danych.
    - `app/views.py`: Plik zawierający definicje widoków Django, które są używane do obsługi żądań HTTP.
    - `app/urls.py`: Plik definiujący mapę URL dla aplikacji.

- **`database/`**: Folder zawierający pliki związane z bazą danych.
  - **Pliki:**
    - `database/create_database.sql`: Plik SQL używany do tworzenia struktury bazy danych.
    - `database/insert_data.sql`: Plik SQL używany do wstawiania danych do bazy danych.
    - `database/load_dwarfs.py`: Plik Pythona używany do ładowania danych o krasnalach do bazy danych.
    - `database/dwarfs.json`: Plik JSON zawierający dane o krasnalach.

- **`PSiM_project/`**: Folder zawierający pliki konfiguracyjne Django.
  - **Pliki:**
    - `PSiM_project/settings.py`: Plik konfiguracyjny Django, zawierający ustawienia takie jak konfiguracja bazy danych, zainstalowane aplikacje, middleware i inne.
    - `PSiM_project/urls.py`: Plik definiujący główną mapę URL dla projektu Django.

- **Pliki:**
  - `README.md`: Plik zawierający podstawowe informacje o projekcie, takie jak opis, instrukcje instalacji i użycia.
  - `.gitignore`: Plik używany przez Git do ignorowania określonych plików i folderów podczas śledzenia zmian.

  
## Instalacja i uruchomienie

1. **Sklonuj repozytorium na swoje lokalne środowisko.**

2. **Utwórz plik `.env` w głównym katalogu projektu i dodaj do niego następujące dane:**

    ```dotenv
    SECRET_KEY='your_secret_key'
    DB_ENGINE=your_db_engine
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=your_db_host
    DB_PORT=your_db_port
    ```

    Zastąp powyższe wartości swoimi rzeczywistymi danymi. Plik `.env` jest ignorowany przez Git (dzięki plikowi `.gitignore`).

3. **Zainstaluj pakiet `python-decouple`, który pozwoli na odczytanie zmiennych środowiskowych z pliku `.env`. Możesz to zrobić za pomocą następującej komendy:**

    ```bash
    pip install python-decouple
    ```

4. **Po utworzeniu pliku `.env` i zainstalowaniu `python-decouple`, przypisz zmienne środowiskowe w odpowiednie miejsca do pliku `settings.py` projektu Django:**

    ```python
    from decouple import config

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

5. **Uruchom migracje, aby utworzyć tabele w bazie danych:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Uruchom serwer deweloperski Django:**

    ```bash
    python manage.py runserver
    ```

7. **Otwórz przeglądarkę internetową i przejdź do odpowiedniego adresu `http://localhost:8000/`.**
