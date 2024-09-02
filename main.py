from fastapi import FastAPI

from city import router as city_router

app = FastAPI()

app.include_router(city_router.router)


@app.get("/")
def test():
    return {"hello": "hello world"}