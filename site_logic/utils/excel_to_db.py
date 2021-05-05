import glob

import xlrd
from icecream import ic

from site_logic.utils import db_util


def start():
    # Give the location of the file
    loc = 'C:/Users/admin/Desktop/excel_vvp/vppv_13xls_u.xls'
    # To open Workbook
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)

    # For row 0 and column 0
    for i in range(4, 1000):
        year = 2013
        pre_unit_type = sheet.cell_value(i, 0)
        if isinstance(pre_unit_type, str):
            unit_type = pre_unit_type[pre_unit_type.rindex(',') + 1::].replace(' ', '')
            ttn_code = sheet.cell_value(i, 1)
            produced = sheet.cell_value(i, 2)

            # db_util.write_obj_to_table(table_class=db_util.ProductionLink,
            #                            identifier=db_util.ProductionLink.ttn_code,
            #                            value=ttn,
            #                            ttn_code=ttn,
            #                            title=title)
            ic(unit_type, ttn_code, produced)
            db_util.write_obj_to_table(table_class=db_util.ProductInfo,
                                       year=year,
                                       unit_type=unit_type,
                                       ttn_code=ttn_code,
                                       produced=produced)
            print('added {}'.format(i))


# 2016 down


if __name__ == '__main__':
    start()
