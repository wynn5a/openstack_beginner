import routes.middleware
import webob.exc
from demo import versions
from webob.dec import wsgify


class Router(object):
    """
    定义了一个 Router 的 application，来完成剩余 url 到 controller 的映射
    """

    def __init__(self, mapper=None):
        mapper.redirect("", "/")  # 处理极端情况
        self._mapper = mapper
        # 利用 routes 的中间件功能，做一系列封装和处理，最后得到具体 url 和 controller 的对应关系
        self._router = routes.middleware.RoutesMiddleware(self._dispatch, self._mapper)

    @classmethod
    def factory(cls, global_conf, **local_conf):
        # cls 指的是调用这个方法的 class
        # 定义一个 WSGI application 工厂类，来处理请求
        return cls()  # 使用 Router 或者其子类的实例来处理请求

    @wsgify
    def __call__(self, req):
        # 处理发到自己或者子类的请求
        return self._router  # 调用 routes 中间件处理好的 router 实例

    @staticmethod
    @wsgify
    def _dispatch(req):
        # _router 的 __call__ 方法会调用这里，所以这里才是真正处理请求的地方
        # 这里我们可以从 environ 里面拿到 controller 和 处理请求的 action，那么就可以通过反射来执行对应的 action
        match = req.environ['wsgiorg.routing_args'][1]

        # url 没有对应的 mapping 关系
        if not match:
            return webob.exc.HTTPNotFound()

        # 拿到对应的 controller
        app = match['controller']
        return app  # 简单化处理，直接调用 controller 的 __call__ 方法来处理请求


class API(Router):
    """
    定义了一个可以处理请求的 WSGI application

    请求到达时，会执行 __call__ 方法
    """

    def __init__(self, mapper=None):
        if mapper is None:
            mapper = routes.Mapper()

        # 拿到 controller
        versions_resource = versions.create_resource()
        # 建立 url 和 controller 以及对应的处理方法之间的 mapping 关系
        mapper.connect("/", controller=versions_resource, action='index', conditions={'method': ['GET']})
        # 调用父类来处理这个 mapper
        super(API, self).__init__(mapper)
