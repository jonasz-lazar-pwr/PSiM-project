# PSiM_project

## Schemat podstron

### Strona główna:
- Prezentacja ogólnej informacji o aplikacji.
- Możliwość przejścia do logowania.
- Możliwość przeglądania Wrocławskich Krasnali (punkty POI).

### Przeglądanie Wrocławskich Krasnali (punkty POI):
- Przeglądanie listy nazw krasnali, kliknięcie nazwy wyświetla szczegóły krasnala (niezalogowany użytkownik nie może widzieć sekcji komentarzy przy krasnalu).
- Możliwość sortowania listy krasnali.
- Zalogowany użytkownik widzi komentarze innych użytkowników.
- Tylko użytkownik, który odblokował dostęp do krasnala poprzez zeskanowanie kodu QR z jego identyfikatorem, może dodać swój komentarz (wtedy otwiera się dla niego ten zasób).

### Panel logowania:
- Zawiera formularz logowania.

### Profil użytkownika:
- Dostępny po zalogowaniu.
- Możliwość przeglądnięcia osiągnięć "Moje osiągnięcia".
- Ranking użytkowników wg odwiedzeń.
- Możliwość zeskanowania kodu QR -> zeskanowanie odblokowuje zasób umożliwiający komentowanie i przenosi użytkownika na podstronę odblokowanego krasnala, oznaczenie go jako "odwiedzony".
- Przeglądanie krasnali (punkty POI), z tym że widzimy tutaj komentarze innych użytkowników (dyskusja) i możemy dodać swój, jeżeli mamy dostęp do zasobu. Jednocześnie widzimy informację, czy odwiedziliśmy już takiego krasnala, czy nie.
- Wylogowanie, przenosi na stronę główną.

#### Dodatkowo:
- Na początku będę korzystał z Bootstrapa (dla ułatwienia). W przyszłości zamienię to na zwykły CSS.
- Linki do podstron będą dostępne w górnym pasku nawigacji (navbar).

#### W przyszłości:
- Rejestracja użytkowników.
- Zarządzanie profilem użytkownika.

- TODO: Ogarnąć odznaki(osiągnięcia) i momenty ich nadawania (za liczbę odblokowanych krasnali i dodanych komentarzy)
