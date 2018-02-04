from flask import render_template, redirect, url_for, abort, flash, request,\
current_app, make_response
from pymongo import MongoClient
from . import sector
from .. import models
from .. import module
from .. import common



@sector.route('/', methods=['GET'])
def index():
    return render_template('/sector/index.html')

@sector.route('/<sectorcode>', methods=['GET'])
def sector(sectorcode):
    counter = module.counter(0)
    if request.args.get('sort_key') is not None:
            sort_key = request.args.get('sort_key')
    else:
            sort_key = 'net_sales_or_revenue'

    db_annual = models.MongoDBControllerJpcrp030000()
    db_sector = models.MongoDBControlerSector()
    sectorname = common.mapping_sector[sectorcode]
    list_SecurityCodeDEI = db_sector.get_SecurityCodeDEI_by_sector(sectorcode)
    count_annual = len(list_SecurityCodeDEI)
    result_annual = db_annual.get_coporations_by_SecurityCodeDEI(SecurityCodeDEI=list_SecurityCodeDEI,sort_key=sort_key)

    sort_key=sort_key
    db_corporation = models.MongoDBControlerCorporation()
    result = db_corporation.get_ranking_by_sector(sector_code=sectorcode, sort_key=sort_key, limit_num=None)


    return render_template('/sector/sector.html', sectorcode=sectorcode, sectorname=sectorname, result_annual=result_annual,\
                            result=result, sort_key=sort_key, \
                           counter=counter, count_annual=count_annual, get_element=module.get_element)
