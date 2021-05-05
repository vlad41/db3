import json

from flask import render_template, request
from icecream import ic

from site_logic.utils import db_util
from site_logic.utils.db_util import get_all_ttn

result_list = get_all_ttn()


def handle():
    end = 2019
    start = 2013
    ttn = request.args.get('ttn', None)
    if end and start and ttn:
        years_values = get_info_from_db(start, end, ttn)
        if years_values:
            al1 = ''
            al2 = ''
            al3 = ''
            al4 = ''
            al5 = ''

            title = years_values[0].get('product')
            text = create_graph_text(years_values)
            text.sort(reverse=True)
            if text:
                try:
                    al1 = text[0]
                    al2 = text[1]
                    al3 = text[2]
                    al4 = text[3]
                    al5 = text[4]
                except IndexError as e:
                    print(e)
                finally:
                    return render_template('graph.html', prod_link=title,
                                           al1=al1,
                                           al2=al2,
                                           al3=al3,
                                           al4=al4,
                                           al5=al5, )
    return render_template('main_page.html', title='Не знайдено', ttn_codes=result_list)


def create_graph_text(years_values):
    text = []
    for year_value in years_values:
        unit = year_value.get('unit')
        produced = year_value.get('produced')
        year = year_value.get('year')
        result = '{} рік: {} {}'.format(year, produced, unit)
        text.append(result)
    return text


def get_info_from_db(year_f, year_l, ttn, title=None):
    if ttn:
        product_info = db_util.get_from_db_in_filter(table_class=db_util.ProductionLink,
                                                     identifier=db_util.ProductionLink.ttn_code,
                                                     value=ttn,
                                                     get_type='one')

        products = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.ProductInfo,
                                                             identifier=db_util.ProductInfo.ttn_code,
                                                             value=ttn,
                                                             get_type='many')
        years_values = []
        if products:
            for product_meta in products:
                if isinstance(product_meta, db_util.ProductInfo):
                    if int(year_f) <= product_meta.year <= int(year_l):
                        years_values.append({'product': product_info.title,
                                             'unit': product_meta.unit_type,
                                             'produced': product_meta.produced,
                                             'year': product_meta.year})
        return years_values
