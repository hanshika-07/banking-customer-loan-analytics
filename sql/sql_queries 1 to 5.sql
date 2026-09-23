#SQL QUERIES

# 1 Calculate total customers by state.

  select
		count(*) as total_customers ,state
  from customers_cleaned as  c
  join branches_cleaned as b
  on c.city=b.city
  group by state;
 
#2. Calculate average annual income by customer segment.

select
    case
        when annual_income <= 1666666 then'Low'
        when  annual_income <= 3333333 then'Medium'
        else 'High'
    END as customer_segment,
    ROUND(avg(annual_income), 2) as avg_annual_income
from customers_cleaned
GROUP BY customer_segment
ORDER BY avg_annual_income DESC;

#3. Find the top 10 branches by total loan amount.

select
	b.branch_name,
	sum(loan_amount) as total_loan_amount 
from branches_cleaned as b
join loans_cleaned as l
   on b.branch_id=l.branch_id 
group by b.branch_name
order by total_loan_amount desc 
limit 10; 

#4. Find the top 10 customers by total loan amount.

select 
  c.customer_name ,
  sum(loan_amount) as total_loan_amount
  from loans_cleaned as l
join customers_cleaned as c 
 on c.customer_id = l.customer_id
group by c.customer_id,c.customer_name
order by total_loan_amount desc 
limit 10;

#5. Calculate total loans and total loan value by loan type.

select 
 loan_type,
 sum(loan_amount) as total_loan_value,
 count(*) as total_loans 
from loans_cleaned 
group by loan_type 
order by total_loan_value desc;