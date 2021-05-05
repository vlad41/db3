from flask import Flask, render_template, request
from icecream import ic

import constant
from site_logic import data_validation
from site_logic.link_handlers import edit_obj, create_obj, graph_init
from site_logic.utils import db_util, excel_to_db

# region init
db_util.create_db()
ic('db created []')
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

# toolbar = DebugToolbarExtension(app)
# endregion
result_list = db_util.get_all_ttn()


# region main pager
@app.route(constant.Links.main_page)
def index():
    if result_list:
        return render_template('main_page.html', ttn_codes=result_list)
    return render_template('main_page.html')


# endregion

# region crud
# region create
@app.route(constant.Links.create_obj)
def create():
    return create_obj.handle_menu()


@app.route(constant.Links.create_obj, methods=['POST'])
def handle():
    return create_obj.handle_obj_creating()


# endregion

# endregion

# region edit
@app.route(constant.Links.edit_obj)
def edit():
    # todo create delete and edit page and handle it
    return edit_obj.handle_ed_menu()


@app.route(constant.Links.edit_obj, methods=['POST'])
def handle_edit_post():
    print('handled')
    if request.values.get('find_button'):
        ttn = request.values.get('ttn_code')
        year = request.values.get('find_year')
        if ttn and year:
            return edit_obj.handle_find(ttn_code=ttn,
                                        year=year)
    elif len(request.values) > 3:

        if request.values.get('edit_button'):
            ttn = request.values.get('hidden_ttn')
            title = request.values.get('title')
            year = request.values.get('hidden_year')
            unit_type = request.values.get('unit_type')
            produced = request.values.get('produced')
            if ttn and title and year and unit_type and produced:
                return edit_obj.handle_edit(title=title,
                                            ttn_code=ttn,
                                            year=year,
                                            unit_type=unit_type,
                                            produced=produced)
        elif request.values.get('delete_button'):
            ttn = request.values.get('hidden_ttn')
            year = request.values.get('hidden_year')
            return edit_obj.handle_delete(ttn_code=ttn,
                                          year=year)
        return render_template('edit_page.html', title='Товар не знайдено!')


# endregion
# endregion

# region graph
@app.route(constant.Links.main_page, methods=['POST'])
def my_form_post():
    return data_validation.handle()


@app.route(constant.Links.graph)
def handle_graph():
    return graph_init.handle()


# region json
@app.route(constant.Ajax.get_products)
def get_products():
    pass
# endregion

# endregion
