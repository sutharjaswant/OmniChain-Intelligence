
-- OmniChain Intelligence
-- SQL business analysis queries
-- Data source: synthetic project dataset

-- 1. Overall order and revenue summary
SELECT
    COUNT(*) AS total_orders,
    SUM(CASE WHEN Status = 'Delivered' THEN 1 ELSE 0 END)
        AS delivered_orders,
    SUM(CASE WHEN Status = 'Returned' THEN 1 ELSE 0 END)
        AS returned_orders,
    SUM(CASE WHEN Status = 'Cancelled' THEN 1 ELSE 0 END)
        AS cancelled_orders,
    ROUND(SUM(NetRevenue), 2) AS total_net_revenue,
    ROUND(SUM(GrossProfit), 2) AS total_gross_profit
FROM orders;

-- 2. Monthly revenue and profit trends
SELECT
    strftime('%Y-%m', OrderDate) AS order_month,
    ROUND(SUM(NetRevenue), 2) AS monthly_revenue,
    ROUND(SUM(GrossProfit), 2) AS monthly_profit,
    COUNT(*) AS order_count
FROM orders
WHERE Status = 'Delivered'
GROUP BY strftime('%Y-%m', OrderDate)
ORDER BY order_month;

-- 3. Category-level performance
SELECT
    p.Category,
    COUNT(*) AS order_line_count,
    ROUND(SUM(o.NetRevenue), 2) AS revenue,
    ROUND(SUM(o.GrossProfit), 2) AS profit
FROM orders AS o
JOIN products AS p
    ON o.ProductID = p.ProductID
WHERE o.Status = 'Delivered'
GROUP BY p.Category
ORDER BY profit DESC;

-- 4. Top 10 products by profit
SELECT
    p.ProductID,
    p.ProductName,
    p.Category,
    ROUND(SUM(o.NetRevenue), 2) AS revenue,
    ROUND(SUM(o.GrossProfit), 2) AS profit
FROM orders AS o
JOIN products AS p
    ON o.ProductID = p.ProductID
WHERE o.Status = 'Delivered'
GROUP BY p.ProductID, p.ProductName, p.Category
ORDER BY profit DESC
LIMIT 10;

-- 5. Inventory items at or below reorder point
SELECT
    i.ProductID,
    p.ProductName,
    i.StockOnHand,
    i.ReorderPoint,
    i.DailyDemandEstimate,
    i.StockStatus
FROM inventory AS i
JOIN products AS p
    ON i.ProductID = p.ProductID
WHERE i.StockOnHand <= i.ReorderPoint
ORDER BY i.StockOnHand ASC;

-- 6. Supplier delivery performance
SELECT
    s.SupplierID,
    s.SupplierName,
    COUNT(d.SupplierID) AS total_deliveries,
    ROUND(100.0 * AVG(
        CASE WHEN d.OnTime = 1 THEN 1.0 ELSE 0.0 END
    ), 2) AS on_time_delivery_percentage,
    ROUND(AVG(d.ActualLeadTimeDays), 2) AS average_lead_time_days
FROM suppliers AS s
LEFT JOIN supplier_deliveries AS d
    ON s.SupplierID = d.SupplierID
GROUP BY s.SupplierID, s.SupplierName
ORDER BY on_time_delivery_percentage DESC;
