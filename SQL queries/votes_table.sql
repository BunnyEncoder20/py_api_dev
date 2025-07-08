SELECT * FROM public.votes_table
ORDER BY user_id ASC, post_id ASC;

SELECT * FROM public.posts_table_v2
ORDER BY id ASC;

-- adding dummy data to votes table (user 24 did not vote)
INSERT INTO votes_table (user_id, post_id) VALUES
(6, 1),
(6, 5),
(6, 8),
(7, 9),
(7, 10),
(18, 11),
(18, 12),
(19, 13),
(19, 14),
(20, 15),
(20, 16),
(21, 17),
(21, 18),
(22, 19),
(23, 20);

-- Left JOIN
SELECT * FROM posts_table_v2
LEFT JOIN users ON posts_table_v2.user_id = users.id;

-- Right JOIN (notice the null entries)
SELECT * FROM posts_table_v2
RIGHT JOIN users ON posts_table_v2.user_id = users.id;

-- Counting Rows (Notice count of 1 for users with no posts)
-- This is cause COUNT(*) is counting all the rows
SELECT users.id, COUNT(*) from posts_table_v2
RIGHT JOIN users ON posts_table_v2.user_id = users.id
GROUP BY users.id
ORDER BY users.id ASC;

-- We can avoid that by specifying which col to COUNT(col_name)
-- That way, null entries of that col_name will not be counted
SELECT users.id, users.email, COUNT(posts_table_v2.id) as User_Posts_Count from posts_table_v2
RIGHT JOIN users ON posts_table_v2.user_id = users.id
GROUP BY users.id
ORDER BY users.id ASC;

-- This shows all the posts and their votes (but also the posts with no votes)
SELECT * FROM posts_table_v2
LEFT JOIN votes_table ON posts_table_v2.id = votes_table.post_id;

-- This shows all the posts and their votes (but skips the posts with no votes)
SELECT * FROM posts_table_v2
RIGHT JOIN votes_table ON posts_table_v2.id = votes_table.post_id;

-- To count votes of each post, group them together by post_id
SELECT id AS POST_ID, COUNT(votes_table.post_id) AS VOTES FROM posts_table_v2
LEFT JOIN votes_table ON posts_table_v2.id = votes_table.post_id
GROUP BY posts_table_v2.id;

-- To count votes of ONE specific post, just add a where clause
-- This is probably the query we want to use
SELECT id AS POST_ID, COUNT(votes_table.post_id) AS VOTES FROM posts_table_v2
LEFT JOIN votes_table ON posts_table_v2.id = votes_table.post_id
WHERE posts_table_v2.id = 16
GROUP BY posts_table_v2.id;
