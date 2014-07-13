Title: [linux] 修复 Redmine 无法发送通知邮件，提示 550 5.7.1 Unable to relay 的问题
Date: 2014-06-09
Tags: linux, redmine
Slug: linux-fix-redmine-send-mail-error-550-5.7.1-Unable-to-relay


前两天接手了公司 Redmine 系统的维护工作，需要写一个安装维护文档。
所以我就在本地虚拟机上尝试进行了一下安装。
安装后，测试使用的过程中遇到了无法发送通知邮件的问题， 日志信息如下：

    The following error occured while sending email notification:
    "550 5.7.1 Unable to relay".
    Check your configuration in config/configuration.yml.

Redmine 版本： 1.2.1

最终的解决办法是，修改 config/configuration.yml ，添加 `authentication: :none` :

    default:
      # Outgoing emails configuration (see examples above)
      email_delivery:
        delivery_method: :smtp
        smtp_settings:
          address: domain.com
          port: 25
          domain: domain.com
          authentication: :none    # 修改项
          # authentication: :login
          # user_name: "redmine@example.net"
          # password: "redmine"


## 参考资料

* [Test e-mail works but notifications aren't send - Redmine](http://www.redmine.org/boards/2/topics/19732)
* [Notification Emails not sent, but test emails do work - Bitnami Community](http://community.bitnami.com/t/notification-emails-not-sent-but-test-emails-do-work/2186/2)
* [Redmine 2.0: error sending email](http://www.redmine.org/boards/2/topics/30851)