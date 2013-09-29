Title: [MySQL]修复 DatabaseError: (1061, "Duplicate key name 'bar_xxx_uniq'") 错误
Date: 2013-09-10
Tags: mysql
Slug: mysql-DatabaseError-1061-Duplicate-key-name

当 MySQL 数据库的索引 key 出现重复时，就会提示类似的错误：

> DatabaseError: (1061, "Duplicate key name 'abc\_xxx\_uniq'")

解决办法是移除重复的索引 key:

    ALTER TABLE `foo`.`bar` DROP INDEX `bar_xxx_uniq`;
