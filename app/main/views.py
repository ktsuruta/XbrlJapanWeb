from flask import render_template, redirect, url_for, abort, flash, request,\
current_app, make_response
from pymongo import MongoClient
from . import main
from .. import models
from .. import module

@main.route('/new', methods=['GET', 'POST'])
def index():

    db_sector = models.MongoDBControlerSector()
    db_annual = models.MongoDBControllerJpcrp030000()
    result_annual = db_annual.get_all_documents('report_date', 'Descending', 20)
    count_annual = db_annual.count_corporations()

    db_quarter_2 = models.MongoDBControllerJpcrp040300()
    result_quarter_2 = db_quarter_2.get_all_documents('report_date', 'Descending', 20)
    count_quarter_2 = db_quarter_2.count_corporations()

    return render_template('new.html', db_annual=db_annual, db_sector=db_sector, get_element=module.get_element, \
                           result_annual=result_annual, count_annual=count_annual, \
                           result_quarter_2=result_quarter_2, count_quarter_2=count_quarter_2)

@main.route('/', methods=['GET', 'POST'])
def overview():

    db_sector = models.MongoDBControlerSector()
    count_by_group = db_sector.count_by_group()

    if request.args.get('sort_key') is not None:
            sort_key = request.args.get('sort_key')
    else:
            sort_key = 'rate_of_return_on_equity'
    db_corporation = models.MongoDBControlerCorporation()
    rankings_by_rate_of_return_on_equity = db_corporation.get_all_rankings(sort_key)

    counter = module.counter(1)
    counter_ranking_class = module.counter

    get_sector_name = module.get_sector_name

    return render_template('overview.html',
                           get_element=module.get_element, db_sector=db_sector, count_by_group=count_by_group, \
                           rankings_by_rate_of_return_on_equity=rankings_by_rate_of_return_on_equity, counter=counter, \
                           counter_ranking_class=counter_ranking_class, \
                           get_sector_name=get_sector_name, sort_key=sort_key)

@main.route('/about')
def about():
    return render_template('about.html')

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
