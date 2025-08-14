from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    router_team_players,
    router_season,
    router_top_season
)

from routers.mission import(
    router_mission_name,
    router_mission_squad_player_stat,
    router_missions_list
)

from routers.player import(
    router_player_mission_stat,
    router_player_search,
    router_player_stat,
    router_player_top,
)

from routers.squad import(
    router_squad_mission_stat,
    router_squad_stat,
    router_squad_top
)

app = FastAPI(title="STATKA")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_missions_list.router, prefix="/api", tags=["информация о всех миссиях"])
app.include_router(router_player_mission_stat.router, prefix="/api", tags=["информация о игроках на мисках"])
app.include_router(router_squad_mission_stat.router, prefix='/api', tags=["информация о отрядах на миске"])
app.include_router(router_squad_top.router, prefix='/api', tags=["Топ отряды"])
app.include_router(router_player_stat.router, prefix='/api', tags=["Игрок по стате"])

app.include_router(router_player_top.router, prefix='/api', tags=["Топ игроки"])
app.include_router(router_player_top.router, prefix='/api', tags=["Топ игроки по тех"])
app.include_router(router_player_top.router, prefix='/api', tags=["Топ игроки по пех"])

app.include_router(router_squad_stat.router, prefix='/api', tags=["Отряд стата по названию"])
app.include_router(router_player_search.router, prefix='/api', tags=["Поиск игрока имени"])
app.include_router(router_mission_name.router, prefix='/api', tags=["Получить название миссии по id"])
app.include_router(router_team_players.router, prefix='/api', tags=["Получить игроков отряда"])
app.include_router(router_mission_squad_player_stat.router, prefix='/api', tags=["Получить мини стату игроков по отряду на мисии"])
app.include_router(router_season.router, prefix='/api', tags=["Получить инфу о сезонах"])
app.include_router(router_top_season.router, prefix='/api', tags=["Получить топы для доски почета по сезонам"])