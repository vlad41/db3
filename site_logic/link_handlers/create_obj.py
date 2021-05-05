import sqlalchemy
from flask import render_template, request
from icecream import ic

from site_logic.utils import db_util
from site_logic.utils.db_util import get_all_ttn

result_list = get_all_ttn()


def handle_menu():
    return render_template('creating page/creating_menu.html', ttn_codes=result_list)


def handle_obj_creating():
    title = request.form['title']
    ttn = request.form['ttn_code']
    unit_type = request.form['unit_type']
    produced = request.form['produced']
    year = request.form['year']
    print('saved')
    ic(title, ttn, unit_type, produced, year)

    db_util.write_obj_to_table(table_class=db_util.ProductionLink,
                               identifier=db_util.ProductionLink.ttn_code,
                               value=ttn,
                               ttn_code=ttn,
                               title=title)
    product_link = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.ProductionLink,
                                                             identifier=db_util.ProductionLink.ttn_code,
                                                             value=ttn)
    if isinstance(product_link, db_util.ProductionLink):
        products = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.ProductInfo,
                                                             identifier=db_util.ProductInfo.ttn_code,
                                                             value=product_link.ttn_code,
                                                             get_type='many')

        not_wr = True
        if products:
            for prod_meta in products:
                if isinstance(prod_meta, db_util.ProductInfo):
                    if prod_meta.year == int(year):
                        db_util.write_obj_to_table(table_class=db_util.ProductInfo,
                                                   identifier=db_util.ProductInfo.id,
                                                   value=prod_meta.id,
                                                   year=year,
                                                   unit_type=unit_type,
                                                   ttn_code=ttn,
                                                   produced=produced)
                        not_wr = False
            if not_wr:
                db_util.write_obj_to_table(table_class=db_util.ProductInfo,
                                           year=year,
                                           unit_type=unit_type,
                                           ttn_code=ttn,
                                           produced=produced)
        else:
            db_util.write_obj_to_table(table_class=db_util.ProductInfo,
                                       year=year,
                                       unit_type=unit_type,
                                       ttn_code=ttn,
                                       produced=produced)

            print('saved')
    result_list = get_all_ttn()
    return render_template('creating page/creating_menu.html', title='Створено!', ttn_codes=result_list)
