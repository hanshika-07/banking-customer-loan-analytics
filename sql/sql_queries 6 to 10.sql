#6. Calculate monthly loan disbursement.

select
    DATE_FORMAT(application_date, '%Y-%m') as month,
    COUNT(*) as total_loans,
    SUM(loan_amount) as total_loan_value
from loans_cleaned
group by DATE_FORMAT(application_date, '%Y-%m')
order by  month;

#7. Calculate default rate by loan type.

select
    loan_type,
    COUNT(*) as total_loans,
    SUM(default_flag) as defaulted_loans,
    ROUND(
        SUM(default_flag) * 100.0 / COUNT(*),
        2
    ) as default_rate
from loans_cleaned
group by loan_type
order by default_rate DESC;

#8. Calculate default rate by customer segment.

select
    case
        when c.annual_income <= 1666666 then 'Low'
        when  c.annual_income <= 3333333 then 'Medium'
        else 'High'
    END as customer_segment,
    COUNT(l.loan_id) as total_loans,
    SUM(l.default_flag) as defaulted_loans,
    ROUND(
        SUM(l.default_flag) * 100.0 / COUNT(l.loan_id),
        2
    ) as default_rate
from loans_cleaned AS l
join customers_cleaned as  c
    on l.customer_id = c.customer_id
group by  customer_segment
order by  default_rate DESC;
    
#9. Find customers with more than one active loan.

select
	c.customer_name,
   count(l.loan_id) as active_loan
  from loans_cleaned as l 
join customers_cleaned as c
 on c.customer_id=l.customer_id 
  where loan_status="Active" 
  group by c.customer_name
  having count(l.loan_id)>1
  order by active_loan;
  
#10. Find customers whose total loan amount exceeds a selected threshold.

select 
    customer_id,
    SUM(loan_amount) AS total_loan_amount
  from loans_cleaned
group by customer_id
having SUM(loan_amount) > 1000000
order by  total_loan_amount DESC;