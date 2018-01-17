import re


def _sort_key_list(keys):
    keys.sort()
    keys.sort(key=lambda x: x.find('YTD'), reverse=True)
    keys.sort(key=lambda x: not x.find('NonConsolidatedMember'), reverse=True)
    return keys

def sort_dict_key(dict):
    '''
    :param dict:
    :return: list of keys
    '''
    keys = list(dict.keys())
    keys = _sort_key_list(keys)
    return keys

def sort_dict_value(dict):
    keys = list(dict.keys())
    keys = _sort_key_list(keys)
    values = []
    for key in keys:
        values.append(dict[key])
    return values

def format_element_name(element_name):
    word = element_name
    new_word = ''
    for letter in word:
        if re.match('[A-Z]+', letter):
            new_word = new_word + ' ' + letter
        else:
            new_word = new_word + letter
    return new_word.split(':')[1]

def sort_list(dict):
    '''
    :param dict:
    :return: list of value
    '''

    if 'FilingDateInstant' in dict:
        return ['FilingDateInstant']

    if 'CurrentYTDDuration_NonConsolidatedMember' in dict:
        return ['CurrentYTDDuration_NonConsolidatedMember']

    if 'CurrentYTDDuration' in dict:
        return ['CurrentYTDDuration']

    if 'CurrentQuarterInstant_NonConsolidatedMember' in dict:
        return ['CurrentQuarterInstant_NonConsolidatedMember']

    if 'CurrentQuarterInstant' in dict:
        return ['CurrentQuarterInstant']

    if 'InterimDuration_NonConsolidatedMember' in dict:
        return ['InterimDuration_NonConsolidatedMember', 'Prior1YearDuration_NonConsolidatedMember', 'Prior2YearDuration_NonConsolidatedMember']

    if 'InterimDuration' in dict:
        return ['InterimDuration', 'Prior1YearDuration', 'Prior2YearDuration']

    if 'InterimInstant_NonConsolidatedMember' in dict:
        return ['InterimInstant_NonConsolidatedMember', 'Prior1InterimInstant_NonConsolidatedMember', 'Prior2InterimInstant_NonConsolidatedMember']

    if 'InterimInstant' in dict:
        return ['InterimInstant', 'Prior1InterimInstant', 'Prior2InterimInstant']

    if 'CurrentYearInstant_NonConsolidatedMember' in dict:
        return ['CurrentYearInstant_NonConsolidatedMember','Prior1YearInstant_NonConsolidatedMember','Prior1YearInstant_NonConsolidatedMember','Prior2YearInstant_NonConsolidatedMember','Prior4YearInstant_NonConsolidatedMember']

    if 'CurrentYearInstant' in dict:
        return ['CurrentYearInstant','Prior1YearInstant','Prior1YearInstant','Prior2YearInstant','Prior4YearInstant']

    if 'CurrentYearDuration_NonConsolidatedMember' in dict:
        return ['CurrentYearDuration_NonConsolidatedMember','Prior1YearDuration_NonConsolidatedMember','Prior2YearDuration_NonConsolidatedMember','Prior3YearDuration_NonConsolidatedMember','Prior4YearDuration_NonConsolidatedMember']

    if 'CurrentYearDuration' in dict:
        return ['CurrentYearDuration','Prior1YearDuration','Prior2YearDuration','Prior3YearDuration','Prior4YearDuration']



def sort_elements_by_year(dict):
    '''
    :param dict:
    :return: list of value
    '''
    try:
        return_list = []
        elements = sort_list(dict)
        for element in elements:
            if element in dict:
                return_list.append(dict[element])
            else:
                return_list.append(None)
        return return_list
    except:
        return []

def change_security_code_to_yahoo_code(code):
    code = str(code)
    return code[0:4]

def get_values_from_list(dictionary, elements, i):
    if elements[i] in dictionary:
        return dictionary(elements[i])
    else:
        return None

def get_element(document, element, attrib=None):
    try:
        if attrib is None:
            record = document[element]
        else:
            record = document[element][attrib]
        return record
    except KeyError:
        pass
    except:
        return 0

def float_to_str(flt):
    return str(int(flt))

def str_to_float(st):
    return float(int(st))

def is_element_exist(dict,element):
    return element in dict

class counter():
    def __init__(self, num):
        self.count = num

    def increment(self):
        self.count = self.count + 1
        return self.count

