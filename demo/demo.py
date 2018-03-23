from demo import BaseApp
from webob.request import Request


def app_factory(global_config, **local_config):
    """
    定义一个 app 的 factory 方法，以便在运行时绑定具体的 app，而不是在配置文件中就绑定。

    :param global_config:
    :param local_config:
    :return:
    """
    return MyApp()


class MyApp(BaseApp):
    """
    定义了一个 Application，并重写了父类的 callable 方法，用来处理请求

    这里采用的是 Paste deployment 实现的形式，必须包含 WSGI 规范中的两个参数 environ 和 start_response
    """

    def __call__(self, environ, start_response):
        req = Request(environ)
        response_body = [("Hello, %s" % req.GET.get("username")).encode()]
        status = '200 OK'
        response_headers = [('Content-Type', 'text/plain')]
        start_response(status, response_headers)
        return response_body
