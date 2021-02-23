import asyncio

from starlette.endpoints import HTTPEndpoint
from starlette.concurrency import run_in_threadpool
from starlette.requests import Request
from starlette.responses import JSONResponse
from typing import get_args, get_origin, Union


class PydanticEndpoint(HTTPEndpoint):
    tags = None

    def check_union(self, parameter, parameter_type):
        for type_cls in get_args(parameter_type):
            if isinstance(type_cls, type):
                if isinstance(parameter, type_cls):
                    break
            else:
                if parameter == type_cls:
                    break
        else:
            raise Exception("Parameter valid error")

    async def check_parameter(self, handler, request, kwargs):
        # TODO: 补充场景： 表单提交、文件上传
        for parameter_name, parameter_type in handler.__annotations__.items():
            # 返回值
            if parameter_name == "return":
                continue

            # 请求Body
            if parameter_name == "body":
                if not await request.body():
                    parameter = {}
                else:
                    parameter = await request.json()
                kwargs['body'] = parameter_type(**parameter)
                continue

            # Path或Query参数
            parameter = kwargs.get(parameter_name)

            # 校验Union（Optional）
            if get_origin(parameter_type) is Union:
                self.check_union(parameter, parameter_type)

            else:
                if isinstance(parameter_type, type):
                    if parameter is None:
                        raise Exception("Need required parameter %s" % parameter_name)

                    if not isinstance(parameter, parameter_type):
                        raise Exception("Parameter valid error")
                else:
                    if not parameter == parameter_type:
                        raise Exception("Parameter valid error")

    async def dispatch(self) -> None:
        request = Request(self.scope, receive=self.receive)
        handler_name = "get" if request.method == "HEAD" else request.method.lower()
        handler = getattr(self, handler_name, self.method_not_allowed)
        is_async = asyncio.iscoroutinefunction(handler)

        # check query parameters
        kwargs = {'request': request}
        if request.query_params:
            kwargs.update(request.query_params)

        # check path parameters
        if request.path_params:
            kwargs.update(request.path_params)

        await self.check_parameter(handler, request, kwargs)

        if is_async:
            resp = await handler(**kwargs)
        else:
            resp = await run_in_threadpool(handler, **kwargs)
        response = JSONResponse(resp.dict())

        await response(self.scope, self.receive, self.send)
