-- Autorzy: Jonasz Lazar, Kacper Malinowski

-- Dodanie osiągnięć --
INSERT INTO achievements (name, comment_count, dwarf_count, description, badge_icon)
VALUES
    ('Explorer', 0, 10, 'Odwiedziłeś 10 krasnali.', 'icons/explorer.svg'),
    ('Super Explorer', 0, 20, 'Odwiedziłeś 20 krasnali.', 'icons/super_explorer.svg'),
    ('Master Explorer', 0, 30, 'Odwiedziłeś 30 krasnali.', 'icons/master_explorer.svg'),
    ('Traveler', 0, 40, 'Odwiedziłeś 40 krasnali.', 'icons/traveler.svg'),
    ('Super Traveler', 0, 50, 'Odwiedziłeś 50 krasnali.', 'icons/super_traveler.svg'),
    ('Master Traveler', 0, 60, 'Odwiedziłeś 60 krasnali.', 'icons/master_traveler.svg'),
    ('Commentator', 10, 0, 'Dodałeś 10 komentarzy.', 'icons/commentator.png'),
    ('Super Commentator', 30, 0, 'Dodałeś 30 komentarzy.', 'icons/super_commentator.png'),
    ('Master Commentator', 50, 0, 'Dodałeś 50 komentarzy.', 'icons/master_commentator.png');

-- Dodanie zdobytych krasnali --
INSERT INTO userdwarfs (user_id, dwarf_id, visited_date)
SELECT users.id, dwarfs.id, NOW()
FROM
    (SELECT id FROM users) AS users
CROSS JOIN
    (SELECT id FROM dwarfs WHERE id <= 40) AS dwarfs
WHERE dwarfs.id BETWEEN ((users.id - 1) * 8 + 1) AND (users.id * 8);

-- Dodanie komentarzy --
INSERT INTO comments (user_id, dwarf_id, comment_text, comment_date)
SELECT user_id, dwarf_id, 'Świetny krasnal!', NOW()
FROM
    (SELECT user_id, MIN(dwarf_id) as dwarf_id FROM userdwarfs GROUP BY user_id) as user_dwarfs;

INSERT INTO comments (user_id, dwarf_id, comment_text, comment_date)
SELECT user_id, dwarf_id, 'Niezwykły krasnal!', NOW()
FROM
    (SELECT user_id, MAX(dwarf_id) as dwarf_id FROM userdwarfs GROUP BY user_id) as user_dwarfs;

INSERT INTO comments (user_id, dwarf_id, comment_text, comment_date)
SELECT user_id, dwarf_id, 'Cudowny krasnal!', NOW()
FROM
    (SELECT user_id, AVG(dwarf_id) as dwarf_id FROM userdwarfs GROUP BY user_id) as user_dwarfs;

