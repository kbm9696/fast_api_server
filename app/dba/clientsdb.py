import logging

from sqlmodel import Session, select, create_engine, SQLModel, Field

# Connect to the PostgreSQL database
#database_url = "postgresql+psycopg2://postgres:9696@192.168.1.9:5432/testdba"
database_url = "postgres://fastapi:xjOAmoeYgDderm2Af5DZgS3PCW9R7uwH@dpg-ci5jielgkuvh0tmd81tg-a.oregon-postgres.render.com/testdba"

class Client(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(nullable=False)
    age: int
    requirement: str = Field(nullable=False)
    payment_done: bool = Field(default=False)
    requirement_done: bool = Field(default=False)

    class Config:
        tablename = "client"


class ClientDba:
    def __init__(self):
        self.engine = create_engine(database_url)
        # Create the all tables
        SQLModel.metadata.create_all(self.engine)

    def get(self):
        result = []
        try:
            with Session(self.engine) as s:
                q = s.query(Client).order_by(Client.id).all()
                for r in q:
                    r = r.__dict__
                    r.pop('_sa_instance_state')
                    result.append(r)
            return result
        except Exception as e:
            logging.error(f"Got Exception while perform get data from client table: {e}")
            return result

    def get_by_id(self,cid):
        result = {}
        try:
            with Session(self.engine) as s:
                q = s.query(Client).filter(Client.id == cid).first()
                result = q.__dict__
                result.pop('_sa_instance_state')
            return result
        except Exception as e:
            logging.error(f"Got Exception while perform get data from client table: {e}")
            return result

    def add(self, c):
        try:
            with Session(self.engine) as s:
                s.add(c)
                s.commit()
            return True
        except Exception as e:
            s.rollback()
            logging.error(f'Got error while insert new row into client table: {e}')
            return False

    def update(self,cid,data):
        try:
            with Session(self.engine) as s:
                q = s.query(Client).filter(Client.id==cid).first()
                if not q:
                    return False
                if 'name' in data:
                    q.name = data['name']
                if 'age' in data:
                    q.age = data['age']
                if 'requirement' in data:
                    q.requirement = data['requirement']
                s.commit()
            return True
        except Exception as e:
            s.rollback()
            logging.error(f'Got exception while update the client details into database: {e}')
            return False

    def delete(self,cid):
        try:
            with Session(self.engine) as s:
                q = s.query(Client).filter(Client.id == cid).delete()
                s.commit()
        except Exception as e:
            logging.error(f'Got Exception while delete the row from client table: {e}')

