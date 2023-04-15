---Create view RESTAURANT_BUSINESSINFO 
---Filter all restaurant business information
CREATE VIEW RESTAURANT_BUSINESSINFO AS
SELECT *
FROM BUSINESSINFO
WHERE BUSINESSINFO.ID IN
		(SELECT BUSINESS_ID
			FROM CATEGORY_IN_BUSINESS
			WHERE CATEGORY_ID = 18 );

---Create view checkin_expand 
---For all the 6 periods in a day and 7 days in a week, count checkin numbers of business in these total 42(6*7) time periods
CREATE VIEW checkin_expand AS
SELECT business_id, 
       COUNT(CASE WHEN day_of_week = 1 AND hour >= 0 AND hour <= 6 THEN checkin_count ELSE NULL END) AS Mon_0_6,
	   COUNT(CASE WHEN day_of_week = 1 AND hour >= 7 AND hour <= 10 THEN checkin_count ELSE NULL END) AS Mon_7_10,
	   COUNT(CASE WHEN day_of_week = 1 AND hour >= 11 AND hour <= 13 THEN checkin_count ELSE NULL END) AS Mon_11_13,
	   COUNT(CASE WHEN day_of_week = 1 AND hour >= 14 AND hour <= 17 THEN checkin_count ELSE NULL END) AS Mon_14_17,
	   COUNT(CASE WHEN day_of_week = 1 AND hour >= 18 AND hour <= 20 THEN checkin_count ELSE NULL END) AS Mon_18_20,
	   COUNT(CASE WHEN day_of_week = 1 AND hour >= 21 AND hour <= 23 THEN checkin_count ELSE NULL END) AS Mon_21_23,
	   COUNT(CASE WHEN day_of_week = 2 AND hour >= 0 AND hour <= 6 THEN checkin_count ELSE NULL END) AS Tue_0_6,
	   COUNT(CASE WHEN day_of_week = 2 AND hour >= 7 AND hour <= 10 THEN checkin_count ELSE NULL END) AS Tue_7_10,
	   COUNT(CASE WHEN day_of_week = 2 AND hour >= 11 AND hour <= 13 THEN checkin_count ELSE NULL END) AS Tue_11_13,
	   COUNT(CASE WHEN day_of_week = 2 AND hour >= 14 AND hour <= 17 THEN checkin_count ELSE NULL END) AS Tue_14_17,
	   COUNT(CASE WHEN day_of_week = 2 AND hour >= 18 AND hour <= 20 THEN checkin_count ELSE NULL END) AS Tue_18_20,
	   COUNT(CASE WHEN day_of_week = 2 AND hour >= 21 AND hour <= 23 THEN checkin_count ELSE NULL END) AS Tue_21_23,
	   COUNT(CASE WHEN day_of_week = 3 AND hour >= 0 AND hour <= 6 THEN checkin_count ELSE NULL END) AS Wed_0_6,
	   COUNT(CASE WHEN day_of_week = 3 AND hour >= 7 AND hour <= 10 THEN checkin_count ELSE NULL END) AS Wed_7_10,
	   COUNT(CASE WHEN day_of_week = 3 AND hour >= 11 AND hour <= 13 THEN checkin_count ELSE NULL END) AS Wed_11_13,
	   COUNT(CASE WHEN day_of_week = 3 AND hour >= 14 AND hour <= 17 THEN checkin_count ELSE NULL END) AS Wed_14_17,
	   COUNT(CASE WHEN day_of_week = 3 AND hour >= 18 AND hour <= 20 THEN checkin_count ELSE NULL END) AS Wed_18_20,
	   COUNT(CASE WHEN day_of_week = 3 AND hour >= 21 AND hour <= 23 THEN checkin_count ELSE NULL END) AS Wed_21_23,
	   COUNT(CASE WHEN day_of_week = 4 AND hour >= 0 AND hour <= 6 THEN checkin_count ELSE NULL END) AS Thur_0_6,
	   COUNT(CASE WHEN day_of_week = 4 AND hour >= 7 AND hour <= 10 THEN checkin_count ELSE NULL END) AS Thur_7_10,
	   COUNT(CASE WHEN day_of_week = 4 AND hour >= 11 AND hour <= 13 THEN checkin_count ELSE NULL END) AS Thur_11_13,
	   COUNT(CASE WHEN day_of_week = 4 AND hour >= 14 AND hour <= 17 THEN checkin_count ELSE NULL END) AS Thur_14_17,
	   COUNT(CASE WHEN day_of_week = 4 AND hour >= 18 AND hour <= 20 THEN checkin_count ELSE NULL END) AS Thur_18_20,
	   COUNT(CASE WHEN day_of_week = 4 AND hour >= 21 AND hour <= 23 THEN checkin_count ELSE NULL END) AS Thur_21_23,
	   COUNT(CASE WHEN day_of_week = 5 AND hour >= 0 AND hour <= 6 THEN checkin_count ELSE NULL END) AS Fri_0_6,
	   COUNT(CASE WHEN day_of_week = 5 AND hour >= 7 AND hour <= 10 THEN checkin_count ELSE NULL END) AS Fri_7_10,
	   COUNT(CASE WHEN day_of_week = 5 AND hour >= 11 AND hour <= 13 THEN checkin_count ELSE NULL END) AS Fri_11_13,
	   COUNT(CASE WHEN day_of_week = 5 AND hour >= 14 AND hour <= 17 THEN checkin_count ELSE NULL END) AS Fri_14_17,
	   COUNT(CASE WHEN day_of_week = 5 AND hour >= 18 AND hour <= 20 THEN checkin_count ELSE NULL END) AS Fri_18_20,
	   COUNT(CASE WHEN day_of_week = 5 AND hour >= 21 AND hour <= 23 THEN checkin_count ELSE NULL END) AS Fri_21_23,
	   COUNT(CASE WHEN day_of_week = 6 AND hour >= 0 AND hour <= 6 THEN checkin_count ELSE NULL END) AS Sat_0_6,
	   COUNT(CASE WHEN day_of_week = 6 AND hour >= 7 AND hour <= 10 THEN checkin_count ELSE NULL END) AS Sat_7_10,
	   COUNT(CASE WHEN day_of_week = 6 AND hour >= 11 AND hour <= 13 THEN checkin_count ELSE NULL END) AS Sat_11_13,
	   COUNT(CASE WHEN day_of_week = 6 AND hour >= 14 AND hour <= 17 THEN checkin_count ELSE NULL END) AS Sat_14_17,
	   COUNT(CASE WHEN day_of_week = 6 AND hour >= 18 AND hour <= 20 THEN checkin_count ELSE NULL END) AS Sat_18_20,
	   COUNT(CASE WHEN day_of_week = 6 AND hour >= 21 AND hour <= 23 THEN checkin_count ELSE NULL END) AS Sat_21_23,
	   COUNT(CASE WHEN day_of_week = 0 AND hour >= 0 AND hour <= 6 THEN checkin_count ELSE NULL END) AS Sun_0_6,
	   COUNT(CASE WHEN day_of_week = 0 AND hour >= 7 AND hour <= 10 THEN checkin_count ELSE NULL END) AS Sun_7_10,
	   COUNT(CASE WHEN day_of_week = 0 AND hour >= 11 AND hour <= 13 THEN checkin_count ELSE NULL END) AS Sun_11_13,
	   COUNT(CASE WHEN day_of_week = 0 AND hour >= 14 AND hour <= 17 THEN checkin_count ELSE NULL END) AS Sun_14_17,
	   COUNT(CASE WHEN day_of_week = 0 AND hour >= 18 AND hour <= 20 THEN checkin_count ELSE NULL END) AS Sun_18_20,
	   COUNT(CASE WHEN day_of_week = 0 AND hour >= 21 AND hour <= 23 THEN checkin_count ELSE NULL END) AS Sun_21_23
