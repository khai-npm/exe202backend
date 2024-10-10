from fastapi import FastAPI
# from src.routers.products.views import product_router
# from src.routers.orders.views import order_router
from fastapi.middleware.cors import CORSMiddleware
from src.events.startup import events as startup_event
from src.routers.account.views import account_router
from src.routers.task.views import task_router


app = FastAPI(on_startup=startup_event)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(product_router)
# app.include_router(order_router)

app.include_router(account_router)
app.include_router(task_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}