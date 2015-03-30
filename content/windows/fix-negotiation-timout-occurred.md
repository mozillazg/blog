Title: [windows]修复 ShrewSoft VPN 客户端连接时出现 negotiation timout occurred 错误
Date: 2015-03-29
Slug: fix-shrewsoft-vpn-client-connect-error-negotiation-timout-occurred


错误信息如下:

    client configured
    local id configured
    remote id configured
    pre-shared key configured
    bringing up tunnel ...
    negotiation timout occurred   <---- here
    tunnel disabled
    detached from key daemon
    attached to key daemon ...


解决办法：使用管理员身份运行 cmd ，输入 `netsh wlan set hostednetwork mode=disallow`

    C:\WINDOWS\system32>netsh wlan set hostednetwork mode=disallow
    The hosted network mode has been set to disallow.