FROM (
  SELECT c.business_id, 
         c.date_hour, 
         EXTRACT(DOW FROM c.date_hour) AS day_of_week, 
         EXTRACT(HOUR FROM c.date_hour) AS hour,
         c.checkin_count
  FROM checkin c
) subquery
GROUP BY business_id;

---Create VIEW RESTAURANT_BUSINESSINFO_checkin
---Join RESTAURANT_BUSINESSINFO and checkin_expand together by business_id
CREATE VIEW RESTAURANT_BUSINESSINFO_checkin AS
SELECT *
FROM RESTAURANT_BUSINESSINFO
JOIN checkin_expand
ON RESTAURANT_BUSINESSINFO.id = checkin_expand.business_id;

---CREATE VIEW RESTAURANT_BUSINESSINFO_checkin_population
---Join RESTAURANT_BUSINESSINFO_checkin and population together by zipcode
CREATE VIEW RESTAURANT_BUSINESSINFO_checkin_population AS
SELECT *
FROM RESTAURANT_BUSINESSINFO_checkin
JOIN population
ON RESTAURANT_BUSINESSINFO_checkin.zipcode = population.zipcode;

---Create view RESTAURANT_REVIEW 
---Filter all restaurant business reviews
CREATE VIEW RESTAURANT_REVIEW AS
SELECT *
FROM review
WHERE review.business_id IN
	(SELECT BUSINESS_ID
	 FROM CATEGORY_IN_BUSINESS
	 WHERE CATEGORY_ID = 18 )
order by review.business_id;





