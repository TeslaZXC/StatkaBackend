from fastapi import FastAPI
from routers import router_missions_list,router_player_mission_stat,router_squad_mission_stat,router_squad_top,router_player_stat,router_player_top,router_squad_stat

app = FastAPI(title="STATKA")

app.include_router(router_missions_list.router, prefix="/api",tags=["информация о всех миссиях"])
app.include_router(router_player_mission_stat.router,prefix="/api",tags=["информация о игроках на мисках"])
app.include_router(router_squad_mission_stat.router,prefix='/api',tags=["информация о отрядах на миске"])
app.include_router(router_squad_top.router,prefix='/api',tags=["Топ отряды"])
app.include_router(router_player_stat.router,prefix='/api',tags=["Игрок по стате"])
app.include_router(router_player_top.router,prefix='/api',tags=["Топ игроки"])
app.include_router(router_squad_stat.router,prefix='/api',tags=["Отряд стата по названию"])