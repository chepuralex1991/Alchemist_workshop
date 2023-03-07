from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}"

engine = create_engine(DATABASE_URI)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))

    cars = relationship("Car", backref="company")


class Car(Base):
    __tablename__ = 'car'
    id = Column(Integer, primary_key=True)
    reg_number = Column(String(10))
    company_id = Column(Integer, ForeignKey('company.id'))


Base.metadata.create_all(engine)

liubava = Company(name='Liubava')
tov_apple = Company(name='TOV_Apple')
session.add_all([liubava, tov_apple])
session.commit()

car1 = Car(reg_number='AA5511BB', company=liubava)
car2 = Car(reg_number='AA5513BB', company=tov_apple)
car3 = Car(reg_number='AA5519BB', company=tov_apple)
session.add_all([car1, car2, car3])
session.commit()

liubava_cars = session.query(Car).join(Company).filter(Company.name == 'Liubava').count() # noqa
print(f"Liubava rents {liubava_cars} cars.")
