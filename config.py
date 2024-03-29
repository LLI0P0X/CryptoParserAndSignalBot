import secret

BOT_TOKEN = secret.BOT_TOKEN  # '0000000000:************************************'
users = secret.users  # [0000000003, 0000000001]
sendTo = secret.sendTo  # [0000000003, 0000000001, 0000000009, 0000000004]
try:
    proxy = secret.proxy  # 'http://login:pass@ip:port' or ['http://login:pass@ip:port','http://login:pass@ip:port','http://login:pass@ip:port']
except:
    proxy = None
pathToBd = __file__[:-9]
timeout = 5