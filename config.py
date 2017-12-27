
DEBUG = True
ALLOWED_HOSTS = ['*']

SERVER_NAME = 'anything'
DOMAIN_NAME = '{0}.xxx.xxx'.format(SERVER_NAME)

LOG_NAME = SERVER_NAME
LOG_PATH = '/data/log/django/{0}.log'.format(SERVER_NAME)
LOG_MAX_BYTES = 5 * 1024 * 1024  # 5M
LOG_BACKUP_COUNT = 90
LOG_LEV = 'DEBUG'

# 微信配置
AppID = ''
AppSecret = ''
EncodingAESKey = ''
Token = ''
