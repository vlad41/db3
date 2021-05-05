from icecream import ic
from sqlalchemy import Integer, Column, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql.expression import func

import config_interpreter

# todo change alchemy path
path_alchemy_local = config_interpreter.alchemy_db_path
engine_p = create_engine(path_alchemy_local, echo=False, pool_size=3)
Base = declarative_base()


# region db engine
def create_db():
    Base.metadata.create_all(bind=engine_p)


def get_session():
    session_creator = sessionmaker(bind=engine_p)
    session = session_creator()
    return session


# endregion


# region tables
class ProductionLink(Base):
    __tablename__ = "production_link"

    ttn_code = Column('ttn_code', String, unique=True, primary_key=True)
    title = Column('title', String, unique=False)
    meta = relationship("ProductInfo")


class ProductInfo(Base):
    __tablename__ = "product_info"
    id = Column('id', Integer, primary_key=True, unique=True, autoincrement=True)
    year = Column('year', Integer, unique=False)
    unit_type = Column('unit_type', String, unique=False)
    ttn_code = Column(String, ForeignKey('production_link.ttn_code'))
    produced = Column('produced', String, unique=False)


# endregion


# region abstract get_from_db
def get_from_db_in_filter(table_class, identifier, value, get_type):
    """:param table_class - select table
    :param identifier - select filter column
    :param value - enter value to column
    :param get_type - string 'many' or 'one'"""
    many = 'many'
    one = 'one'
    session = get_session()
    if get_type == one:
        obj = session.query(table_class). \
            filter(identifier.contains(value)).first()
        session.close()
        return obj
    elif get_type == many:
        objs = session.query(table_class). \
            filter(identifier.contains(value)).all()
        session.close()
        return objs
    session.close()


def get_from_db_eq_filter_not_editing(table_class, identifier=None, value=None, get_type='one', eq: bool = True,
                                      all_objects: bool = None):
    """WARNING! DO NOT USE THIS OBJECT TO EDIT DATA IN DATABASE! IT ISN`T WORK!
    USE ONLY TO SHOW DATA...
    :param table_class - select table
    :param identifier - select filter column
    :param value - enter value to column
    :param get_type - string 'many' or 'one'
    :param eq - choose the value equals to column or not
    :param all_objects - return all rows from table"""
    many = 'many'
    one = 'one'
    session = get_session()
    if all_objects is True:
        objs = session.query(table_class).all()
        session.close()
        return objs
    if get_type == one:
        if eq:
            obj = session.query(table_class). \
                filter(identifier == value).first()
        else:
            obj = session.query(table_class). \
                filter(identifier != value).first()

        session.close()
        return obj
    elif get_type == many:
        if eq:
            objs = session.query(table_class). \
                filter(identifier == value).all()
        else:
            objs = session.query(table_class). \
                filter(identifier != value).all()

        session.close()
        return objs
    session.close()


# endregion


# region abstract write


def write_obj_to_table(table_class, identifier=None, value=None, **column_name_to_value):
    """column name to value must be exist in table class in columns"""
    # get obj
    session = get_session()
    is_new = False
    if identifier:
        tab_obj = session.query(table_class).filter(identifier == value).first()
    else:
        tab_obj = table_class()
        is_new = True

    # is obj not exist in db, we create them
    if not tab_obj:
        tab_obj = table_class()
        is_new = True
    for col_name, val in column_name_to_value.items():
        tab_obj.__setattr__(col_name, val)
    # if obj created jet, we add his to db
    if is_new:
        session.add(tab_obj)
    # else just update
    session.commit()
    session.close()


# endregion


# region abstract edit
# test this method
def edit_obj_in_table(table_class, identifier=None, value=None, **column_name_to_value):
    """column name to value must be exist in table class in columns"""
    # get bj
    session = get_session()
    tab_obj = session.query(table_class).filter(identifier == value).first()

    if tab_obj:
        for col_name, val in column_name_to_value.items():
            tab_obj.__setattr__(col_name, val)
    session.commit()
    session.close()


# endregion


# region abstract delete from db
def delete_obj_from_table(table_class, identifier=None, value=None):
    """column name to value must be exist in table class in columns"""
    session = get_session()
    result = session.query(table_class).filter(identifier == value).delete()
    ic('affected {} rows'.format(result))
    session.commit()
    session.close()


# endregion

# endregion
# region get random_obj
def get_random_obj(table_class):
    session = get_session()
    result = session.query(table_class).order_by(func.random()).first()
    session.close()
    return result


# endregion


def get_all_ttn():
    all_codes = get_from_db_eq_filter_not_editing(ProductionLink, all_objects=True)
    res_list = []
    for code in all_codes:
        if isinstance(code, ProductionLink):
            if code.ttn_code not in res_list:
                res_list.append(code.ttn_code)
    return res_list
