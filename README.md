# starlette-pydantic
Automatic verification with pydantic

## usage
```python
from typing import Optional
from starlette.routing import Route
from starlette.applications import Starlette
from pydantic import BaseModel
from starlette_pydantic import PydanticEndpoint


class RequestBody(BaseModel):
    name: int


class ResponseBody(BaseModel):
    age: int


class UserDetail(PydanticEndpoint):

    @staticmethod
    async def get(request, username: str = None, page: Optional[str] = None) -> ResponseBody:
        return ResponseBody(age=11)


class User(PydanticEndpoint):

    @staticmethod
    async def post(request, body: RequestBody) -> ResponseBody:
        return ResponseBody(age=21)


routes = [
    Route("/user", User),
    Route("/user/{username}", UserDetail),
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("test.main:app", host="0.0.0.0", port=8000, reload=True, debug=True)

```