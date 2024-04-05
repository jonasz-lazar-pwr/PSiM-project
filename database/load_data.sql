DELETE FROM userachievements;
DELETE FROM achievements;
DELETE FROM comments;
DELETE FROM userdwarfs;
DELETE FROM dwarfs;
DELETE FROM users;


-- Dodanie użytkowników --
-- Dodanie użytkowników --
INSERT INTO users (username, password, joined_date)
VALUES
    ('user1', 'user1', NOW()),
    ('user2', 'user2', NOW()),
    ('user3', 'user3', NOW()),
    ('user4', 'user4', NOW()),
    ('user5', 'user5', NOW());


-- Dodanie odwiedzeń --
-- Użytkownik 1
INSERT INTO userdwarfs (user_id, dwarf_id, visited_date)
SELECT
    1 AS user_id,
    id AS dwarf_id,
    NOW() AS visited_date
FROM
    dwarfs
LIMIT 2;

-- Użytkownik 2
INSERT INTO userdwarfs (user_id, dwarf_id, visited_date)
SELECT
    2 AS user_id,
    id AS dwarf_id,
    NOW() AS visited_date
FROM
    dwarfs
LIMIT 2 OFFSET 2;

-- Użytkownik 3
INSERT INTO userdwarfs (user_id, dwarf_id, visited_date)
SELECT
    3 AS user_id,
    id AS dwarf_id,
    NOW() AS visited_date
FROM
    dwarfs
LIMIT 2 OFFSET 4;

-- Użytkownik 4
INSERT INTO userdwarfs (user_id, dwarf_id, visited_date)
SELECT
    4 AS user_id,
    id AS dwarf_id,
    NOW() AS visited_date
FROM
    dwarfs
LIMIT 2 OFFSET 6;

-- Użytkownik 5
INSERT INTO userdwarfs (user_id, dwarf_id, visited_date)
SELECT
    5 AS user_id,
    id AS dwarf_id,
    NOW() AS visited_date
FROM
    dwarfs
LIMIT 2 OFFSET 8;


-- Dodanie komentarzy --
-- Użytkownik 1
INSERT INTO comments (user_id, dwarf_id, comment_text, comment_date)
VALUES
    (1, 1, 'Bardzo podobał mi się ten krasnal!', NOW()),
    (1, 2, 'Świetna atrakcja, polecam!', NOW());

-- Użytkownik 2
INSERT INTO comments (user_id, dwarf_id, comment_text, comment_date)
VALUES
    (2, 3, 'Piękne miejsce, świetna zabawa dla dzieci!', NOW()),
    (2, 4, 'Ciekawa historia krasnali, warto zobaczyć.', NOW());

-- Użytkownik 3
INSERT INTO comments (user_id, dwarf_id, comment_text, comment_date)
VALUES
    (3, 5, 'Fantastyczne miejsce, niezapomniane wrażenia!', NOW()),
    (3, 6, 'Krasnale są urocze, zdjęcia wyszły świetnie.', NOW());

-- Użytkownik 4
INSERT INTO comments (user_id, dwarf_id, comment_text, comment_date)
VALUES
    (4, 7, 'Świetny krasnal, polecam odwiedzić!', NOW()),
    (4, 8, 'Bardzo interesująca historia tego krasnala.', NOW());

-- Użytkownik 5
INSERT INTO comments (user_id, dwarf_id, comment_text, comment_date)
VALUES
    (5, 9, 'Wspaniałe miejsce, świetna zabawa dla dzieci!', NOW()),
    (5, 10, 'Krasnale są pięknie wykonane, polecam zwiedzić.', NOW());


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
