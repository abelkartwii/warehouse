class SQLQueries:
    # creates tables for everything: temporary, fact, dimension
    # used with CreateTableOperator
    create_table_queries = ("""

    -- create staging (temporary) tables
    -- no need for orders.csv bc the same
    CREATE TABLE IF NOT EXISTS temp_products (
        product_id          INT PRIMARY KEY,
        product_name        VARCHAR(200) NOT NULL,
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

    -- holds contents of past orders for all customers
    CREATE TABLE IF NOT EXISTS temp_prior (
        order_id                INT PRIMARY KEY,
        product_id              INT,
        add_to_cart_order       INT,
        reordered               BIT
    )
    
    -- holds contents of recent orders for a subset of customers
    CREATE TABLE IF NOT EXISTS temp_train (
        order_id                INT PRIMARY KEY,
        product_id              INT,
        add_to_cart_order       INT,
        reordered               BIT
    )

    --------- create dimension tables

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

    -- close to products.csv, but add name as well
    CREATE TABLE IF NOT EXISTS dim_goods (
        product_id      INT PRIMARY KEY,
        product         VARCHAR(200) NOT NULL,
        aisle_id        INT,
        aisle           VARCHAR(100) NOT NULL,
        department_id   INT,
        department      VARCHAR(100) NOT NULL
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
        INSERT INTO dim_goods (product_id, product_name, aisle_id, aisle, department_id, department)
        SELECT product_id, product_name, aisle_id, a.aisle, department_id, d.department
        FROM temp_products p
        INNER JOIN temp_aisles a ON a.aisle_id = p.aisle_id
        INNER JOIN temp_dept d ON d.department_id = p.department_id
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
          FROM dim_orders AS o
          LEFT JOIN temp_prior AS prior
            ON o.order_id = prior.order_id
          LEFT JOIN temp_train AS train
            ON o.order_id = train.order_id
          LEFT JOIN temp_products AS p
            ON o.product_id = p.product_id

    """)