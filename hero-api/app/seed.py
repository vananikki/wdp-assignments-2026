from sqlmodel import Session, select
from app.database import engine, create_db_and_tables
from app.models import Team, Hero, Mission

def run_seed():
    create_db_and_tables()

    with Session(engine) as session:
        # Kiểm tra xem đã có ít nhất 1 team chưa (để chạy 2 lần an toàn không bị trùng lặp)
        existing_team = session.exec(select(Team)).first()
        if existing_team:
            print("Database already seeded! Skipping...")
            return

        print("Seeding database...")

        # 1. Tạo các Team
        team_avengers = Team(name="Avengers", headquarters="Avengers Tower")
        team_xmen = Team(name="X-Men", headquarters="X-Mansion")

        # 2. Tạo các Mission
        mission_sokovia = Mission(title="Battle of Sokovia")
        mission_thanos = Mission(title="Defeat Thanos")

        # 3. Tạo các Hero, gắn sẵn vào Team và Mission thông qua quan hệ object
        hero_ironman = Hero(
            name="Iron Man", 
            secret_name="Tony Stark", 
            team=team_avengers,
            missions=[mission_sokovia, mission_thanos]
        )
        hero_cap = Hero(
            name="Captain America", 
            secret_name="Steve Rogers", 
            team=team_avengers,
            missions=[mission_sokovia]
        )
        hero_thor = Hero(
            name="Thor", 
            secret_name="Thor Odinson", 
            team=team_avengers,
            missions=[mission_thanos]
        )
        hero_wolverine = Hero(
            name="Wolverine", 
            secret_name="Logan", 
            team=team_xmen,
            missions=[]
        )
        hero_storm = Hero(
            name="Storm", 
            secret_name="Ororo Munroe", 
            team=team_xmen,
            missions=[]
        )

        # 4. Thêm tất cả vào session và commit
        session.add(team_avengers)
        session.add(team_xmen)
        session.add(hero_ironman)
        session.add(hero_cap)
        session.add(hero_thor)
        session.add(hero_wolverine)
        session.add(hero_storm)
        session.commit()

        print("Seeding completed successfully!")

if __name__ == "__main__":
    run_seed()