from flask import render_template

# todo create find edit and  and add flashes next debug all this stuff create modified html page
from site_logic.utils import db_util
from site_logic.utils.db_util import get_all_ttn

result_list = get_all_ttn()


def handle_ed_menu():
    return render_template('edit_page.html', ttn_codes=result_list)


def handle_edit(title, ttn_code, year: int, produced: int, unit_type):
    products = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.ProductInfo,
                                                         identifier=db_util.ProductInfo.ttn_code,
                                                         value=ttn_code,
                                                         get_type='many')
    prod_id = None
    if products:
        for prod in products:
            if isinstance(prod, db_util.ProductInfo):
                if prod.year == int(year):
                    prod_id = prod.id
                    break
    if prod_id:
        db_util.edit_obj_in_table(table_class=db_util.ProductionLink,
                                  identifier=db_util.ProductionLink.ttn_code,
                                  value=ttn_code,
                                  title=title)
        db_util.edit_obj_in_table(table_class=db_util.ProductInfo,
                                  identifier=db_util.ProductInfo.id,
                                  value=prod_id,
                                  unit_type=unit_type,
                                  produced=produced)
        return render_template('edit_page.html', title='Відредаговано!', ttn_codes=result_list)
    return render_template('edit_page.html', title='Товар не знайдено!', ttn_codes=result_list)


def handle_find(ttn_code, year: int):
    if year.isdigit():
        products = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.ProductInfo,
                                                             identifier=db_util.ProductInfo.ttn_code,
                                                             value=ttn_code,
                                                             get_type='many')
        current_prod = None
        if products:
            for prod in products:
                if isinstance(prod, db_util.ProductInfo):
                    if prod.year == int(year):
                        current_prod = prod
                        break

        if current_prod:
            prod_link = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.ProductionLink,
                                                                  identifier=db_util.ProductionLink.ttn_code,
                                                                  value=ttn_code)
            if isinstance(prod_link, db_util.ProductionLink):
                return render_template('edit_page.html',
                                       unit_type=current_prod.unit_type,
                                       produced=current_prod.produced,
                                       year=year,
                                       ttn_code=ttn_code,
                                       title=prod_link.title)

    return render_template('edit_page.html', title='Не знайдено', ttn_codes=result_list)


def handle_delete(ttn_code, year):
    products = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.ProductInfo,
                                                         identifier=db_util.ProductInfo.ttn_code,
                                                         value=ttn_code,
                                                         get_type='many')
    prod_id = None
    if products:
        for prod in products:
            if isinstance(prod, db_util.ProductInfo):
                if prod.year == int(year):
                    prod_id = prod.id
                    break
    if prod_id:
        db_util.delete_obj_from_table(table_class=db_util.ProductInfo,
                                      identifier=db_util.ProductInfo.id,
                                      value=prod_id)
        return render_template('edit_page.html', title='Видалено!', ttn_codes=result_list)
    return render_template('edit_page.html', title='Не знайдено!', ttn_codes=result_list)
