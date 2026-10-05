from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select, SQLModel
from app.database import engine, SessionDep, get_session
from app.models import Hero, HeroCreate, HeroPublic, HeroUpdate, Mission, MissionCreate, MissionPublic, Team, TeamCreate, TeamPublic

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Tạo tất cả các bảng trong database khi server vừa khởi động
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)


# --- TEAM ENDPOINTS (6.1) ---
@app.post("/teams", response_model=TeamPublic, status_code=201)
def create_team(team_in: TeamCreate, session: SessionDep):
    db_team = Team.model_validate(team_in)
    try:
        session.add(db_team)
        session.commit()
        session.refresh(db_team)
        return db_team
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Team already exists")

@app.get("/teams", response_model=list[TeamPublic])
def list_teams(session: SessionDep, offset: int = 0, limit: int = Query(default=10, le=100)):
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams

@app.get("/teams/{team_id}/heroes", response_model=list[HeroPublic])
def get_team_heroes(team_id: int, session: SessionDep):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team.heroes


# --- HERO ENDPOINTS (5.x, 6.2, 6.3) ---
@app.get("/heroes", response_model=list[HeroPublic])
def list_heroes(
    session: SessionDep, 
    offset: int = 0, 
    limit: int = Query(default=10, le=100),
    min_age: int | None = None,
    team_id: int | None = None,
    name: str | None = None,
):
    statement = select(Hero)
    
    # Xây dựng điều kiện lọc động (Dynamic filtering)
    if min_age is not None:
        statement = statement.where(Hero.age >= min_age)
    if team_id is not None:
        statement = statement.where(Hero.team_id == team_id)
    if name is not None:
        statement = statement.where(Hero.name.ilike(f"%{name}%"))
        
    heroes = session.exec(statement.offset(offset).limit(limit)).all()
    return heroes

@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def get_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@app.post("/heroes", response_model=HeroPublic, status_code=201)
def create_hero(hero_in: HeroCreate, session: SessionDep):
    # Kiểm tra xem team_id có tồn tại không trước khi tạo (6.3)
    if hero_in.team_id is not None:
        team = session.get(Team, hero_in.team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
            
    db_hero = Hero.model_validate(hero_in)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero_in: HeroUpdate, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    # Kiểm tra team_id mới nếu có cập nhật (6.3)
    if hero_in.team_id is not None:
        team = session.get(Team, hero_in.team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
    
    # Chỉ lấy các trường dữ liệu mà client thực sự gửi lên (exclude_unset=True)
    hero_data = hero_in.model_dump(exclude_unset=True)
    hero.sqlmodel_update(hero_data)
    
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.delete("/heroes/{hero_id}", status_code=204)
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    session.delete(hero)
    session.commit()
    return None

# main.py (Thêm các endpoint sau)

@app.post("/missions/", response_model=MissionPublic, status_code=201)
def create_mission(*, session: Session = Depends(get_session), mission: MissionCreate):
    db_mission = Mission.model_validate(mission)
    session.add(db_mission)
    session.commit()
    session.refresh(db_mission)
    return db_mission


@app.post("/heroes/{hero_id}/missions/{mission_id}", status_code=204)
def assign_hero_to_mission(
    hero_id: int, mission_id: int, session: Session = Depends(get_session)
):
    hero = session.get(Hero, hero_id)
    mission = session.get(Mission, mission_id)
    
    # Nếu không tìm thấy hero hoặc mission thì trả về lỗi 404
    if not hero or not mission:
        raise HTTPException(status_code=404, detail="Hero or Mission not found")
    
    # Nếu đã được gán rồi thì không làm gì cả (tránh trùng lặp)
    if mission not in hero.missions:
        hero.missions.append(mission)
        session.commit()
        
    return None


@app.get("/heroes/{hero_id}/missions", response_model=list[MissionPublic])
def read_hero_missions(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero.missions