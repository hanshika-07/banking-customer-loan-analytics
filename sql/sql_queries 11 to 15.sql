#11. Find branches with above-average loan disbursement.

select
    branch_id,
    SUM(loan_amount) as total_loan_amount
from loans_cleaned
group by branch_id
having ROUND(SUM(loan_amount),2) > (
    select avg(branch_total)
    from (
        select
            branch_id,
            ROUND(SUM(loan_amount),2) AS branch_total
        from loans_cleaned
        group by branch_id
    ) as branch_totals
)
order by total_loan_amount DESC;

#12. Calculate average transaction amount by transaction type.

select 	
	transaction_type,
    ROUND(avg(amount),2) as avg_transaction
	from transactions_cleaned
group by transaction_type;

#13. Find the top 10 customers by transaction volume.

select
	c.customer_id,
    count(t.transaction_id) as transaction_volume,
    ROUND(sum(t.amount),2) as transaction_value 
from customers_cleaned as c 
join accounts_cleaned as a 
  on c.customer_id=a.customer_id 
join transactions_cleaned as t 
  on t.account_id=a.account_id
group by c.customer_id
order by transaction_volume desc
limit 10;

#14. Calculate monthly transaction value.

select 
	extract(month from transaction_date) as month ,
    ROUND(SUM(amount),2) as transaction_value
from transactions_cleaned
group by extract(month from transaction_date)
order by month;

#15. Find customers with no transactions in the most recent period.

select 
	c.customer_id,
    c.customer_name 
from customers_cleaned as c 
join accounts_cleaned as a 
on c.customer_id=a.customer_id
left join transactions_cleaned as t
on a.account_id=t.account_id 
AND date_format("t.transaction_date","%Y-%M") =(
 select 
	MAX(date_format("t.transaction_date","%Y-%M")) 
from transactions_cleaned
)
where t.transaction_id is null;
