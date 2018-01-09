from flask import render_template, redirect, url_for, abort, flash, request,\
current_app, make_response
from pymongo import MongoClient
from . import report
from .. import models
from .. import module

@report.route('/annual_report', methods=['GET'])
def annual_report():
    if request.args.get('page') is not None:
        page = int(request.args.get('page'))
    else:
        page = 0
    if request.args.get('sort_key') is not None:
        sort_key = request.args.get('sort_key')
    else:
        sort_key = "report_date"

    db_annual = models.MongoDBControllerJpcrp030000()
    result_annual = db_annual.get_documents_by_page(sort_key=sort_key, order='Descending', page=page, records_by_page=50)
    count_annual = db_annual.count_corporations()

    return render_template('/report/annual_report.html', result_annual=result_annual, count_annual=count_annual, sort_key=sort_key, page=page, \
                           get_element=module.get_element)


@report.route('/quarter_report', methods=['GET'])
def quarter_report():
    if request.args.get('page') is not None:
        page = int(request.args.get('page'))
    else:
        page = 0

    if request.args.get('sort_key') is not None:
        sort_key = request.args.get('sort_key')
    else:
        sort_key = "report_date"

    db_quarter = models.MongoDBControllerJpcrp040000()
    result_quarter = db_quarter.get_documents_by_page(sort_key=sort_key, order='Descending', page=0, records_by_page=50)
    count_quarter = db_quarter.count_corporations()

    db_quarter_2 = models.MongoDBControllerJpcrp040300()
    result_quarter_2 = db_quarter_2.get_documents_by_page(sort_key=sort_key, order='Descending', page=0, records_by_page=50)
    count_quarter_2 = db_quarter_2.count_corporations()

    return render_template('/report/quarter_report.html', result_quarter=result_quarter, count_quarter=count_quarter, sort_key=sort_key, page=page, \
                           result_quarter_2=result_quarter_2, count_quarter_2=count_quarter_2,\
                           get_element=module.get_element)


@report.route('/half_year_report', methods=['GET'])
def half_year_report():
    if request.args.get('page') is not None:
        page = int(request.args.get('page'))
    else:
        page = 0

    if request.args.get('sort_key') is not None:
        sort_key = request.args.get('sort_key')
    else:
        sort_key = "report_date"
    db_half_year = models.MongoDBControllerJpcrp050000()
    result_half_year = db_half_year.get_documents_by_page(sort_key="report_date", order='Descending', page=0, records_by_page=50)
    count_half_year = db_half_year.count_corporations()

    db_half_year_2 = models.MongoDBControllerJpcrp050200()
    result_half_year_2 = db_half_year_2.get_documents_by_page(sort_key="report_date", order='Descending', page=0, records_by_page=50)
    count_half_year_2 = db_half_year_2.count_corporations()

    return render_template('/report/half_year_report.html', result_half_year=result_half_year, count_half_year=count_half_year, sort_key=sort_key, page=page, \
                           result_half_year_2=result_half_year_2, count_half_year_2=count_half_year_2, \
                           get_element=module.get_element)
