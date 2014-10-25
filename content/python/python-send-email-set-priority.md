Title: [python] 发送邮件时设置邮件的优先级/重要性
Date: 2013-07-02
Tags: python, email, X-Priority
Slug: python-send-email-set-priority

[TOC]

设置邮件 header 中 X-Priority 的值就可以了：

|  X-Priority 的值  |          含义           |
|-------------------|------------------------ |
|       "1"         | 最高级别（重要性高）    |
|       "2"         | 介于中间                |
|       "3"         | 普通级别（不提示重要性）|
|       "4"         | 介于中间                |
|       "5"         | 最低级别（重要性低）    |

## python 使用示例

> <http://stackoverflow.com/a/11844141>
>
>     :::python
>     import smtplib
>     from email.Message import Message
> 
>     smtp = smtplib.SMTP('localhost')
>     m = Message()
>     m['From'] = 'me'
>     m['To'] = 'you'
>     m['X-Priority'] = '2'
>     m['Subject'] = 'Urgent!'
>     m.set_payload('Nothing.')
>     smtp.sendmail(from_addr, to_addr, m.as_string())

## django 使用示例

    :::python
    from django.core.mail import EmailMessage

    subject = 'hello'
    msg = 'hello'
    headers = {'X-Priority': '1'}  # 注意值是字符串
    email = EmailMessage(subject, msg, from_email, to_emails,
                         headers=headers)
    email.send()



## 参考

* [python - SMTP sending an priority email - Stack Overflow](http://stackoverflow.com/questions/11843148/smtp-sending-an-priority-email)
* [X-Priority Header Field](http://www.chilkatsoft.com/braindump/email_headers/X-Priority_header.html)
