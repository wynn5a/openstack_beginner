import http.client
import json

from webob import Response
from webob.dec import wsgify


class Controller(object):
    """
    具体处理请求的 controller 类，里面的方法可以分别对应着不同的 url
    """

    def __init__(self):
        self.version = "1.0.0"

    def index(self, req):
        """
        具体处理请求的方法
        :param req:
        :return:
        """

        # 利用 webob 的封装，方便的创建 response
        response = Response(request=req,
                            status=http.HTTPStatus.MULTIPLE_CHOICES,
                            content_type='application/json')
        response.text = json.dumps(dict(versions=self.version))
        return response

    @wsgify  # 利用 webob 注解封装简化参数
    def __call__(self, request):
        return self.index(request)


def create_resource():
    """
    这里相当于 controller 的 factory，能够生产不同的 controller
    :return: controller instance
    """
    return Controller()
