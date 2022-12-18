/* 1. Add queries to retrieve the data from you database
1.1 Noncorrelated and Correlated Subqueries in Select */
SELECT id_post, title, (SELECT ROUND(AVG(LENGTH(title)), 1) FROM posts) AS average_len_title FROM posts;

SELECT p.id_post, p.title, (SELECT COUNT(*) FROM photos AS ph WHERE p.id_post = ph.post_id) AS numb_photos
FROM posts AS p;

/* 1.2 Write at least one From clause with subquery in it */

SELECT id_user, first_name, last_name, description FROM (SELECT  u.id_user, u.first_name, u.last_name, tp.description
FROM users AS u, userPermission AS up, typePermission AS tp WHERE u.id_user = up.user_id
and  up.type_permission_id = tp.id_type_permission and tp.description = 'writer') AS user_writer;

/* 1.3 Write at least one Where clause with subquery in it */

SELECT p.id_post, p.title FROM posts AS p WHERE
 (SELECT count(*) FROM userComments AS uc WHERE p.id_post = uc.post_id) > 2;

/* 1.4 Use WITH clause (Common Table Expression) */

WITH category_2 AS (SELECT p.id_post, p.title, c.description FROM posts AS p, categories AS c
WHERE p.category_id = c.id_category and c.description = 'Topic 2')
SELECT id_post, title, description, (SELECT ROUND(AVG(LENGTH(title)), 1)  FROM category_2) AS average_len_title
FROM category_2;

/* 1.5 Group the data by some field and filter it with Having clause */

SELECT u.id_user, u.first_name, u.last_name, count(*) AS num_posts FROM users AS u INNER JOIN posts AS p
ON u.id_user = p.user_id GROUP BY u.id_user HAVING COUNT(*) > 2;

/* 1.6 Use Order by */

SELECT * FROM posts ORDER BY user_id;

/* 1.7 Use Limit */

SELECT * FROM posts ORDER BY user_id LIMIT 5;

/* 2. Add queries that work with multiple table to retrieve the data from you database
2.1 INNER, LEFT, RIGHT, OUTER joins */

SELECT c.description, COUNT(*) AS num_posts FROM categories c INNER JOIN posts AS p ON c.id_category = p.category_id
GROUP BY c.description ORDER BY c.description;

SELECT u.id_user, u.first_name, u.last_name, count(*) AS num_comments FROM userComments AS uc LEFT JOIN users AS u
ON uc.user_id = u.id_user GROUP BY u.id_user;

SELECT p.id_post, p.title, count(*) AS num_comments FROM userComments AS uc RIGHT JOIN posts AS p
ON p.id_post = uc.post_id GROUP BY p.id_post;

SELECT  (SELECT tp.description FROM typePermission AS tp WHERE tp.id_type_permission = up.type_permission_id)
AS description, up.type_permission_id , count(*) as num_user FROM users AS u FULL JOIN userPermission AS up
ON u.id_user = up.user_id GROUP BY up.type_permission_id ORDER BY description;

/* 2.2 USING

I don't have two tables with the same column names

2.3 NATURAL JOIN

I don't have two tables with the same column names

2.4 CROSS JOIN*/

SELECT u.id_user, u.first_name, u.last_name, c.description FROM users AS u CROSS JOIN categories as c;

/* 2.5 SELF JOIN */

SELECT p1.category_id,
(SELECT c.description FROM categories AS c WHERE p1.category_id = c.id_category ) as description, p1.title, p2.title
FROM posts p1 INNER JOIN posts p2 ON p1.id_post <> p2.id_post AND p1.category_id = p2.category_id
ORDER BY description , p1.title;

/* 2.6 UNION */

SELECT * FROM categories
UNION
SELECT * FROM typePermission;

/* 2.7 EXCEPT and INTERSECT */

SELECT u.id_user, u.first_name, u.last_name FROM users AS u WHERE id_user = (SELECT u.id_user EXCEPT
SELECT p.user_id FROM posts AS p);

SELECT u.id_user, u.first_name, u.last_name FROM users AS u WHERE id_user = (SELECT u.id_user INTERSECT
SELECT p.user_id FROM posts AS p);

/* 3 Add statements to work with the db.
3.1 transactions (at least 2) */

START TRANSACTION;
INSERT INTO categories (description) VALUES ('T6');
INSERT INTO categories (description) VALUES ('N7');
UPDATE categories SET description = 'N7' WHERE description = 'T7';
COMMIT;

START TRANSACTION;
DELETE FROM categories WHERE description = 'T6';
DELETE FROM categories WHERE description = 'T7';
COMMIT;

/* 3.2 coalesce */

SELECT u.id_user, u.first_name, u.last_name, coalesce(p.title, 'no posts') FROM users AS u FULL OUTER JOIN posts AS p
ON u.id_user = p.user_id;

/* 3.3 cast */

SELECT id_user, first_name, last_name, registration_date, CAST(registration_date AS DATE) FROM users;

/* 3.4 case when */

SELECT u.id_user, u.first_name, u.last_name, p.title FROM users AS u FULL OUTER JOIN posts AS p
ON u.id_user = p.user_id;

SELECT u.id_user, u.first_name, u.last_name, CASE WHEN p.title = NULL THEN 0 ELSE 1 END AS is_post
FROM users AS u FULL OUTER JOIN posts AS p ON u.id_user = p.user_id;

/* 3.5 use different datetime functions */

SELECT id_user, first_name, last_name, registration_date, CAST(registration_date AS DATE),
AGE(registration_date), CURRENT_TIME, date_part('decade', registration_date) FROM users;