class SQLQueries:
    create_table_queries = ("""
    
    -- create dimension tables

    CREATE TABLE IF NOT EXISTS dim_aisles (
        aisle_id        INT PRIMARY KEY,
        aisle           VARCHAR(100) NOT NULL
    )

    CREATE TABLE IF NOT EXISTS dim_departments (
        department_id       INT PRIMARY KEY,
        department          VARCHAR(100) NOT NULL
    )

    CREATE TABLE IF NOT EXISTS dim_orders (
        order_id                    INT PRIMARY KEY,
        user_id                     INT,
        eval_set                    VARCHAR(10),
        order_number                INT,
        order_dow                   INT,
        order_hour_of_day           INT,
        days_since_prior_order      DOUBLE
    )

    CREATE TABLE IF NOT EXISTS dim_order_products_prior (
        order_id                INT PRIMARY KEY,
        product_id              INT,
        add_to_cart_order       INT,
        reordered               BIT
    )

    CREATE TABLE IF NOT EXISTS dim_order_products_train (
        order_id                INT PRIMARY KEY,
        product_id              INT,
        add_to_cart_order       INT,
        reordered               BIT
    )

    CREATE TABLE IF NOT EXISTS dim_products (
        product_id          INT PRIMARY KEY,
        name                VARCHAR(100) NOT NULL,
        aisle_id            INT,
        department_id       INT,
    )

    CREATE TABLE IF NOT EXISTS dim_submissions (
        order_id            INT,
        product_id          INT
    )

    -- create fact table
    CREATE TABLE IF NOT EXISTS fact_table (
        id                          INT PRIMARY KEY,

        -- dimension table ids
        aisle_id                    INT,
        department_id               INT,
        order_id                    INT,
        product_id                  INT,

        -- aisles
        aisle

        -- departments
        department

        -- orders
        user_id
        eval_set
        order_number
        order_dow
        order_hour_of_day
        days_since_prior_order

        -- products
        product_name
    )    
    """)

    fact_table_insert = ("""
        INSERT INTO fact_table (
            aisle_id,                    
            department_id,               
            order_id,                    
            product_id,                 
            aisle,
            department,
            user_id,
            eval_set,
            order_number,
            order_dow,
            order_hour_of_day,
            days_since_prior_order,
            product_name 
        ) SELECT


    """)