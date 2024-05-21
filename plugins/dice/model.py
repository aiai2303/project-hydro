from sqlalchemy import create_engine, Column, BigInteger, String
from sqlalchemy.orm import declarative_base, sessionmaker
from environment import neon_url

Base = declarative_base()


class Model64(Base):
    __tablename__ = "type64"
    user_id = Column(BigInteger, primary_key=True)
    first_name = Column(String)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    point = Column(BigInteger, default=0)


class Model6(Base):
    __tablename__ = "type6"
    user_id = Column(BigInteger, primary_key=True)
    first_name = Column(String)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    point = Column(BigInteger, default=0)


class Model5(Base):
    __tablename__ = "type5"
    user_id = Column(BigInteger, primary_key=True)
    first_name = Column(String)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    point = Column(BigInteger, default=0)


class Database:
    def __init__(self):
        self.engine = create_engine(neon_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def update(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        username: str,
        point: int,
        model: Model64 | Model6 | Model5,
    ):
        user = model(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            point=point,
        )
        self.session.merge(user)
        self.session.commit()

    def get(
        self, user_id: int, model: Model64 | Model6 | Model5
    ) -> Model64 | Model6 | Model5 | None:
        user = self.session.query(model).filter_by(user_id=user_id).first()
        if user and user.point > 0:
            return user

    def list(self, model: Model64 | Model6 | Model5):
        return self.session.query(model).all()

    def reset(self):
        list64 = self.session.query(Model64).all()

        list6 = self.session.query(Model6).all()

        list5 = self.session.query(Model5).all()

        for user in list64:
            user.point = 0

        for user in list6:
            user.point = 0

        for user in list5:
            user.point = 0

        self.session.commit()
