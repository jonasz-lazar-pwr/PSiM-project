DELETE FROM userachievements;
DELETE FROM achievements;
DELETE FROM comments;
DELETE FROM userdwarfs;
DELETE FROM dwarfs;
DELETE FROM users;


-- Dodanie użytkowników --
INSERT INTO users (username, password, joined_date)
VALUES
    ('user1', 'user1', NOW()),
    ('user2', 'user2', NOW()),
    ('user3', 'user3', NOW()),
    ('user4', 'user4', NOW()),
    ('user5', 'user5', NOW());


-- Dodanie odwiedzeń dla użytkownika 1 (id = 1) dla krasnali 1-10
INSERT INTO userdwarfs (user_id, dwarf_id, visited_date)
SELECT
    1 AS user_id,
    id AS dwarf_id,
    NOW() AS visited_date
FROM
    dwarfs
WHERE
    id BETWEEN 1 AND 10;

-- Dodanie odwiedzeń dla użytkownika 2 (id = 2) dla krasnali 5-15
INSERT INTO userdwarfs (user_id, dwarf_id, visited_date)
SELECT
    2 AS user_id,
    id AS dwarf_id,
    NOW() AS visited_date
FROM
    dwarfs
WHERE
    id BETWEEN 5 AND 15;


-- Dodanie komentarzy --
-- Użytkownik 1
INSERT INTO comments (user_id, dwarf_id, comment_text, comment_date)
VALUES
    (1, 1, 'Bardzo podobał mi się ten krasnal!', NOW()),
    (2, 2, 'Świetna atrakcja, polecam!', NOW()),
    (1, 3, 'Piękne miejsce, świetna zabawa dla dzieci!', NOW()),
    (2, 4, 'Ciekawa historia krasnali, warto zobaczyć.', NOW()),
    (1, 5, 'Fantastyczne miejsce, niezapomniane wrażenia!', NOW()),
    (2, 6, 'Krasnale są urocze, zdjęcia wyszły świetnie.', NOW()),
    (1, 7, 'Świetny krasnal, polecam odwiedzić!', NOW()),
    (2, 8, 'Bardzo interesująca historia tego krasnala.', NOW()),
    (1, 9, 'Wspaniałe miejsce, świetna zabawa dla dzieci!', NOW()),
    (2, 10, 'Krasnale są pięknie wykonane, polecam zwiedzić.', NOW()),
    (1, 11, 'Bardzo podobał mi się ten krasnal!', NOW()),
    (2, 12, 'Świetna atrakcja, polecam!', NOW()),
    (1, 13, 'Piękne miejsce, świetna zabawa dla dzieci!', NOW()),
    (2, 14, 'Ciekawa historia krasnali, warto zobaczyć.', NOW()),
    (1, 15, 'Fantastyczne miejsce, niezapomnione wrażenia!', NOW());


-- Dodanie osiągnięć --
INSERT INTO achievements (name, description)
VALUES
    ('Explorer', 'Odwiedziłeś więcej niż 5 krasnali.'),
    ('Commentator', 'Dodałeś komentarz do co najmniej 5 krasnali.'),
    ('Traveler', 'Odwiedziłeś więcej niż 10 krasnali.'),
    ('Super Explorer', 'Odwiedziłeś więcej niż 15 krasnali.'),
    ('Dwarf Master', 'Odwiedziłeś co najmniej 20 krasnali i dodałeś komentarz do co najmniej 10 z nich.');


-- Dodanie osiągnięć dla użytkowników
INSERT INTO userachievements (user_id, achievement_id, achievement_date)
VALUES
    (1, 1, NOW()),
    (2, 2, NOW()),
    (3, 3, NOW()),
    (4, 4, NOW()),
    (5, 5, NOW());
