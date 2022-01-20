class SQLQueries:
    create_table_queries = ("""

    -- create staging (temporary) tables
    -- no need for orders.csv bc the same
    CREATE TABLE IF NOT EXISTS temp_products (
        product_id          INT PRIMARY KEY,
        product_id          INT,
        aisle_id            INT,
        department_id       INT
    )

    CREATE TABLE IF NOT EXISTS temp_dept (
        department_id       INT PRIMARY KEY,
        department          VARCHAR(100) NOT NULL
    )

    CREATE TABLE IF NOT EXISTS temp_aisles (
        aisle_id    INT PRIMARY KEY,
        aisle       VARCHAR(100)
    )

    --------- create dimension tables

    -- close to products.csv, but add name as well
    CREATE TABLE IF NOT EXISTS dim_goods (
        product_id      INT PRIMARY KEY,
        product         VARCHAR(200) NOT NULL,
        aisle_id        INT,
        aisle           VARCHAR(100) NOT NULL,
        department_id   INT,
        department      VARCHAR(100) NOT NULL
    )

    -- same as orders.csv
    CREATE TABLE IF NOT EXISTS dim_orders (
        order_id                    INT PRIMARY KEY,
        user_id                     INT,
        eval_set                    VARCHAR(10),
        order_number                INT,
        order_dow                   INT,
        order_hour_of_day           INT,
        days_since_prior_order      DOUBLE
    )

    -- holds contents of past orders for all customers
    CREATE TABLE IF NOT EXISTS dim_order_products_prior (
        order_id                INT PRIMARY KEY,
        product_id              INT,
        add_to_cart_order       INT,
        reordered               BIT
    )
    
    -- holds contents of recent orders for a subset of customers
    CREATE TABLE IF NOT EXISTS dim_order_products_train (
        order_id                INT PRIMARY KEY,
        product_id              INT,
        add_to_cart_order       INT,
        reordered               BIT
    )

    CREATE TABLE IF NOT EXISTS dim_reorder (
        product_id          INT PRIMARY KEY,
        reorder_sum         INT,
        reorder_total       INT,
        reorder_probability INT,
        product_name        VARCHAR(100) NOT NULL
    )

    -- create fact table
    CREATE TABLE IF NOT EXISTS fact_orders (
        order_id                    INT,
        product_id                  INT,
        aisle_id                    INT,
        department_id               INT,
        id                          PRIMARY KEY (order_id, product_id, aisle_id, department_id),
    )    
    """)

    goods_table_insert = ("""
        INSERT INTO dim_goods (product_id, aisle_id, department_id)
        SELECT * FROM (
            SELECT DISTINCT COALESCE
            FROM temp_
        )
    """)

    fact_table_insert = ("""
        INSERT INTO fact_table (
            order_id,
            product_id,
            aisle_id,
            department_id,
        ) SELECT
            o.id,
            p.id,
            a.id,
            d.id,
          FROM 


    """)