#16. Calculate average days late by loan type.

select
	  l.loan_type ,
      ROUND(avg(lp.days_late),2) as average_days 
from loan_payments_cleaned as lp
join loans_cleaned as l
on lp.loan_id=l.loan_id
group by loan_type
order by average_days desc;

#17. Find loans with repeated late or missed payments.

Select
    loan_id,
    COUNT(*) as late_or_missed_payments
from loan_payments_cleaned
where payment_status IN ('Late', 'Missed')
group by  loan_id
having COUNT(*) >= 2
order by late_or_missed_payments DESC;


#18. Rank branches by loan value using a window function.

with cte as (
    select
        branch_id,
        SUM(loan_amount) as total_loan_value
    from loans_cleaned
    group by branch_id
)
select
    branch_id,
    total_loan_value,
    dense_rank() OVER (
        order by total_loan_value DESC
    ) AS br
from cte
order by br;

#19. Calculate each loan type's percentage contribution to total loan value.

Select
    loan_type,
    SUM(loan_amount) as loan_value,
    ROUND(
        SUM(loan_amount) * 100 /
        (Select SUM(loan_amount) from loans_cleaned),
        2
    ) as percentage_contribution
from loans_cleaned
group by loan_type
order by percentage_contribution DESC;

#20. Identify customers whose loan amount is high relative to annual income.

Select
    c.customer_id,
    c.customer_name,
    c.annual_income,
    SUM(l.loan_amount) AS total_loan_amount,
    ROUND(
        SUM(l.loan_amount) / NULLIF(c.annual_income, 0),
        2
    ) as loan_to_income_ratio
from customers_cleaned as c
join loans_cleaned as l
    on c.customer_id = l.customer_id
group by
    c.customer_id,
    c.customer_name,
    c.annual_income
having loan_to_income_ratio > 3
order by loan_to_income_ratio DESC;