from sqlmodel import SQLModel, Field, Relationship

class TeamBase(SQLModel):
    name: str = Field(index=True, unique=True)
    headquarters: str

class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    heroes: list["Hero"] = Relationship(back_populates="team")

class TeamCreate(TeamBase):
    pass

class TeamPublic(TeamBase):
    id: int

class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = None
    secret_name: str
    team_id: int | None = Field(default=None, foreign_key="team.id")
    power: str | None = None  
    

class HeroCreate(HeroBase):
    pass

class HeroPublic(HeroBase):
    id: int

class HeroUpdate(SQLModel):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None
    team_id: int | None = None
    power: str | None = None

class HeroMissionLink(SQLModel, table=True):
    hero_id: int | None = Field(default=None, foreign_key="hero.id", primary_key=True)
    mission_id: int | None = Field(default=None, foreign_key="mission.id", primary_key=True)


class MissionBase(SQLModel):
    title: str = Field(index=True)


class Mission(MissionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    # Quan hệ nhiều-nhiều ngược lại với Hero
    heroes: list["Hero"] = Relationship(back_populates="missions", link_model=HeroMissionLink)


class MissionCreate(MissionBase):
    pass


class MissionPublic(MissionBase):
    id: int

class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    team: Team | None = Relationship(back_populates="heroes")
    missions: list["Mission"] = Relationship(back_populates="heroes", link_model=HeroMissionLink)

