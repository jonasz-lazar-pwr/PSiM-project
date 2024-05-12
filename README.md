# PSiM_project

## Struktura projektu

Projekt składa się z dwóch głównych części: backendu (Django) i frontendu (React). Poniżej znajduje się opis struktury katalogów i plików w projekcie:

- **`PSiM_project/`**: Główny katalog projektu Django.
  - **`PSiM_project/settings.py`**: Plik konfiguracyjny Django, zawierający ustawienia takie jak konfiguracja bazy danych, zainstalowane aplikacje, middleware i inne.
  - **`PSiM_project/urls.py`**: Plik definiujący główną mapę URL dla projektu Django.
  - **`PSiM_project/asgi.py`**: Plik konfiguracyjny ASGI dla serwera Django.
  - **`PSiM_project/wsgi.py`**: Plik konfiguracyjny WSGI dla serwera Django.
- **`backend/`**: Folder zawierający pliki związane z backendem stworzonym w Django.
  - **`backend/migrations/`**: Folder zawierający migracje Django.
  - **`backend/admin.py`**: Plik zawierający konfigurację panelu administracyjnego Django.
  - **`backend/apps.py`**: Plik zawierający konfigurację aplikacji Django.
  - **`backend/models.py`**: Plik zawierający modele Django.
  - **`backend/serializers.py`**: Plik zawierający serializatory Django REST Framework.
  - **`backend/tests.py`**: Plik, w którym można umieścić testy jednostkowe dla aplikacji Django.
  - **`backend/urls.py`**: Plik zawierający mapę URL dla aplikacji Django.
  - **`backend/utils.py`**: Plik zawierający funkcje pomocnicze.
  - **`backend/views.py`**: Plik zawierający widoki Django (wg wzorca Django REST Framework).
- **`frontend/`**: Folder zawierający pliki związane z frontendem stworzonym w React.
  - **`frontend/public/`**: Folder zawierający pliki publiczne, takie jak pliki HTML, ikony, obrazy itp.
  - **`frontend/src/`**: Folder zawierający pliki źródłowe React.
    - **`frontend/src/components/`**: Folder zawierający komponenty React.
    - **`frontend/src/pages/`**: Folder zawierający strony React.
    - **`frontend/src/context/`**: Folder zawierający kontekst React.
    - **`frontend/src/App.js`**: Plik zawierający główny komponent aplikacji React.
    - **`frontend/src/index.js`**: Plik zawierający punkt wejścia dla aplikacji React.
  - **`frontend/.env`**: Plik zawierający zmienne środowiskowe dla aplikacji React. *Plik ten nie jest dodany do repozytorium, ponieważ zawiera poufne dane.*
  - **`frontend/package.json`**: Plik zawierający informacje o projekcie, zależności i skrypty.
- **`database/`**: Folder zawierający pliki związane z stworzeniem i wypełnieniem bazy danych.
  - **`database/create_database.sql`**: Plik SQL używany do tworzenia struktury bazy danych.
  - **`database/insert_data.sql`**: Plik SQL używany do wstawiania danych do bazy danych.
  - **`database/insert_dwarfs.py`**: Plik Pythona używany do ładowania danych o krasnalach do bazy danych.
  - **`database/dwarfs.json`**: Plik JSON zawierający dane o krasnalach.
- **`QR_codes/`**: Folder zawierający kody QR używane w projekcie. 
  - **`QR_codes/download_qr_codes.py`**: Skrypt Pythona do pobierania kodów QR.
  - **`QR_codes/*.png`**: Pliki obrazów kodów QR.
- **`README.md`**: Plik zawierający informacje o projekcie, takie jak opisy plików i katalogów, instrukcje instalacji i uruchomienia projektu.
- **`requirements.txt`**: Plik zawierający listę zależności Pythona.
- **`.gitignore`**: Plik zawierający listę plików i katalogów, które mają być ignorowane przez system kontroli wersji Git.
- **`.env`**: Plik zawierający zmienne środowiskowe dla projektu Django. *Plik ten nie jest dodany do repozytorium, ponieważ zawiera poufne dane.*
- **`manage.py`**: Plik zarządzający Django.

## Instalacja i uruchomienie backendu (Django oraz baza danych)

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


## Instalacja i uruchomienie frontendu (React)

1. **Zainstaluj Node.js na swoim komputerze. Możesz pobrać Node.js ze strony [https://nodejs.org/](https://nodejs.org/).**

2. **W głównym katalogu projektu utwórz nowy projekt React za pomocą komendy `npx create-react-app <nazwa_projektu>`.**

3. **Przejdź do katalogu projektu React `/frontend` i zainstaluj wymagane pakiety za pomocą komendy `npm install`.**

4. **Utwórz plik `.env` w katalogu projektu React i dodaj do niego następujące dane:**

    ```dotenv
    GENERATE_SOURCEMAP=false
    REACT_APP_API_URL='http://localhost:8000'
    ```
    Zastąp powyższą wartość rzeczywistym adresem URL backendu Django.

5. **Uruchom serwer deweloperski React za pomocą komendy `npm start`.**

6. **Otwórz przeglądarkę internetową i przejdź do odpowiedniego adresu `http://localhost:3000/`.**

Przykładową implementację projektu można zobaczyć na stronie [https://wroclawskie-krasnale-28f39b99bec7.herokuapp.com/](https://wroclawskie-krasnale-28f39b99bec7.herokuapp.com/).

## Autorzy
- Jonasz Lazar
- Kazper Malinowski
