# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# STEP 1
df_boston = pd.read_sql("""
    SELECT e.firstName,
           e.lastName
    FROM employees e
    JOIN offices o
        ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston'
""", conn)

# STEP 2
df_zero_emp = pd.read_sql("""
    SELECT o.officeCode,
           o.city,
           o.country
    FROM offices o
    LEFT JOIN employees e
        ON o.officeCode = e.officeCode
    WHERE e.employeeNumber IS NULL
""", conn)
# STEP 3
df_employee = pd.read_sql("""
    SELECT e.firstName,
           e.lastName,
           o.city,
           o.state
    FROM employees e
    LEFT JOIN offices o
        ON e.officeCode = o.officeCode
    ORDER BY e.firstName, e.lastName
""", conn)
# STEP 4
df_contacts = pd.read_sql("""
    SELECT contactFirstName,
           contactLastName,
           phone,
           salesRepEmployeeNumber
    FROM customers
    WHERE customerNumber NOT IN (
        SELECT customerNumber
        FROM orders
    )
    ORDER BY contactLastName
""", conn)

# STEP 5
# STEP 5
df_payment = pd.read_sql("""
    SELECT c.contactFirstName,
           c.contactLastName,
           p.amount,
           p.paymentDate
    FROM customers c
    JOIN payments p
        ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC
""", conn)

# STEP 6
# STEP 6
df_credit = pd.read_sql("""
    SELECT e.employeeNumber,
           e.firstName,
           e.lastName,
           COUNT(c.customerNumber) AS numcustomers
    FROM employees e
    JOIN customers c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber, e.firstName, e.lastName
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY numcustomers DESC
""", conn)

# STEP 7
df_product_sold = pd.read_sql("""
    SELECT p.productName,
           COUNT(od.orderNumber) AS numorders,
           SUM(od.quantityOrdered) AS totalunits
    FROM products p
    JOIN orderdetails od
        ON p.productCode = od.productCode
    GROUP BY p.productCode, p.productName
    ORDER BY totalunits DESC
""", conn)

# STEP 8
df_total_customers = pd.read_sql("""
    SELECT p.productName,
           p.productCode,
           COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM products p
    JOIN orderdetails od
        ON p.productCode = od.productCode
    JOIN orders o
        ON od.orderNumber = o.orderNumber
    GROUP BY p.productCode, p.productName
    ORDER BY numpurchasers DESC
""", conn)

# STEP 9
# STEP 9
df_customers = pd.read_sql("""
    SELECT o.officeCode,
           o.city,
           COUNT(c.customerNumber) AS n_customers
    FROM offices o
    JOIN employees e
        ON o.officeCode = e.officeCode
    JOIN customers c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode, o.city
    ORDER BY o.officeCode
""", conn)

# STEP 10# STEP 10
df_under_20 = pd.read_sql("""
    WITH low_performing_products AS (
        SELECT od.productCode
        FROM orderdetails od
        JOIN orders o
            ON od.orderNumber = o.orderNumber
        GROUP BY od.productCode
        HAVING COUNT(DISTINCT o.customerNumber) < 20
    )
    SELECT DISTINCT
           e.employeeNumber,
           e.firstName,
           e.lastName,
           ofc.city,
           ofc.officeCode
    FROM employees e
    JOIN offices ofc
        ON e.officeCode = ofc.officeCode
    JOIN customers c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    JOIN orders o
        ON c.customerNumber = o.customerNumber
    JOIN orderdetails od
        ON o.orderNumber = od.orderNumber
    WHERE od.productCode IN (
        SELECT productCode
        FROM low_performing_products
    )
    ORDER BY e.employeeNumber
""", conn)