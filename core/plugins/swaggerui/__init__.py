#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   __init__.py
@Time    :   2025/03/04 12:01:48
@Desc    :   None
"""

from fastapi import FastAPI, Request
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

from ..pluginbase import IBasePlugin as BasePlugin


class SwaggeruiPluginClient(BasePlugin):
    """Swaggerui"""

    name = "本地的Swaggerui文档，避免在线访问"
    describe = "该插件启用后，会自动过滤之前路由设置，只保留下来/docs的路由访问"

    def __init__(self, app: FastAPI = None, name=None, proxy=False, **options):
        """插件初始化"""
        super().__init__(app, name, **options)
        self.proxy = proxy

    def setup(self, app: FastAPI, name: str = None, *args, **kwargs):
        """插件初始化"""
        # 启用插件后自动关闭之前的配置在线文档

        # 路由： Route(path='/openapi.json', name='openapi', methods=['GET', 'HEAD'])
        # 路由： Route(path='/docs', name='swagger_ui_html', methods=['GET', 'HEAD'])
        # 路由： Route(path='/docs/oauth2-redirect', name='swagger_ui_redirect', methods=['GET', 'HEAD'])
        # 路由： Route(path='/redoc', name='redoc_html', methods=['GET', 'HEAD'])

        # assert core_app.redoc_url is None and core_app.docs_url is None, '本地的Swaggerui文档插件，请先关闭APP原始的开关设置为None'
        # 过滤路由的方式，不用手动的关闭app.redoc_url is None and core_app.docs_url is None
        app.router.routes = [
            route
            for route in app.routes
            if route.path != "/docs" and route.path != "/redoc"
        ]
        # 需要先设置了关闭才可以自定义
        import pathlib

        cur_file_path = str(pathlib.Path(__file__).absolute()).replace(
            r"\__init__.py", ""
        )
        # cur_file_path='/data/www/woreid_right_pay/azyxfastcore/core_plugins/swaggerui/__init__.py/static'
        # 原始当前路径： /data/www/woreid_right_pay/azyxfastcore/core_plugins/swaggerui/__init__.py
        # 当前路径： /data/www/woreid_right_pay/azyxfastcore/core_plugins/swaggerui/__init__.py
        # 处理配置经过NGINX代理后的路径有所变化的问题
        if "/__init__.py/static" in cur_file_path:
            cur_file_path = cur_file_path.replace("/__init__.py/static", "")
        if "/__init__.py" in cur_file_path:
            cur_file_path = cur_file_path.replace("/__init__.py", "")

        # 挂载静态目录
        app.mount(
            "/static", StaticFiles(directory=f"{cur_file_path}/static"), name="static"
        )

        # 自定义需要在关闭的情况下才可以
        @app.get("/", include_in_schema=False)
        @app.get("/docs", include_in_schema=False)
        @app.get("/swagger/docs", include_in_schema=False)
        async def custom_swagger_ui_html(req: Request):
            root_path = req.scope.get("root_path", "").rstrip("/")
            openapi_url = root_path + req.app.openapi_url
            # INFO  2022-10-01 19:01:43.980 | azyxfastcore.core_plugins.swaggerui:custom_swagger_ui_html:77 |  - root_path：
            # INFO  2022-10-01 19:01:43.980 | azyxfastcore.core_plugins.swaggerui:custom_swagger_ui_html:78 |  - openapi_url：('/openapi.json',)
            # 如果是反向代理之后的话，就不需要设置--- swagger_js_url="/static/swagger-ui-bundle.js",并且返回代理那需要配置为：
            # 	location /openapi.json {
            # 		proxy_pass http://woreid_right_pay_online_api_up/openapi.json;
            # 	}
            #
            # 	location /swagger-ui-bundle.js {
            # 		proxy_pass http://woreid_right_pay_online_api_up/static/swagger-ui-bundle.js;
            # 	}
            #
            # 	location /swagger-ui.css {
            # 		proxy_pass http://woreid_right_pay_online_api_up/static/swagger-ui.css;
            # 	}
            if self.proxy:
                swagger_js_url = "/swagger-ui-bundle.js"
                swagger_css_url = "/swagger-ui.css"
            else:
                pass
                swagger_js_url = "/static/swagger-ui-bundle.js"
                swagger_css_url = "/static/swagger-ui.css"

            return get_swagger_ui_html(
                openapi_url=openapi_url,
                title=app.title + " - Swagger UI",
                oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
                swagger_js_url=swagger_js_url,
                init_oauth=app.swagger_ui_init_oauth,
                swagger_ui_parameters=app.swagger_ui_parameters,
                swagger_css_url=swagger_css_url,
                # swagger_js_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js",
                # swagger_css_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css",
                # swagger_favicon_url: str = "https://fastapi.tiangolo.com/img/favicon.png",
            )

        @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
        async def swagger_ui_redirect():
            return get_swagger_ui_oauth2_redirect_html()

        @app.get("/redoc", include_in_schema=False)
        async def redoc_html():
            return get_redoc_html(
                openapi_url=app.openapi_url,
                title=app.title + " - ReDoc",
                redoc_js_url="/static/redoc.standalone.js",
            )
