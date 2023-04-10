CREATE VIEW restaurant_businessinfo AS
SELECT *
FROM businessinfo
WHERE businessinfo.id IN (
	SELECT business_id 
	FROM category_in_business 
	WHERE category_id = 18
);

SELECT * FROM restaurant_businessinfo;
