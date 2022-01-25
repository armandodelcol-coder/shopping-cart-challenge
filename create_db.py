import uuid

import sqlalchemy


engine = sqlalchemy.create_engine("mysql://root:123@localhost")
engine.execute("DROP DATABASE IF EXISTS shop")
engine.execute("CREATE DATABASE shop")
engine.execute("USE shop")
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
