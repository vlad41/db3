from flask import request, flash, redirect, url_for, render_template
from icecream import ic

import constant


def handle():
    ttn_code = request.form.get('ttn_code')

    return redirect(url_for(constant.Links.graph.replace('/', ''),
                            start=2013,
                            end=2019,
                            ttn=ttn_code))
