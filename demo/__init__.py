class BaseApp:
    """
    定义一个 callable 的父类，提供默认的 application 的功能
    """

    def __call__(self, environ, start_response):
        response_body = []
        for k in environ:
            response_body.append(("%s = %s \n" % (k, environ[k])).encode())
        status = '200 OK'
        response_headers = [('Content-Type', 'text/plain')]
        start_response(status, response_headers)
        return response_body
