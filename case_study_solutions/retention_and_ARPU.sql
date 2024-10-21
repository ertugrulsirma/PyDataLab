SELECT
    p.registered_on AS install_date,
    p.platform,
    p.country_code,
    COUNT(DISTINCT CASE WHEN s.occurred_on = DATE_ADD(p.registered_on, INTERVAL 1 DAY) THEN s.player_id END) * 100.0 / COUNT(DISTINCT p.id)
        AS retention_rate_day1,
    COUNT(DISTINCT CASE WHEN s.occurred_on = DATE_ADD(p.registered_on, INTERVAL 3 DAY) THEN s.player_id END) * 100.0 / COUNT(DISTINCT p.id)
        AS retention_rate_day3,
    COUNT(DISTINCT CASE WHEN s.occurred_on = DATE_ADD(p.registered_on, INTERVAL 7 DAY) THEN s.player_id END) * 100.0 / COUNT(DISTINCT p.id)
        AS retention_rate_day7,
    SUM(CASE WHEN sa.purchased_on = DATE_ADD(p.registered_on, INTERVAL 1 DAY) THEN sa.net_revenue ELSE 0 END) / COUNT(DISTINCT p.id)
        AS arpu_day1,
    SUM(CASE WHEN sa.purchased_on = DATE_ADD(p.registered_on, INTERVAL 3 DAY) THEN sa.net_revenue ELSE 0 END) / COUNT(DISTINCT p.id)
        AS arpu_day3,
    SUM(CASE WHEN sa.purchased_on = DATE_ADD(p.registered_on, INTERVAL 7 DAY) THEN sa.net_revenue ELSE 0 END) / COUNT(DISTINCT p.id)
        AS arpu_day7
FROM
    Players p
LEFT JOIN
    Sessions s ON p.id = s.player_id
LEFT JOIN
    Sales sa ON p.id = sa.player_id
WHERE
    p.game_id = 627
    AND p.registered_on BETWEEN '2023-11-01' AND '2023-11-30'
GROUP BY
    p.registered_on,
    p.platform,
    p.country_code;
