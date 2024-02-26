SELECT DISTINCT depositor.customer_name 
FROM depositor, account 
WHERE depositor.account_number = account.account_number 
AND account.branch_name IN (
    SELECT branch_name 
    FROM branch 
    WHERE branch_city = 'New York'
)
GROUP BY depositor.customer_name 
HAVING COUNT(*) = (
    SELECT COUNT(DISTINCT branch_name) 
    FROM branch 
    WHERE branch_city = 'New York'
);
