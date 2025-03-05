#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""这是一个使用 FastAPI 框架创建的 Web 应用程序"""

# 必须在外部载入 app 对象

from app.application import app  # noqa: F401

if __name__ == "__main__":
    import inspect
    from pathlib import Path

    app_model_name = inspect.getmodulename(Path(__file__).name)
    import uvicorn

    uvicorn.run(
        f"{app_model_name}:app",
        host="0.0.0.0",
        port=8000,
        log_config=None,
        workers=1,
        reload=True,
    )
