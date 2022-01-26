import uuid

import sqlalchemy

# CREATE DATABASE
engine = sqlalchemy.create_engine("mysql://root:123@localhost")
engine.execute("DROP DATABASE IF EXISTS shop")
engine.execute("CREATE DATABASE shop")
engine.execute("USE shop")

# CREATE PRODUCTS
engine.execute("create table product("
               "id varchar(255) primary key, "
               "name varchar(255) not null,"
               "stock int not null default 0) "
               "engine=InnoDB default charset=utf8mb4;")
engine.execute("insert into product values("
               f"'{uuid.uuid4()}',"
               "'PRODUTO A',"
               "5)")
engine.execute("insert into product values("
               f"'{uuid.uuid4()}',"
               "'PRODUTO B',"
               "1)")
engine.execute("insert into product values("
               f"'{uuid.uuid4()}',"
               "'PRODUTO C',"
               "4)")
engine.execute("insert into product values("
               f"'{uuid.uuid4()}',"
               "'PRODUTO D',"
               "2)")
engine.execute("insert into product values("
               f"'{uuid.uuid4()}',"
               "'PRODUTO E',"
               "3)")
engine.execute("insert into product values("
               f"'{uuid.uuid4()}',"
               "'PRODUTO F',"
               "1)")
engine.execute("insert into product values("
               f"'{uuid.uuid4()}',"
               "'PRODUTO G',"
               "5)")

# CREATE SHOPPING_CART
engine.execute("create table shopping_cart("
               "id varchar(255) primary key)"
               "engine=InnoDB default charset=utf8mb4;")

engine.execute("create table products_in_shopping_cart("
               "id bigint primary key auto_increment, "
               "quantity int not null, "
               "product_id varchar(255) not null, "
               "shopping_cart_id varchar(255) not null, "
               "constraint fk_product_shopping_cart_product foreign key (product_id) references product (id), "
               "constraint fk_product_shopping_cart_cart foreign key (shopping_cart_id) references shopping_cart (id))"
               " engine=InnoDB default charset=utf8mb4;")
