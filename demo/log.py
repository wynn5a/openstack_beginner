from webob.dec import wsgify
from webob.request import Request


def log_auth_factory(global_conf, **local_conf):
    """
    简单的 filter factory- 记录请求基本信息，并且校验用户名密码
    """

    def log_auth(app):
        # 绑定了一个具体的 filter
        return LogFilter(app, global_conf, local_conf)

    return log_auth


def log_unauth_factory(global_conf, **local_conf):
    """
    简单的 filter factory - 记录请求基本信息
    """
    return log_unauth


@wsgify.middleware  # webob 的注解，能够简化参数
def log_unauth(req, app):
    print("log_unauth is called")
    print("%s is trying to access %s" % (req.GET.get("username", ""), req.url))
    # 没有鉴定过程，直接调用 app 来处理请求
    return app(req)


class LogFilter:
    """
    定义了一个具体的 filter 中间件，使用的是默认的形式。
    """

    def __init__(self, app, global_conf, local_conf):
        self.app = app
        self.global_conf = global_conf
        self.local_conf = local_conf

    def __call__(self, environ, start_response):
        """
        定义了 filter 的 call 方法，用来响应请求

        :param environ:
        :param start_response:
        :return:
        """
        print("LogFilter is called")
        # webob 对 environ 参数进行简单的封装
        req = Request(environ)
        username = req.GET.get("username", "")
        print("%s is trying to access %s" % (username, req.url))

        # 鉴定用户名和密码
        if self.local_conf['username'] in username and req.GET.get("password", "") == \
                self.local_conf['password']:
            # 鉴定通过，调用 app 来处理请求
            return self.app(environ, start_response)

        # 鉴定失败，直接处理请求
        start_response("401 Unauthorized", [("Content-type", "text/plain")])
        return [b"You are not authorized"]
