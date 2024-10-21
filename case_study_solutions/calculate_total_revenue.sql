SELECT 
    purchased_on,
    player_last_progress,
    SUM(net_revenue) AS revenue
FROM 
    Sales
WHERE 
    sale_status = 1 AND is_sandbox = 0 
GROUP BY
    purchased_on, 
    player_last_progress;