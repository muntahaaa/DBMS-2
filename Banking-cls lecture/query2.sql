SELECT customer_name 
FROM depositor 
WHERE account_number IN (
    SELECT account_number 
    FROM account 
    WHERE branch_name IN (
        SELECT branch_name 
        FROM branch 
        WHERE branch_city = 'New York'
    )
) 
GROUP BY customer_name 
HAVING COUNT(account_number) = (
    SELECT COUNT(DISTINCT branch_name) 
    FROM branch 
    WHERE branch_city = 'New York'
);
