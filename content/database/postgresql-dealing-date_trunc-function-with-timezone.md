Title: [postgreqsql] 处理 date_trunc 函数的时区问题
Slug: postgresql-dealing-date_trunc-function-with-timezone
Tags: postgresql
Date: 2015-04-20

前几天使用 `date` 函数计算天数的时候遇到了时区问题。

默认情况下如果数据库里存的是 UTC 时间的话，计算的是 UTC 时间的 `day`。
由于我们需要的最终结果是北京时间，所以需要在计算 `day` 的时候指定时区：

    # before
    date_trunc('day', posted_at)
    # after
    date_trunc('day', posted_at::TIMESTAMPTZ AT TIME ZONE '+08:00'::INTERVAL)


## 参考资料

* http://www.postgresql.org/docs/9.4/static/functions-datetime.html
* http://brendankemp.com/essays/dealing-with-time-zones-using-rails-and-postgres/
