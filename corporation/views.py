from flask import render_template, redirect, url_for, abort, flash, request,\
current_app, make_response
from pymongo import MongoClient
from . import corporation
from .. import models
from .. import module

def sort_list(dict):
    '''
    :param dict:
    :return: list of value
    '''
    if 'CurrentYearInstant_NonConsolidatedMember' in dict:
        return ['CurrentYearInstant_NonConsolidatedMember','Prior1YearInstant_NonConsolidatedMember','Prior1YearInstant_NonConsolidatedMember','Prior2YearInstant_NonConsolidatedMember','Prior4YearInstant_NonConsolidatedMember']

    if 'CurrentYearInstant' in dict:
        return ['CurrentYearInstant','Prior1YearInstant','Prior1YearInstant','Prior2YearInstant','Prior4YearInstant']

    if 'CurrentYearDuration_NonConsolidatedMember' in dict:
        return ['CurrentYearDuration_NonConsolidatedMember','Prior1YearDuration_NonConsolidatedMember','Prior2YearDuration_NonConsolidatedMember','Prior3YearDuration_NonConsolidatedMember','Prior4YearDuration_NonConsolidatedMember']

    if 'CurrentYearDuration' in dict:
        return ['CurrentYearDuration','Prior1YearDuration','Prior2YearDuration','Prior3YearDuration','Prior4YearDuration']

    if 'FilingDateInstant' in dict:
        return ['FilingDateInstant']

def sort_elements_by_year(dict):
    '''
    :param dict:
    :return: list of value
    '''
    return_list = []
    elements = sort_list(dict)
    for element in elements:
        if element in dict:
            return_list.append(dict[element])
        else:
            return_list.append(None)
    return return_list

def change_security_code_to_yahoo_code(code):
    code = str(code)
    return code[0:4]

def get_values_from_list(dictionary, elements, i):
    if elements[i] in dictionary:
        return dictionary(elements[i])
    else:
        return None

@corporation.route('/<code>/')
def index(code):
    db_annual = models.MongoDBControllerJpcrp030000()
    result = db_annual.get_the_latest_document(code)
    docs_annual_report = db_annual.get_documents(code)
    db_annual_report_2 = models.MongoDBControllerJpcrp030200()
    db_quarter_report = models.MongoDBControllerJpcrp040000()
    db_quarter_report_2 = models.MongoDBControllerJpcrp040300()
    db_half_year_report = models.MongoDBControllerJpcrp050000()
    db_half_year_report_2 = models.MongoDBControllerJpcrp050200()
    docs_annual_report_2 = db_annual_report_2.get_documents(code)
    docs_quarter_report = db_quarter_report.get_documents(code)
    docs_quarter_report_2 = db_quarter_report_2.get_documents(code)
    docs_half_year = db_half_year_report.get_documents(code)
    docs_half_year_2 = db_half_year_report_2.get_documents(code)
    db_sector = models.MongoDBControlerSector()
    sector = db_annual.get_sector(code, db_sector)
    return render_template('/corporation/corporation.html', code=code, sector=sector, result=result, docs_annual_report=docs_annual_report, docs_annual_report_2=docs_annual_report_2, \
                           docs_quarter_report=docs_quarter_report, docs_quarter_report_2=docs_quarter_report_2, docs_half_year=docs_half_year, \
                           docs_half_year_2=docs_half_year_2, get_element=module.get_element, sort_elements_by_year=module.sort_elements_by_year, \
                           change_security_code_to_yahoo_code=module.change_security_code_to_yahoo_code, get_values_from_list=module.get_values_from_list, \
                           format_element_name=module.format_element_name, db_sector=db_sector, db_annual=db_annual )

@corporation.route('/<code>/annual_report', methods=['GET'])
def annual_report(code):
    db_annual = models.MongoDBControllerJpcrp030000()
    file_name = request.args.get('file_name')
    if len(file_name) > 0:
        result = db_annual.get_the_document_by_file_name(file_name)
    else:
        result = db_annual.get_the_latest_document(code)
    return render_template('/corporation/corporation_annual_report.html', result=result, file_name=file_name, \
                           get_element=module.get_element, sort_elements_by_year=module.sort_elements_by_year, \
                           change_security_code_to_yahoo_code=module.change_security_code_to_yahoo_code, format_element_name=module.format_element_name, \
                           get_values_from_list=module.get_values_from_list, sort_dict_value=module.sort_dict_value, sort_dict_key=module.sort_dict_key)

@corporation.route('/<code>/quarter_report', methods=['GET'])
def quarter_report(code):
    db_annual = models.MongoDBControllerJpcrp040000()
    file_name = request.args.get('file_name')
    if len(file_name) > 0:
        result = db_annual.get_the_document_by_file_name(file_name)
    else:
        result = db_annual.get_the_latest_document(code)
    return render_template('/corporation/corporation_quarter_report.html', result=result, file_name=file_name, \
                           get_element=module.get_element, sort_elements_by_year=module.sort_elements_by_year, \
                           change_security_code_to_yahoo_code=module.change_security_code_to_yahoo_code, format_element_name=module.format_element_name, \
                           get_values_from_list=module.get_values_from_list, sort_dict_value=module.sort_dict_value, sort_dict_key=module.sort_dict_key)

@corporation.route('/<code>/quarter_report_2', methods=['GET'])
def quarter_report_2(code):
    db_annual = models.MongoDBControllerJpcrp040300()
    file_name = request.args.get('file_name')
    if len(file_name) > 0:
        result = db_annual.get_the_document_by_file_name(file_name)
    else:
        result = db_annual.get_the_latest_document(code)
    return render_template('/corporation/corporation_quarter_report_2.html', result=result, file_name=file_name, \
                           get_element=module.get_element, sort_elements_by_year=module.sort_elements_by_year, \
                           change_security_code_to_yahoo_code=module.change_security_code_to_yahoo_code, format_element_name=module.format_element_name, \
                           get_values_from_list=module.get_values_from_list, sort_dict_value=module.sort_dict_value, sort_dict_key=module.sort_dict_key)


@corporation.route('/<code>/half_year_report', methods=['GET'])
def half_year_report(code):
    db_annual = models.MongoDBControllerJpcrp050000()
    file_name = request.args.get('file_name')
    if len(file_name) > 0:
        result = db_annual.get_the_document_by_file_name(file_name)
    else:
        result = db_annual.get_the_latest_document(code)
    return render_template('/corporation/corporation_half_year_report.html', result=result, get_element=module.get_element, file_name=file_name, \
                           sort_elements_by_year=module.sort_elements_by_year, \
                           change_security_code_to_yahoo_code=module.change_security_code_to_yahoo_code, format_element_name=module.format_element_name, \
                           get_values_from_list=module.get_values_from_list, sort_dict_value=module.sort_dict_value, sort_dict_key=module.sort_dict_key)

@corporation.route('/<code>/half_year_report_2', methods=['GET'])
def half_year_report_2(code):
    db_annual = models.MongoDBControllerJpcrp050200()
    file_name = request.args.get('file_name')
    if len(file_name) > 0:
        result = db_annual.get_the_document_by_file_name(file_name)
    else:
        result = db_annual.get_the_latest_document(code)
    return render_template('/corporation/corporation_half_year_report_2.html', result=result, get_element=module.get_element, file_name=file_name, \
                           sort_elements_by_year=module.sort_elements_by_year, \
                           change_security_code_to_yahoo_code=module.change_security_code_to_yahoo_code, format_element_name=module.format_element_name, \
                           get_values_from_list=module.get_values_from_list, sort_dict_value=module.sort_dict_value, sort_dict_key=module.sort_dict_key)


