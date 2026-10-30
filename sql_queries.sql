-- 1. Динамика выручки (DAU по дням)
SELECT
    DATE(timestamp) AS event_date,
    COUNT(DISTINCT user_id) AS dau,
    COUNT(DISTINCT CASE WHEN event_type = 'add_to_cart' THEN user_id END) AS users_added_to_cart,
    COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_id END) AS users_purchased,
    SUM(CASE WHEN event_type = 'purchase' THEN amount ELSE 0 END) AS total_revenue
FROM raw_events
GROUP BY DATE(timestamp)
ORDER BY event_date;

-- 2. Топ-10 товаров по выручке
SELECT
    product_id,
    COUNT(*) AS times_purchased,
    SUM(amount) AS revenue
FROM raw_events
WHERE event_type = 'purchase' AND product_id != 'unknown'
GROUP BY product_id
ORDER BY revenue DESC
LIMIT 10;

-- 3. Топ-10 товаров по просмотрам
SELECT
    product_id,
    COUNT(*) AS view_count
FROM raw_events
WHERE event_type IN ('page_view', 'product_view') AND product_id != 'unknown'
GROUP BY product_id
ORDER BY view_count DESC
LIMIT 10;

-- 4. Результаты A/B теста
SELECT
    "group",
    COUNT(user_id) AS total_users,
    SUM(converted) AS total_purchases,
    ROUND(AVG(converted) * 100, 2) AS conversion_rate
FROM ab_test_results
GROUP BY "group";