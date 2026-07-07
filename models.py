from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine("sqlite:///verification.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Equipment(Base):
    "Создание таблицы"
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    responsible = Column(String(100), nullable=True, name='Ответственный')
    number_object = Column(String(20), nullable=True, name="Номер объекта")
    name_equipment = Column(String(100), nullable=True, name="Наименование оборудования")
    equipment_type = Column(String(100), nullable=True, name="Тип оборудования")
    factory_number = Column(String(100), nullable=True, name="Заводской номер")
    verification_date = Column(String(20), name="Дата поверки")

    def __repr__(self):
        return (f"| Ответственный: {self.responsible} | "
                f"Номер объекта: {self.number_object} | "
                f"Наименование: {self.name_equipment} | "
                f"Тип: {self.equipment_type} | " 
                f"Заводской номер: {self.factory_number} | "
                f"Дата поверки: {self.verification_date} |")

def drop_tables(team_names):
    """Удаляет указанные таблицы из БД, если они существуют"""
    # Сначала регистрируем кламмы с правильными __tablename__, чтобы Base.metadata "увидел" эти таблицы
    tables_to_drop = []
    for name in team_names:
        class_name = f"Equipment_{name}"
        DynamicClass = type(
            class_name,
            (Equipment,),
            {
                "__tablename__": name,
                "__module__": __name__,
                "__table_args__": {"extend_existing": True}
            },
        )
        table = Base.metadata.tables.get(name)
        if table is not None:
            tables_to_drop.append(table)
    
    if tables_to_drop:
        Base.metadata.drop_all(engine, tables=tables_to_drop)
        print(f"✅ Удалены таблицы: {[t.name for t in tables_to_drop]}")
    else:
        print("ℹ️ Нет таблиц для удаления.")


def create_table_for_team(team_name):
    """Создает таблицу для конкретной компании"""
    # Динамически создаём класс для таблицы
    class_name = f"Equipment_{team_name}"
    dynamic_class = type(
        class_name,
        (Equipment,),
        {
            "__tablename__": team_name,
            "__module__": __name__,
            "__table_args__": {"extend_existing": True}
        }
    )
    
    # Создаёт таблицу
    Base.metadata.create_all(engine)
    
    return dynamic_class


def adding_data(responsible, object, name, eq_type, number, date, team_name):
    "Добавляет значения в таблицу"
    
    dynamic_class = create_table_for_team(team_name)
    
    new_data = dynamic_class(
        responsible=responsible,
        number_object=object,
        name_equipment=name,
        equipment_type=eq_type,
        factory_number=number,
        verification_date=date,
    )
    session.add(new_data)
    session.commit()
