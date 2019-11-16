-- CREATE TABLE student_course (
-- 		stud_id INT REFERENCES student (stud_id) ON UPDATE CASCADE ON DELETE CASCADE,
-- 		course_id INT REFERENCES course(course_id) ON UPDATE CASCADE ON DELETE CASCADE,
-- 		CONSTRAINT student_course_pkey PRIMARY KEY (course_id, stud_id)
-- );

-- Create table course_date
-- CREATE TABLE course_date (
-- 		id SERIAL PRIMARY KEY,
-- 		course_id INT REFERENCES course(course_id) ON UPDATE CASCADE ON DELETE CASCADE,
-- 		date_held DATE NOT NULL
-- 		)
-- 		
-- Adding date a course was held 
-- INSERT INTO course_date(course_id, date_held)
-- VALUES (2, '2019-11-15'), (2, '2019-11-18'), (2, '2019-11-20'), (2, '2019-11-22'), (2, '2019-11-25'), (2, '2019-11-27'), (2, '2019-11-29');

-- Adding a student to a course
-- INSERT INTO student_course
-- VALUES (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (0, 1);

-- Adding Courses 
-- INSERT INTO course
-- VALUES (3, 'Astronomy 1');

-- Create table student_course_date
-- CREATE TABLE student_course_date (
-- 		course_date_id INT REFERENCES course_date (id) ON UPDATE CASCADE ON DELETE CASCADE,
-- 		stud_id INT REFERENCES student(stud_id) ON UPDATE CASCADE ON DELETE CASCADE,
-- 		CONSTRAINT student_course_date_pkey PRIMARY KEY (course_date_id, stud_id)
-- 		)
-- 


-- Check a student as attended in a course C which was held in date D
-- INSERT INTO student_course_date(course_date_id, stud_id)
-- VALUES (8, 14)

--  Add some course session 
-- INSERT INTO course_date(course_id, date_held) 
--     SELECT 
-- 			2,	'2019-12-15'
-- WHERE NOT EXISTS (
--     SELECT 1 FROM course_date WHERE course_id=2 AND date_held='2019-12-15'
-- )
-- RETURNING id;

-- SELECT id
-- FROM course_date
-- WHERE course_id=2 AND date_held='2019-12-15' 
-- 
-- Select course_date_id
-- SELECT id
-- FROM course_date
-- WHERE course_id=1 AND date_held='2019-12-02'

-- Select id of a session where a course C were held at a date D
-- SELECT id
-- FROM course_date cd
-- LEFT JOIN course cc ON cd.course_id = cc.course_id
-- WHERE course_name LIKE 'Data Mining%' and date_held='2019-11-20';

-- Select course id by name
-- SELECT course_id
-- FROM course
-- WHERE course_name LIKE 'Data Mining%';

