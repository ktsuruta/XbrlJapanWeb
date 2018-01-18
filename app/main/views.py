from flask import render_template, redirect, url_for, abort, flash, request,\
current_app, make_response
from pymongo import MongoClient
from . import main
from .. import models
from .. import module

@main.route('/', methods=['GET', 'POST'])
def index():
    db_annual = models.MongoDBControllerJpcrp030000()
    result_annual = db_annual.get_all_documents('report_date', 'Descending', 10)
    count_annual = db_annual.count_corporations()

    db_annual_2 = models.MongoDBControllerJpcrp030200()
    result_annual_2 = db_annual_2.get_all_documents('report_date', 'Descending', 10)
    count_annual_2 = db_annual_2.count_corporations()

    db_quarter = models.MongoDBControllerJpcrp040000()
    result_quarter = db_quarter.get_all_documents('report_date', 'Descending', 10)
    count_quarter = db_quarter.count_corporations()

    db_quarter_2 = models.MongoDBControllerJpcrp040300()
    result_quarter_2 = db_quarter_2.get_all_documents('report_date', 'Descending', 10)
    count_quarter_2 = db_quarter_2.count_corporations()

    db_half_year = models.MongoDBControllerJpcrp050000()
    result_half_year = db_half_year.get_all_documents('report_date', 'Descending', 10)
    count_half_year = db_half_year.count_corporations()

    db_half_year_2 = models.MongoDBControllerJpcrp050200()
    result_half_year_2 = db_half_year_2.get_all_documents('report_date', 'Descending', 10)
    count_half_year_2 = db_half_year_2.count_corporations()

    db_sector = models.MongoDBControlerSector()

    count_by_group = db_sector.count_by_group()

    db_corporation = models.MongoDBControlerCorporation()
    rankings_by_sector_net_sales = db_corporation.get_all_rankings('net_sales_or_revenue')

    return render_template('index.html', result_annual=result_annual, count_annual=count_annual, \
                           result_annual_2=result_annual_2, count_annual_2=count_annual_2, \
                           result_half_year=result_half_year, count_half_year=count_half_year,\
                           result_half_year_2=result_half_year_2,count_half_year_2=count_half_year_2, \
                           result_quarter=result_quarter, count_quarter=count_quarter, \
                           result_quarter_2=result_quarter_2, count_quarter_2=count_quarter_2,\
                           get_element=module.get_element, db_sector=db_sector, db_annual=db_annual, count_by_group=count_by_group, \
                           rankings_by_sector_net_sales=rankings_by_sector_net_sales)

@main.route('/search', methods=['GET'])
def search_reports():
    query = request.args.get('query')

    db_annual = models.MongoDBControllerJpcrp030000()
    result_annual = db_annual.search_documents_by_query(query)

    db_quarter = models.MongoDBControllerJpcrp040300()
    result_quarter = db_quarter.search_documents_by_query(query)

    db_half = models.MongoDBControllerJpcrp050000()
    result_half_year = db_half.search_documents_by_query(query)


    return render_template('search.html', result_annual=result_annual,result_quarter=result_quarter, result_half_year=result_half_year, query=query, get_element=module.get_element)
