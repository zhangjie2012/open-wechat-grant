
import config
import redis

# Redis Key -> 保持精简
k_component_verify_ticket = '{0}{1:03d}'.format(config.SERVER_NAME, 1)
k_component_access_token = '{0}{1:03d}'.format(config.SERVER_NAME, 2)
k_pre_auth_code = '{0}{1:03d}'.format(config.SERVER_NAME, 3)


class GlobalStore(object):

    def __init__(self, host, port=6379, password=None):
        self.rds = redis.StrictRedis(
            host=host,
            port=port,
            password=password,
            decode_responses=True  # 避免每次都做 decode
        )

    # component_verify_ticket
    def set_component_verify_ticket(self, ticket):
        self.rds.set(k_component_verify_ticket, ticket)

    def get_component_verify_ticket(self):
        self.rds.get(k_component_verify_ticket)

    # 第三方平台令牌
    def set_component_access_token(self, token, ex):
        self.rds.set(k_component_access_token, token, ex)

    def get_component_access_token(self):
        return self.rds.get(k_component_access_token)

    def ttl_component_access_token(self):
        return self.rds.ttl(k_component_access_token)

    # 预授权码
    def set_pre_auth_code(self, code, ex):
        self.rds.set(k_pre_auth_code, code, ex)

    def get_pre_auth_code(self):
        return self.rds.get(k_pre_auth_code)

    def delete_pre_auth_code(self):
        self.rds.delete(k_pre_auth_code)


global_store = GlobalStore('localhost')
