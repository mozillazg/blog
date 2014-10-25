Title: [linux]解决 sendmail 错误： FEATURE() should be before MAILER()
Date: 2013-02-22
Tags: linux, ubuntu, sendmail
Slug: linux-fix-sendmail-configuration-error-feature-should-be-before-mailer


错误详情：

    :::console
    # m4 /etc/mail/sendmail.mc > /etc/mail/sendmail.cf
    *** ERROR: FEATURE() should be before MAILER()
    *** MAILER(`local') must appear after FEATURE(`always_add_domain')*** ERROR: FEATURE() should be before MAILER()
    *** MAILER(`local') must appear after FEATURE(`allmasquerade')*** ERROR: FEATURE() should be before MAILER()

解决办法：

按照提示，编辑 /etc/mail/sendmail.mc 文件，将 FEATURE() 放到 MAILER() 之前：

更改

    :::text
    dnl #
    dnl # Default Mailer setup
    MAILER_DEFINITIONS
    MAILER(`local')dnl
    MAILER(`smtp')dnl

    dnl # Masquerading options
    FEATURE(`always_add_domain')dnl
    MASQUERADE_AS(`tumblr.3sd.me')dnl
    FEATURE(`allmasquerade')dnl
    FEATURE(`masquerade_envelope')dnl

为

    :::text
    dnl #

    dnl # Masquerading options
    FEATURE(`always_add_domain')dnl
    MASQUERADE_AS(`tumblr.3sd.me')dnl
    FEATURE(`allmasquerade')dnl
    FEATURE(`masquerade_envelope')dnl

    dnl # Default Mailer setup
    MAILER_DEFINITIONS
    MAILER(`local')dnl
    MAILER(`smtp')dnl

