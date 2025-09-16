from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from pandas.io import sql


engine = create_engine("sqlite:///verification.db")
Base = declarative_base()
name_team = input("Введите наименование организации: ")
delete_table = "DROP TABLE IF EXISTS {};".format(name_team)
Session = sessionmaker(bind=engine)
session = Session()


class Equipment(Base):
    "Создание таблицы с заданным пользователем именем"
    __tablename__ = name_team

    id = Column(Integer, primary_key=True)
    responsible = Column(String(100), nullable=True)
    number_object = Column(String(20), nullable=True)
    name_equipment = Column(String(100), nullable=True)
    equipment_type = Column(String(100), nullable=True)
    factory_number = Column(String(100), nullable=True)
    verification_date = Column(String(20))

    def __repr__(self):
        return "| Ответственный: {} | Номер объекта: {} | Наименование: {} | Тип: {} | Заводской номер: {} | Дата поверки: {} |".format(
            self.responsible,
            self.number_object,
            self.name_equipment,
            self.equipment_type,
            self.factory_number,
            self.verification_date,
        )

# Удаляет таблицу если она уже существует
Base.metadata.drop_all(engine)
# Создаёт таблицу
Base.metadata.create_all(engine)


def adding_data(responsible, object, name, eq_type, number, date):
    "Добавляет значения в таблицу"
    new_data = Equipment(
        responsible=responsible,
        number_object=object,
        name_equipment=name,
        equipment_type=eq_type,
        factory_number=number,
        verification_date=date,
    )
    session.add(new_data)
    session.commit()
