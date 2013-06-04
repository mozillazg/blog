Title: [django]解决发送密码重置邮件的发件人是 "webmaster@localhost" 的问题
Date: 2013-06-04
Tags: django, python, send_mail
Slug: django-fix-reset-password-use-webmaster@localhost-send-mail

默认情况下，django 将通过 webmaster@localhost 发送密码重置邮件。

这明显不是我们想要的，更改 settings.py 文件即可修复这个问题。

增加一个配置项 DEFAULT_FROM_EMAIL：

    :::python
    DEFAULT_FROM_EMAIL = 'foo@bar.com'

此时的发件人将会是：foo@bar.com


## 参考

* [Re: [Django] #13847: PasswordResetForm sends emails using "webmaster@localhost" - Django - com.googlegroups.django-updates - MarkMail](http://markmail.org/thread/yiomiws5gvyxvfia#query:+page:1+mid:sb6fpukeijedzxzg+state:results)
