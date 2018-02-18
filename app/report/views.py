from flask import render_template, redirect, url_for, abort, flash, request,\
current_app, make_response
from pymongo import MongoClient
from . import report
from .. import common
from .. import models
from .. import module


@report.route('/', methods=['GET'])
def report_by_type():
    if request.args.get('period') is not None:
        period = request.args.get('period')
    else:
        period = 'fiscal'

    if request.args.get('page') is not None:
        page = int(request.args.get('page'))
    else:
        page = 0
    if request.args.get('sort_key') is not None:
        sort_key = request.args.get('sort_key')
    else:
        sort_key = "rate_of_return_on_equity"

    db_corporation = models.MongoDBControlerCorporation()
    records_per_page = 50
    result_count = db_corporation.count_by_period(period, sort_key)
    total_page = int(result_count / records_per_page)
    result = db_corporation.get_ranking_by_period(type_of_period=period, sort_key=sort_key,order='Descending',page=page,records_by_page=records_per_page)


    return render_template('/report/report.html', result=result,  period=period, sort_key=sort_key,page=page, \
                           result_count=result_count,total_page=total_page, get_element=module.get_element)
