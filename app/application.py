#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   main.py
@Time    :   2025/03/04 10:33:55
@Desc    :   项目主入口
"""

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.app import IApplicationBuilder
from core.plugins.globalrequest.request import GlobalRequestPluginClient
from core.plugins.loguru.client import LoguruPluginClient
from core.plugins.swaggerui import SwaggeruiPluginClient
from core.tools.router import load_controller_modules

from .settings.development import DevSettings
from .settings.production import ProSettings
from .settings.setting import Environment


class FastApplicationBuilder(IApplicationBuilder):
    """创建应用"""

    def __init__(self, *, settings: DevSettings | ProSettings):
        """创建APP实例对象"""
        if settings is None:
            # 检测是否存在配置实例对象
            raise RuntimeError("Must provide a valid Settings object")
        self.settings = settings

    @classmethod
    def with_environment_settings(cls) -> "FastApplicationBuilder":
        """根据当前环境变量选择指定的环境配置实例"""
        return cls(settings=Environment.select())

    def _instance_app(self) -> FastAPI:
        # logger.info(f"{self.settings}")
        # 创建实例对象
        return FastAPI(
            title=self.settings.project_name,
            version=self.settings.project_version,
            debug=self.settings.debug,
        )

    def _register_loguru_log_client(self, app: FastAPI) -> None:
        # 放在在最后处理因为是日志作用，所以一般使用的时候最后再执行注册
        pass
        # 日志插件初始化
        LoguruPluginClient(
            app=app,
            name="Loguru",
            settings=LoguruPluginClient.LoguruConfig(
                PROJECT_SLUG=self.settings.LOG_PROJECT_SLUG,
                FLITER_REQUEST_URL=self.settings.FLITER_REQUEST_URL,
                LOG_FILE_PATH=self.settings.LOG_FILE_PATH,
                MODEL=self.settings.LOG_MODEL,
            ),
        )

    def _register_global_request(self, app: FastAPI) -> None:
        # 注册应用全局请求的request
        pass
        GlobalRequestPluginClient(app=app, name="GlobalRequest")

    def _register_plugins(self, app: FastAPI) -> None:
        # 应用注册注册插件
        pass
        # 离线本地文档浏览
        SwaggeruiPluginClient(
            app=app,
            name="Swaggerui",
            proxy=self.settings.swaggerui_proxy,
        )

        # # 异步缓存插件
        # AsyncCashewsPluginClient(app=app, settings=AsyncCashewsPluginClient.CacheSettings(
        #     url='redis://root:123456@127.0.0.1:6379/?db=1&socket_connect_timeout=0.5&safe=0'
        # ))
        # 另一个后台任务的插件
        # AiojobsPluginClient(app=app)
        # 类似信号事件分发插件
        # EventEmitterPluginClient(app=app, settings=EventEmitterPluginClient.EventsSettings(
        #     events_name='events'
        # ))

        # 性能检测数据，打印出相关调用链路的耗时处理
        # ProfilePluginClient(core_app=core_app, configs=ProfilePluginClient.ProfileConfig())
        # # 定时任务===需注意避免本地多worker情况启动多个可以加文件锁或其他锁
        # schedule = RocketrySchedulerPluginClient(core_app=core_app, configs=RocketrySchedulerPluginClient.SchedulerConfig())
        # @schedule.infirmary_tasks('every 5 seconds')
        # async def do_things():
        #     print("定时任务！")
        #
        # @schedule.infirmary_tasks(every('10 seconds', based="finish"))
        # async def do_permanently():
        #     "This runs for really long time"
        #     print(600000)
        #     await asyncio.sleep(600000)
        #
        # @schedule.infirmary_tasks(every('2 seconds', based="finish"))
        # async def do_short():
        #     "This runs for short time"
        #     print(11111)
        #     await asyncio.sleep(1)

    def _register_exception_handlers(self, app: FastAPI) -> None:
        # 应用注册自定义的错误处理机制
        pass

        # 注册某个插件下特定的异常抛出处理
        # from infirmary_admin_src.infirmary_common.infirmary_errors.globalexption import (
        #     setup_snowy_ext_exception,
        # )

        # setup_snowy_ext_exception(app=app)

    def _register_routes(self, app: FastAPI) -> None:
        app_router = APIRouter(prefix="/api/v1")
        # 加入模块路由组
        # from fastapi import Depends
        # app.include_router(app_router, dependencies=[Depends(smart_admin_check_login)])

        # 自动注册模块路由
        load_controller_modules(app_router, module_dir="app/modules")

        app.include_router(app_router)

    def _register_middlewares(self, app: FastAPI) -> None:
        pass
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        # 读取响应报文和读取请求报文信息的中间件
        from core.middleware.request_response import (
            RequestResponseMiddleware,
        )

        app.add_middleware(RequestResponseMiddleware)


# ############################################################################
# ############################# 启动说明 #############################
# ############################################################################
# 如果下面的代码放在main中的话，
# core_app = FastApplicationBuilder \
#     .with_environment_settings() \
#     .build()
# 也会类似下面的代码执行两次！
# if __name__ == "__main__":
#     直接在这里跑的会会运行两次，需要注意。所以建议单独放到main中运行，否则一些注册会执行多次
#     import uvicorn
#     import os
#     # 使用os.path.basename函数获取了当前文件的名称，并将.py文件扩展名替换为空字符串
#     app_modeel_name = os.path.basename(__file__).replace(".py", "")
#     # 使用uvicorn.run函数运行了一个应用程序。它指定了应用程序的主机和端口，并且设置了reload参数为True。
#     uvicorn.run(f"{app_modeel_name}:core_app", host='127.0.0.1',port=31100,reload=True)
# ############################################################################
# ############################# 启动说明 #############################
# ############################################################################
app = FastApplicationBuilder.with_environment_settings().build()
