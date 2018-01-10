import collections as collections
import datetime
import pymongo
from pymongo import MongoClient
from . import module
from . import common


class MongoDBConnector():
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.data_base

class MongoDBCommonModule():
    '''
    :param
    :return
    '''
    def get_all_documents(self, sort_key="report_date", order='Descending', limit_num=10):
        if order == 'Ascending':
            sort = pymongo.ASCENDING
        elif order == 'Descending':
            sort = pymongo.DESCENDING
        return self.collection.find({}).sort([(sort_key, sort)]).limit(limit_num)

    def get_documents_by_page(self, sort_key="report_date", order='Descending', page=0, records_by_page=50, year=None):
        start_record = page * records_by_page
        if order == 'Ascending':
            sort = pymongo.ASCENDING
        elif order == 'Descending':
            sort = pymongo.DESCENDING
        if year is None:
            year = common.DEFAULT_YEAR
        year_start = datetime.datetime(year, 1, 1, 0, 0, 0)
        year_end = datetime.datetime(year, 12, 31, 23, 59, 0)

        return self.collection.find({'report_date':{'$lt': year_end, '$gte': year_start}}).sort([(sort_key, sort)]).skip(start_record).limit(records_by_page)

    def get_corporation_data(self,code):
        return_dict = collections.defaultdict()
        tmp_file_names = self.collection.distinct("file_name",{"code": code})
        for file_name in tmp_file_names:
            for document in self.collection.find({"file_name": file_name}).sort([("report_date", pymongo.DESCENDING)]):
                for element in self.target_element:
                    tmp_key = element
                    return_dict[tmp_key] = self._get_element(document,element)
            return dict(return_dict)

    def get_documents(self, code):
        '''
        :param code:
        :return: list of documents
        '''
        return self.collection.find({"code":code}).sort([("report_date", pymongo.DESCENDING)])

    def get_the_latest_document(self,code):
        '''
        :param code:
        :return: dict of the latest document
        '''
        return self.collection.find({"code": code}).sort([("report_date", pymongo.DESCENDING)])[0]

    def get_the_document_by_file_name(self, file_name):
        print(file_name)
        return self.collection.find({"file_name": file_name})[0]

    def search_documents_by_query(self, query):
        print("search " + query)
        result = self.collection.find({'$text':{'$search':query}})
        print(result)
        #for a in result:
        #    print(a)
        print(type(result))
        return result

    def _get_element(self, document, element):
        try:
            record = document[element]
            return record
        except KeyError:
            pass

    def count_corporations(self):
        return len(self.collection.distinct("code"))

    def get_sector(self,code, InstanseMongoDBControlerSector):
        if self.collection.find({"$and": [{"code": code}, {"jpdei_cor:SecurityCodeDEI.FilingDateInstant": {"$ne": None}}]}).count() > 0:
            SecurityCodeDEI = self.collection.find_one({"$and": [{"code": code}, {"jpdei_cor:SecurityCodeDEI.FilingDateInstant": {"$ne": None}}]})["jpdei_cor:SecurityCodeDEI"]["FilingDateInstant"]
            SecurityCodeDEI = module.float_to_str(SecurityCodeDEI)
            return InstanseMongoDBControlerSector.get_sector_of_corporation(SecurityCodeDEI)
        return None

    def get_coporations_by_SecurityCodeDEI(self, SecurityCodeDEI="", sort_key=None):
        return_list_of_dict = []
        if type(SecurityCodeDEI) == list:
            for code in SecurityCodeDEI:
                code = module.str_to_float(code)
                return_list_of_dict.append(self.collection.find({"jpdei_cor:SecurityCodeDEI.FilingDateInstant" : code}).sort([("report_date", pymongo.DESCENDING)])[0])
            if sort_key is not None:
                print("before start " + str(len(return_list_of_dict)))
                new_return_list_of_dict = []
                for dict in return_list_of_dict:
                    if sort_key.split('.')[0] in dict:
                        if sort_key.split('.')[1] in dict[sort_key.split('.')[0]]:
                            if dict[sort_key.split('.')[0]][sort_key.split('.')[1]] is not None:
                                new_return_list_of_dict.append(dict)
                print("after start " + str(len(new_return_list_of_dict)))
                return_list_of_dict = sorted(new_return_list_of_dict, key=lambda k: int(k[sort_key.split('.')[0]][sort_key.split('.')[1]]), reverse=True)
            return return_list_of_dict
        else:
            if self.collection.find({"jpdei_cor:SecurityCodeDEI.FilingDateInstant": SecurityCodeDEI}).count() > 0:
                return self.collection.find({"jpdei_cor:SecurityCodeDEI.FilingDateInstant": SecurityCodeDEI}).sort([(sort_key, pymongo.DESCENDING)])[0]
            else:
                return None

    def is_exist(self,code):
        if self.collection.find({"code":code}).count() == 0:
            return False
        else:
            return True

class MongoDBControlerSector(MongoDBConnector, MongoDBCommonModule):

    def __init__(self):
        # noinspection PyUnresolvedReferences
        MongoDBConnector.__init__(self)
        self.collection = self.db['Sector']

    def get_sectors(self):
        return self.collection.distinct("Sector")

    def get_sector_of_corporation(self, SecurityCodeDEI):
        if self.collection.find({"SecurityCodeDEI":SecurityCodeDEI}).count() > 0:
            return self.collection.find_one({"SecurityCodeDEI": SecurityCodeDEI})['Sector']
        else:
            return None

    def get_SecurityCodeDEI_by_sector(self, sectorcode):
        if len(self.collection.find({"SectorCode": sectorcode}).distinct("SecurityCodeDEI")) > 0:
            len(self.collection.find({"SectorCode": sectorcode}).distinct("SecurityCodeDEI"))
            return self.collection.find({"SectorCode": sectorcode}).distinct("SecurityCodeDEI")
        else:
            return None


class MongoDBControllerJpcrp030000(MongoDBConnector,MongoDBCommonModule ):
    '''
    企業内容等の開示に関する内閣府令 第三号様式 有価証券報告書  (jpcrp030000-asr)
    '''

    def __init__(self):
        # noinspection PyUnresolvedReferences
        MongoDBConnector.__init__(self)
        self.collection = self.db['jpcrp030000']

        self.target_element = [
            'jpdei_cor:EDINETCodeDEI',
            'jpdei_cor:FundCodeDEI',
            'jpdei_cor:SecurityCodeDEI',
            'jpdei_cor:FundNameInJapaneseDEI',
            'jpdei_cor:FundNameInEnglishDEI',
            'jpdei_cor:IndustryCodeWhenConsolidatedFinancialStatementsArePreparedInAccordanceWithIndustrySpecificRegulationsDEI',
            'jpdei_cor:IndustryCodeWhenFinancialStatementsArePreparedInAccordanceWithIndustrySpecificRegulationsDEI',
            'jpdei_cor:CurrentFiscalYearStartDateDEI',
            'jpdei_cor:CurrentPeriodEndDateDEI',
            'jpdei_cor:TypeOfCurrentPeriodDEI',
            'jpdei_cor:CurrentFiscalYearEndDateDEI',
            'jpdei_cor:WhetherConsolidatedFinancialStatementsArePreparedDEI',
            'jpdei_cor:AccountingStandardsDEI',
            'jpcrp_cor:DocumentTitleCoverPage',
            'jpcrp_cor:ClauseOfStipulationCoverPage',
            'jpcrp_cor:PlaceOfFilingCoverPage',
            'jpcrp_cor:FilingDateCoverPage',
            'jpcrp_cor:FiscalYearCoverPage',
            'jpcrp_cor:CompanyNameCoverPage',
            'jpcrp_cor:CompanyNameInEnglishCoverPage',
            'jpcrp_cor:TitleAndNameOfRepresentativeCoverPage',
            'jpcrp_cor:AddressOfRegisteredHeadquarterCoverPage',
            'jpcrp_cor:TelephoneNumberAddressOfRegisteredHeadquarterCoverPage',
            'jpcrp_cor:NameOfContactPersonAddressOfRegisteredHeadquarterCoverPage',
            'jpcrp_cor:NearestPlaceOfContactCoverPage',
            'jpcrp_cor:TelephoneNumberNearestPlaceOfContactCoverPage',
            'jpcrp_cor:NameOfContactPersonNearestPlaceOfContactCoverPage',
            'jpcrp_cor:PlaceForPublicInspectionCoverPageTextBlock',
            'jpcrp_cor:PlaceForPublicInspectionCoverPageNA',
            'jpcrp_cor:BusinessResultsOfGroupHeading',
            'jpcrp_cor:BusinessResultsOfGroupTable',
            'jppfs_cor:ConsolidatedOrNonConsolidatedAxis',
            'jppfs_cor:ConsolidatedMember',
            'jpcrp_cor:BusinessResultsOfGroupLineItems',
            'jpcrp_cor:NetSalesSummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue2SummaryOfBusinessResults',
            'jpcrp_cor:GrossOperatingRevenueSummaryOfBusinessResults',
            'jpcrp_cor:OrdinaryIncomeSummaryOfBusinessResults',
            'jpcrp_cor:NetPremiumsWrittenSummaryOfBusinessResultsINS',
            'jpcrp_cor:OrdinaryIncomeLossSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossAttributableToOwnersOfParentSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioInternationalStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioBISStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandard2SummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquitySummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInOperatingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInInvestingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInFinancingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsSummaryOfBusinessResults',
            'jpcrp_cor:NumberOfEmployees',
            'jpcrp_cor:AverageNumberOfTemporaryWorkers',
            'jpcrp_cor:RevenueIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossBeforeTaxIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossFromContinuingOperationsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossAttributableToOwnersOfParentIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeAttributableToOwnersOfParentIFRSSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentIFRSSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioIFRSSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareIFRSSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsLossPerShareIFRSSummaryOfBusinessResults',
            'jpcrp_cor:RatioOfOwnersEquityToGrossAssetsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquityIFRSSummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:RevenueJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossBeforeTaxJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossFromContinuingOperationsJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossAttributableToOwnersOfParentJMISSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeJMISSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeAttributableToOwnersOfParentJMISSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentJMISSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsJMISSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioJMISSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareJMISSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsLossPerShareJMISSummaryOfBusinessResults',
            'jpcrp_cor:RatioOfOwnersEquityToGrossAssetsJMISSummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquityJMISSummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsJMISSummaryOfBusinessResults',
            'jpcrp_cor:RevenuesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:OperatingIncomeLossUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossBeforeTaxUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:NetIncomeLossAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityIncludingPortionAttributableToNonControllingInterestUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentPerShareUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsLossPerShareUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquityUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:BusinessResultsOfReportingCompanyHeading',
            'jpcrp_cor:BusinessResultsOfReportingCompanyTable',
            'jppfs_cor:ConsolidatedOrNonConsolidatedAxis',
            'jppfs_cor:NonConsolidatedMember',
            'jpcrp_cor:BusinessResultsOfReportingCompanyLineItems',
            'jpcrp_cor:NetSalesSummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue2SummaryOfBusinessResults',
            'jpcrp_cor:GrossOperatingRevenueSummaryOfBusinessResults',
            'jpcrp_cor:OrdinaryIncomeSummaryOfBusinessResults',
            'jpcrp_cor:NetPremiumsWrittenSummaryOfBusinessResultsINS',
            'jpcrp_cor:OrdinaryIncomeLossSummaryOfBusinessResults',
            'jpcrp_cor:NetIncomeLossSummaryOfBusinessResults',
            'jpcrp_cor:NetLossRatioSummaryOfBusinessResultsINS',
            'jpcrp_cor:NetOperatingExpenseRatioSummaryOfBusinessResultsINS',
            'jpcrp_cor:InterestAndDividendIncomeSummaryOfBusinessResultsINS',
            'jpcrp_cor:InvestmentAssetsYieldIncomeYieldSummaryOfBusinessResultsINS',
            'jpcrp_cor:InvestmentYieldRealizedYieldSummaryOfBusinessResultsINS',
            'jpcrp_cor:EquityInEarningsLossesOfAffiliatesIfEquityMethodIsAppliedSummaryOfBusinessResults',
            'jpcrp_cor:CapitalStockSummaryOfBusinessResults',
            'jpcrp_cor:TotalNumberOfIssuedSharesSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsSummaryOfBusinessResults',
            'jpcrp_cor:DepositsSummaryOfBusinessResults',
            'jpcrp_cor:LoansAndBillsDiscountedSummaryOfBusinessResults',
            'jpcrp_cor:SecuritiesSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:DividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:InterimDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:FirstQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:SecondQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:ThirdQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:FourthQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:FifthQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioInternationalStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioBISStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandard2SummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquitySummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioSummaryOfBusinessResults',
            'jpcrp_cor:PayoutRatioSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInOperatingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInInvestingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInFinancingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsSummaryOfBusinessResults',
            'jpcrp_cor:NumberOfEmployees',
            'jpcrp_cor:AverageNumberOfTemporaryWorkers',
            'jpcrp_cor:DescriptionOfBusinessTextBlock'

        ]

    def get_all_records(self):
        for document in self.collection.find():
            print(document)


class MongoDBControllerJpcrp030200(MongoDBConnector,MongoDBCommonModule ):
    '''
    企業内容等の開示に関する内閣府令 第三号の二様式 有価証券報告書  (jpcrp030200-asr)
    '''

    def __init__(self):
        # noinspection PyUnresolvedReferences
        MongoDBConnector.__init__(self)
        self.collection = self.db['jpcrp030200']

        self.target_element = [
            'jpdei_cor:EDINETCodeDEI',
            'jpdei_cor:FundCodeDEI',
            'jpdei_cor:SecurityCodeDEI',
            'jpdei_cor:FundNameInJapaneseDEI',
            'jpdei_cor:FundNameInEnglishDEI',
            'jpdei_cor:IndustryCodeWhenConsolidatedFinancialStatementsArePreparedInAccordanceWithIndustrySpecificRegulationsDEI',
            'jpdei_cor:IndustryCodeWhenFinancialStatementsArePreparedInAccordanceWithIndustrySpecificRegulationsDEI',
            'jpdei_cor:CurrentFiscalYearStartDateDEI',
            'jpdei_cor:CurrentPeriodEndDateDEI',
            'jpdei_cor:TypeOfCurrentPeriodDEI',
            'jpdei_cor:CurrentFiscalYearEndDateDEI',
            'jpdei_cor:WhetherConsolidatedFinancialStatementsArePreparedDEI',
            'jpdei_cor:AccountingStandardsDEI',
            'jpcrp_cor:CoverPageHeading',
            'jpcrp_cor:DocumentTitleCoverPage',
            'jpcrp_cor:ClauseOfStipulationCoverPage',
            'jpcrp_cor:PlaceOfFilingCoverPage',
            'jpcrp_cor:FilingDateCoverPage',
            'jpcrp_cor:FiscalYearCoverPage',
            'jpcrp_cor:CompanyNameCoverPage',
            'jpcrp_cor:CompanyNameInEnglishCoverPage',
            'jpcrp_cor:TitleAndNameOfRepresentativeCoverPage',
            'jpcrp_cor:AddressOfRegisteredHeadquarterCoverPage',
            'jpcrp_cor:TelephoneNumberAddressOfRegisteredHeadquarterCoverPage',
            'jpcrp_cor:NameOfContactPersonAddressOfRegisteredHeadquarterCoverPage',
            'jpcrp_cor:NearestPlaceOfContactCoverPage',
            'jpcrp_cor:TelephoneNumberNearestPlaceOfContactCoverPage',
            'jpcrp_cor:NameOfContactPersonNearestPlaceOfContactCoverPage',
            'jpcrp_cor:PlaceForPublicInspectionCoverPageTextBlock',
            'jpcrp_cor:PlaceForPublicInspectionCoverPageNA',
            'jpcrp_cor:BusinessResultsOfGroupHeading',
            'jpcrp_cor:BusinessResultsOfGroupTable',
            'jppfs_cor:ConsolidatedOrNonConsolidatedAxis',
            'jppfs_cor:ConsolidatedMember',
            'jpcrp_cor:BusinessResultsOfGroupLineItems',
            'jpcrp_cor:NetSalesSummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue2SummaryOfBusinessResults',
            'jpcrp_cor:GrossOperatingRevenueSummaryOfBusinessResults',
            'jpcrp_cor:OrdinaryIncomeSummaryOfBusinessResults',
            'jpcrp_cor:NetPremiumsWrittenSummaryOfBusinessResultsINS',
            'jpcrp_cor:OrdinaryIncomeLossSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossAttributableToOwnersOfParentSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioInternationalStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioBISStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandard2SummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquitySummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInOperatingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInInvestingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInFinancingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsSummaryOfBusinessResults',
            'jpcrp_cor:NumberOfEmployees',
            'jpcrp_cor:AverageNumberOfTemporaryWorkers',
            'jpcrp_cor:RevenueIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossBeforeTaxIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossFromContinuingOperationsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossAttributableToOwnersOfParentIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeAttributableToOwnersOfParentIFRSSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentIFRSSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioIFRSSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareIFRSSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsLossPerShareIFRSSummaryOfBusinessResults',
            'jpcrp_cor:RatioOfOwnersEquityToGrossAssetsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquityIFRSSummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:RevenueJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossBeforeTaxJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossFromContinuingOperationsJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossAttributableToOwnersOfParentJMISSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeJMISSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeAttributableToOwnersOfParentJMISSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentJMISSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsJMISSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioJMISSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareJMISSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsLossPerShareJMISSummaryOfBusinessResults',
            'jpcrp_cor:RatioOfOwnersEquityToGrossAssetsJMISSummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquityJMISSummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsJMISSummaryOfBusinessResults',
            'jpcrp_cor:RevenuesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:OperatingIncomeLossUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossBeforeTaxUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:NetIncomeLossAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityIncludingPortionAttributableToNonControllingInterestUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentPerShareUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsLossPerShareUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquityUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:BusinessResultsOfReportingCompanyHeading',
            'jpcrp_cor:BusinessResultsOfReportingCompanyTable',
            'jppfs_cor:ConsolidatedOrNonConsolidatedAxis',
            'jppfs_cor:NonConsolidatedMember',
            'jpcrp_cor:BusinessResultsOfReportingCompanyLineItems',
            'jpcrp_cor:NetSalesSummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue2SummaryOfBusinessResults',
            'jpcrp_cor:GrossOperatingRevenueSummaryOfBusinessResults',
            'jpcrp_cor:OrdinaryIncomeSummaryOfBusinessResults',
            'jpcrp_cor:NetPremiumsWrittenSummaryOfBusinessResultsINS',
            'jpcrp_cor:OrdinaryIncomeLossSummaryOfBusinessResults',
            'jpcrp_cor:NetIncomeLossSummaryOfBusinessResults',
            'jpcrp_cor:NetLossRatioSummaryOfBusinessResultsINS',
            'jpcrp_cor:NetOperatingExpenseRatioSummaryOfBusinessResultsINS',
            'jpcrp_cor:InterestAndDividendIncomeSummaryOfBusinessResultsINS',
            'jpcrp_cor:InvestmentAssetsYieldIncomeYieldSummaryOfBusinessResultsINS',
            'jpcrp_cor:InvestmentYieldRealizedYieldSummaryOfBusinessResultsINS',
            'jpcrp_cor:EquityInEarningsLossesOfAffiliatesIfEquityMethodIsAppliedSummaryOfBusinessResults',
            'jpcrp_cor:CapitalStockSummaryOfBusinessResults',
            'jpcrp_cor:TotalNumberOfIssuedSharesSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsSummaryOfBusinessResults',
            'jpcrp_cor:DepositsSummaryOfBusinessResults',
            'jpcrp_cor:LoansAndBillsDiscountedSummaryOfBusinessResults',
            'jpcrp_cor:SecuritiesSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:DividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:InterimDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:FirstQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:SecondQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:ThirdQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:FourthQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:FifthQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioInternationalStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioBISStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandard2SummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquitySummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioSummaryOfBusinessResults',
            'jpcrp_cor:PayoutRatioSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInOperatingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInInvestingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInFinancingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsSummaryOfBusinessResults',
            'jpcrp_cor:NumberOfEmployees',
            'jpcrp_cor:AverageNumberOfTemporaryWorkers'

        ]

    def get_all_records(self):
        for document in self.collection.find():
            print(document)

    def get_codes(self):
        return self.collection.find({},{"code":1,"jpcrp_cor:CompanyNameInEnglishCoverPage":1,"jpcrp_cor:NetSalesSummaryOfBusinessResults":1})


class MongoDBControllerJpcrp040000(MongoDBConnector,MongoDBCommonModule ):
    '''
    企業内容等の開示に関する内閣府令 第四号様式 有価証券報告書  (jpcrp040000-asr)
    '''

    def __init__(self):
        # noinspection PyUnresolvedReferences
        MongoDBConnector.__init__(self)
        self.collection = self.db['jpcrp040000']

        self.target_element = [
            'jpdei_cor:EDINETCodeDEI',
            'jpdei_cor:FundCodeDEI',
            'jpdei_cor:SecurityCodeDEI',
            'jpdei_cor:FundNameInJapaneseDEI',
            'jpdei_cor:FundNameInEnglishDEI',
            'jpdei_cor:IndustryCodeWhenConsolidatedFinancialStatementsArePreparedInAccordanceWithIndustrySpecificRegulationsDEI',
            'jpdei_cor:IndustryCodeWhenFinancialStatementsArePreparedInAccordanceWithIndustrySpecificRegulationsDEI',
            'jpdei_cor:CurrentFiscalYearStartDateDEI',
            'jpdei_cor:CurrentPeriodEndDateDEI',
            'jpdei_cor:TypeOfCurrentPeriodDEI',
            'jpdei_cor:CurrentFiscalYearEndDateDEI',
            'jpdei_cor:WhetherConsolidatedFinancialStatementsArePreparedDEI',
            'jpdei_cor:AccountingStandardsDEI',
            'jpcrp_cor:CoverPageHeading',
            'jpcrp_cor:DocumentTitleCoverPage',
            'jpcrp_cor:ClauseOfStipulationCoverPage',
            'jpcrp_cor:PlaceOfFilingCoverPage',
            'jpcrp_cor:FilingDateCoverPage',
            'jpcrp_cor:FiscalYearCoverPage',
            'jpcrp_cor:CompanyNameCoverPage',
            'jpcrp_cor:CompanyNameInEnglishCoverPage',
            'jpcrp_cor:TitleAndNameOfRepresentativeCoverPage',
            'jpcrp_cor:AddressOfRegisteredHeadquarterCoverPage',
            'jpcrp_cor:TelephoneNumberAddressOfRegisteredHeadquarterCoverPage',
            'jpcrp_cor:NameOfContactPersonAddressOfRegisteredHeadquarterCoverPage',
            'jpcrp_cor:NearestPlaceOfContactCoverPage',
            'jpcrp_cor:TelephoneNumberNearestPlaceOfContactCoverPage',
            'jpcrp_cor:NameOfContactPersonNearestPlaceOfContactCoverPage',
            'jpcrp_cor:PlaceForPublicInspectionCoverPageTextBlock',
            'jpcrp_cor:PlaceForPublicInspectionCoverPageNA',
            'jpcrp_cor:BusinessResultsOfGroupHeading',
            'jpcrp_cor:BusinessResultsOfGroupTable',
            'jppfs_cor:ConsolidatedOrNonConsolidatedAxis',
            'jppfs_cor:ConsolidatedMember',
            'jpcrp_cor:BusinessResultsOfGroupLineItems',
            'jpcrp_cor:NetSalesSummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue2SummaryOfBusinessResults',
            'jpcrp_cor:GrossOperatingRevenueSummaryOfBusinessResults',
            'jpcrp_cor:OrdinaryIncomeSummaryOfBusinessResults',
            'jpcrp_cor:NetPremiumsWrittenSummaryOfBusinessResultsINS',
            'jpcrp_cor:OrdinaryIncomeLossSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossAttributableToOwnersOfParentSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioInternationalStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioBISStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandard2SummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquitySummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInOperatingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInInvestingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInFinancingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsSummaryOfBusinessResults',
            'jpcrp_cor:NumberOfEmployees',
            'jpcrp_cor:AverageNumberOfTemporaryWorkers',
            'jpcrp_cor:RevenueIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossBeforeTaxIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossFromContinuingOperationsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossAttributableToOwnersOfParentIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeAttributableToOwnersOfParentIFRSSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentIFRSSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioIFRSSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareIFRSSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsLossPerShareIFRSSummaryOfBusinessResults',
            'jpcrp_cor:RatioOfOwnersEquityToGrossAssetsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquityIFRSSummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:RevenueJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossBeforeTaxJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossFromContinuingOperationsJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossAttributableToOwnersOfParentJMISSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeJMISSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeAttributableToOwnersOfParentJMISSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentJMISSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsJMISSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioJMISSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareJMISSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsLossPerShareJMISSummaryOfBusinessResults',
            'jpcrp_cor:RatioOfOwnersEquityToGrossAssetsJMISSummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquityJMISSummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsJMISSummaryOfBusinessResults',
            'jpcrp_cor:RevenuesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:OperatingIncomeLossUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossBeforeTaxUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:NetIncomeLossAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityIncludingPortionAttributableToNonControllingInterestUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentPerShareUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsLossPerShareUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquityUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:BusinessResultsOfReportingCompanyHeading',
            'jpcrp_cor:BusinessResultsOfReportingCompanyTable',
            'jppfs_cor:ConsolidatedOrNonConsolidatedAxis',
            'jppfs_cor:NonConsolidatedMember',
            'jpcrp_cor:BusinessResultsOfReportingCompanyLineItems',
            'jpcrp_cor:NetSalesSummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue2SummaryOfBusinessResults',
            'jpcrp_cor:GrossOperatingRevenueSummaryOfBusinessResults',
            'jpcrp_cor:OrdinaryIncomeSummaryOfBusinessResults',
            'jpcrp_cor:NetPremiumsWrittenSummaryOfBusinessResultsINS',
            'jpcrp_cor:OrdinaryIncomeLossSummaryOfBusinessResults',
            'jpcrp_cor:NetIncomeLossSummaryOfBusinessResults',
            'jpcrp_cor:NetLossRatioSummaryOfBusinessResultsINS',
            'jpcrp_cor:NetOperatingExpenseRatioSummaryOfBusinessResultsINS',
            'jpcrp_cor:InterestAndDividendIncomeSummaryOfBusinessResultsINS',
            'jpcrp_cor:InvestmentAssetsYieldIncomeYieldSummaryOfBusinessResultsINS',
            'jpcrp_cor:InvestmentYieldRealizedYieldSummaryOfBusinessResultsINS',
            'jpcrp_cor:EquityInEarningsLossesOfAffiliatesIfEquityMethodIsAppliedSummaryOfBusinessResults',
            'jpcrp_cor:CapitalStockSummaryOfBusinessResults',
            'jpcrp_cor:TotalNumberOfIssuedSharesSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsSummaryOfBusinessResults',
            'jpcrp_cor:DepositsSummaryOfBusinessResults',
            'jpcrp_cor:LoansAndBillsDiscountedSummaryOfBusinessResults',
            'jpcrp_cor:SecuritiesSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:DividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:InterimDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:FirstQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:SecondQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:ThirdQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:FourthQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:FifthQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioInternationalStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioBISStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandard2SummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquitySummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioSummaryOfBusinessResults',
            'jpcrp_cor:PayoutRatioSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInOperatingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInInvestingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInFinancingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsSummaryOfBusinessResults',
            'jpcrp_cor:NumberOfEmployees',
            'jpcrp_cor:AverageNumberOfTemporaryWorkers'
        ]

    def get_all_records(self):
        for document in self.collection.find():
            print(document)

    def get_codes(self):
        return self.collection.find({},{"code":1,"jpcrp_cor:CompanyNameInEnglishCoverPage":1,"jpcrp_cor:NetSalesSummaryOfBusinessResults":1})


class MongoDBControllerJpcrp040300(MongoDBConnector,MongoDBCommonModule ):
    '''
    企業内容等の開示に関する内閣府令 第四号の三様式 四半期報告書  (jpcrp040300-qsr)
    '''

    def __init__(self):
        # noinspection PyUnresolvedReferences
        MongoDBConnector.__init__(self)
        self.collection = self.db['jpcrp040300']

        self.target_element = [
            'jpdei_cor:EDINETCodeDEI',
            'jpdei_cor:FundCodeDEI',
            'jpdei_cor:SecurityCodeDEI',
            'jpdei_cor:FundNameInJapaneseDEI',
            'jpdei_cor:FundNameInEnglishDEI',
            'jpdei_cor:IndustryCodeWhenConsolidatedFinancialStatementsArePreparedInAccordanceWithIndustrySpecificRegulationsDEI',
            'jpdei_cor:IndustryCodeWhenFinancialStatementsArePreparedInAccordanceWithIndustrySpecificRegulationsDEI',
            'jpdei_cor:CurrentFiscalYearStartDateDEI',
            'jpdei_cor:CurrentPeriodEndDateDEI',
            'jpdei_cor:TypeOfCurrentPeriodDEI',
            'jpdei_cor:CurrentFiscalYearEndDateDEI',
            'jpdei_cor:WhetherConsolidatedFinancialStatementsArePreparedDEI',
            'jpdei_cor:AccountingStandardsDEI',
            'jpcrp_cor:CoverPageHeading',
            'jpcrp_cor:DocumentTitleCoverPage',
            'jpcrp_cor:ClauseOfStipulationCoverPage',
            'jpcrp_cor:PlaceOfFilingCoverPage',
            'jpcrp_cor:FilingDateCoverPage',
            'jpcrp_cor:QuarterlyAccountingPeriodCoverPage',
            'jpcrp_cor:CompanyNameCoverPage',
            'jpcrp_cor:CompanyNameInEnglishCoverPage',
            'jpcrp_cor:TitleAndNameOfRepresentativeCoverPage',
            'jpcrp_cor:AddressOfRegisteredHeadquarterCoverPage',
            'jpcrp_cor:TelephoneNumberAddressOfRegisteredHeadquarterCoverPage',
            'jpcrp_cor:NameOfContactPersonAddressOfRegisteredHeadquarterCoverPage',
            'jpcrp_cor:NearestPlaceOfContactCoverPage',
            'jpcrp_cor:TelephoneNumberNearestPlaceOfContactCoverPage',
            'jpcrp_cor:NameOfContactPersonNearestPlaceOfContactCoverPage',
            'jpcrp_cor:PlaceForPublicInspectionCoverPageTextBlock',
            'jpcrp_cor:PlaceForPublicInspectionCoverPageNA',
            'jpcrp_cor:BusinessResultsOfGroupHeading',
            'jpcrp_cor:BusinessResultsOfGroupTable',
            'jppfs_cor:ConsolidatedOrNonConsolidatedAxis',
            'jppfs_cor:ConsolidatedMember',
            'jpcrp_cor:BusinessResultsOfGroupLineItems',
            'jpcrp_cor:NetSalesSummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue2SummaryOfBusinessResults',
            'jpcrp_cor:GrossOperatingRevenueSummaryOfBusinessResults',
            'jpcrp_cor:OrdinaryIncomeSummaryOfBusinessResults',
            'jpcrp_cor:NetPremiumsWrittenSummaryOfBusinessResultsINS',
            'jpcrp_cor:OrdinaryIncomeLossSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossAttributableToOwnersOfParentSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioInternationalStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioBISStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandard2SummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquitySummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInOperatingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInInvestingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInFinancingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsSummaryOfBusinessResults',
            'jpcrp_cor:NumberOfEmployees',
            'jpcrp_cor:AverageNumberOfTemporaryWorkers',
            'jpcrp_cor:RevenueIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossBeforeTaxIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossFromContinuingOperationsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossAttributableToOwnersOfParentIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeAttributableToOwnersOfParentIFRSSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentIFRSSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioIFRSSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareIFRSSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsLossPerShareIFRSSummaryOfBusinessResults',
            'jpcrp_cor:RatioOfOwnersEquityToGrossAssetsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquityIFRSSummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:RevenueJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossBeforeTaxJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossFromContinuingOperationsJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossAttributableToOwnersOfParentJMISSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeJMISSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeAttributableToOwnersOfParentJMISSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentJMISSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsJMISSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioJMISSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareJMISSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsLossPerShareJMISSummaryOfBusinessResults',
            'jpcrp_cor:RatioOfOwnersEquityToGrossAssetsJMISSummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquityJMISSummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsJMISSummaryOfBusinessResults',
            'jpcrp_cor:RevenuesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:OperatingIncomeLossUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossBeforeTaxUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:NetIncomeLossAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityIncludingPortionAttributableToNonControllingInterestUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentPerShareUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsLossPerShareUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquityUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:BusinessResultsOfReportingCompanyHeading',
            'jpcrp_cor:BusinessResultsOfReportingCompanyTable',
            'jppfs_cor:ConsolidatedOrNonConsolidatedAxis',
            'jppfs_cor:NonConsolidatedMember',
            'jpcrp_cor:BusinessResultsOfReportingCompanyLineItems',
            'jpcrp_cor:NetSalesSummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue2SummaryOfBusinessResults',
            'jpcrp_cor:GrossOperatingRevenueSummaryOfBusinessResults',
            'jpcrp_cor:OrdinaryIncomeSummaryOfBusinessResults',
            'jpcrp_cor:NetPremiumsWrittenSummaryOfBusinessResultsINS',
            'jpcrp_cor:OrdinaryIncomeLossSummaryOfBusinessResults',
            'jpcrp_cor:NetIncomeLossSummaryOfBusinessResults',
            'jpcrp_cor:NetLossRatioSummaryOfBusinessResultsINS',
            'jpcrp_cor:NetOperatingExpenseRatioSummaryOfBusinessResultsINS',
            'jpcrp_cor:InterestAndDividendIncomeSummaryOfBusinessResultsINS',
            'jpcrp_cor:InvestmentAssetsYieldIncomeYieldSummaryOfBusinessResultsINS',
            'jpcrp_cor:InvestmentYieldRealizedYieldSummaryOfBusinessResultsINS',
            'jpcrp_cor:EquityInEarningsLossesOfAffiliatesIfEquityMethodIsAppliedSummaryOfBusinessResults',
            'jpcrp_cor:CapitalStockSummaryOfBusinessResults',
            'jpcrp_cor:TotalNumberOfIssuedSharesSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsSummaryOfBusinessResults',
            'jpcrp_cor:DepositsSummaryOfBusinessResults',
            'jpcrp_cor:LoansAndBillsDiscountedSummaryOfBusinessResults',
            'jpcrp_cor:SecuritiesSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:DividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:InterimDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:FirstQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:SecondQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:ThirdQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:FourthQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:FifthQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioInternationalStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioBISStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandard2SummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquitySummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioSummaryOfBusinessResults',
            'jpcrp_cor:PayoutRatioSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInOperatingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInInvestingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInFinancingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsSummaryOfBusinessResults',
            'jpcrp_cor:NumberOfEmployees',
            'jpcrp_cor:AverageNumberOfTemporaryWorkers'

        ]

    def get_all_records(self):
        for document in self.collection.find():
            print(document)

    def get_codes(self):
        return self.collection.find({},{"code":1,"jpcrp_cor:CompanyNameInEnglishCoverPage":1,"jpcrp_cor:NetSalesSummaryOfBusinessResults":1})


class MongoDBControllerJpcrp050000(MongoDBConnector,MongoDBCommonModule ):
    '''
    企業内容等の開示に関する内閣府令 第五号様式 半期報告書  (jpcrp050000-ssr)
    '''

    def __init__(self):
        # noinspection PyUnresolvedReferences
        MongoDBConnector.__init__(self)
        self.collection = self.db['jpcrp050000']

        self.target_element = [
            'jpdei_cor:EDINETCodeDEI',
            'jpdei_cor:FundCodeDEI',
            'jpdei_cor:SecurityCodeDEI',
            'jpdei_cor:FundNameInJapaneseDEI',
            'jpdei_cor:FundNameInEnglishDEI',
            'jpdei_cor:IndustryCodeWhenConsolidatedFinancialStatementsArePreparedInAccordanceWithIndustrySpecificRegulationsDEI',
            'jpdei_cor:IndustryCodeWhenFinancialStatementsArePreparedInAccordanceWithIndustrySpecificRegulationsDEI',
            'jpdei_cor:CurrentFiscalYearStartDateDEI',
            'jpdei_cor:CurrentPeriodEndDateDEI',
            'jpdei_cor:TypeOfCurrentPeriodDEI',
            'jpdei_cor:CurrentFiscalYearEndDateDEI',
            'jpdei_cor:WhetherConsolidatedFinancialStatementsArePreparedDEI',
            'jpdei_cor:AccountingStandardsDEI',
            'jpcrp_cor:CoverPageHeading',
            'jpcrp_cor:DocumentTitleCoverPage',
            'jpcrp_cor:PlaceOfFilingCoverPage',
            'jpcrp_cor:FilingDateCoverPage',
            'jpcrp_cor:SemiAnnualAccountingPeriodCoverPage',
            'jpcrp_cor:CompanyNameCoverPage',
            'jpcrp_cor:CompanyNameInEnglishCoverPage',
            'jpcrp_cor:TitleAndNameOfRepresentativeCoverPage',
            'jpcrp_cor:AddressOfRegisteredHeadquarterCoverPage',
            'jpcrp_cor:TelephoneNumberAddressOfRegisteredHeadquarterCoverPage',
            'jpcrp_cor:NameOfContactPersonAddressOfRegisteredHeadquarterCoverPage',
            'jpcrp_cor:NearestPlaceOfContactCoverPage',
            'jpcrp_cor:TelephoneNumberNearestPlaceOfContactCoverPage',
            'jpcrp_cor:NameOfContactPersonNearestPlaceOfContactCoverPage',
            'jpcrp_cor:PlaceForPublicInspectionCoverPageTextBlock',
            'jpcrp_cor:PlaceForPublicInspectionCoverPageNA',
            'jpcrp_cor:BusinessResultsOfGroupHeading',
            'jpcrp_cor:BusinessResultsOfGroupTable',
            'jppfs_cor:ConsolidatedOrNonConsolidatedAxis',
            'jppfs_cor:ConsolidatedMember',
            'jpcrp_cor:BusinessResultsOfGroupLineItems',
            'jpcrp_cor:NetSalesSummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue2SummaryOfBusinessResults',
            'jpcrp_cor:GrossOperatingRevenueSummaryOfBusinessResults',
            'jpcrp_cor:OrdinaryIncomeSummaryOfBusinessResults',
            'jpcrp_cor:NetPremiumsWrittenSummaryOfBusinessResultsINS',
            'jpcrp_cor:OrdinaryIncomeLossSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossAttributableToOwnersOfParentSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioInternationalStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioBISStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandard2SummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquitySummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInOperatingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInInvestingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInFinancingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsSummaryOfBusinessResults',
            'jpcrp_cor:NumberOfEmployees',
            'jpcrp_cor:AverageNumberOfTemporaryWorkers',
            'jpcrp_cor:RevenueIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossBeforeTaxIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossFromContinuingOperationsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossAttributableToOwnersOfParentIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeAttributableToOwnersOfParentIFRSSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentIFRSSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioIFRSSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareIFRSSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsLossPerShareIFRSSummaryOfBusinessResults',
            'jpcrp_cor:RatioOfOwnersEquityToGrossAssetsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquityIFRSSummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:RevenueJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossBeforeTaxJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossFromContinuingOperationsJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossAttributableToOwnersOfParentJMISSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeJMISSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeAttributableToOwnersOfParentJMISSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentJMISSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsJMISSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioJMISSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareJMISSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsLossPerShareJMISSummaryOfBusinessResults',
            'jpcrp_cor:RatioOfOwnersEquityToGrossAssetsJMISSummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquityJMISSummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsJMISSummaryOfBusinessResults',
            'jpcrp_cor:RevenuesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:OperatingIncomeLossUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossBeforeTaxUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:NetIncomeLossAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityIncludingPortionAttributableToNonControllingInterestUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentPerShareUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsLossPerShareUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquityUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:BusinessResultsOfReportingCompanyHeading',
            'jpcrp_cor:BusinessResultsOfReportingCompanyTable',
            'jppfs_cor:ConsolidatedOrNonConsolidatedAxis',
            'jppfs_cor:NonConsolidatedMember',
            'jpcrp_cor:BusinessResultsOfReportingCompanyLineItems',
            'jpcrp_cor:NetSalesSummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue2SummaryOfBusinessResults',
            'jpcrp_cor:GrossOperatingRevenueSummaryOfBusinessResults',
            'jpcrp_cor:OrdinaryIncomeSummaryOfBusinessResults',
            'jpcrp_cor:NetPremiumsWrittenSummaryOfBusinessResultsINS',
            'jpcrp_cor:OrdinaryIncomeLossSummaryOfBusinessResults',
            'jpcrp_cor:NetIncomeLossSummaryOfBusinessResults',
            'jpcrp_cor:NetLossRatioSummaryOfBusinessResultsINS',
            'jpcrp_cor:NetOperatingExpenseRatioSummaryOfBusinessResultsINS',
            'jpcrp_cor:InterestAndDividendIncomeSummaryOfBusinessResultsINS',
            'jpcrp_cor:InvestmentAssetsYieldIncomeYieldSummaryOfBusinessResultsINS',
            'jpcrp_cor:InvestmentYieldRealizedYieldSummaryOfBusinessResultsINS',
            'jpcrp_cor:EquityInEarningsLossesOfAffiliatesIfEquityMethodIsAppliedSummaryOfBusinessResults',
            'jpcrp_cor:CapitalStockSummaryOfBusinessResults',
            'jpcrp_cor:TotalNumberOfIssuedSharesSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsSummaryOfBusinessResults',
            'jpcrp_cor:DepositsSummaryOfBusinessResults',
            'jpcrp_cor:LoansAndBillsDiscountedSummaryOfBusinessResults',
            'jpcrp_cor:SecuritiesSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:DividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:InterimDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:FirstQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:SecondQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:ThirdQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:FourthQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:FifthQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioInternationalStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioBISStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandard2SummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquitySummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioSummaryOfBusinessResults',
            'jpcrp_cor:PayoutRatioSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInOperatingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInInvestingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInFinancingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsSummaryOfBusinessResults',
            'jpcrp_cor:NumberOfEmployees',
            'jpcrp_cor:AverageNumberOfTemporaryWorkers'
        ]

    def get_all_records(self):
        for document in self.collection.find():
            print(document)

    def get_codes(self):
        return self.collection.find({},{"code":1,"jpcrp_cor:CompanyNameInEnglishCoverPage":1,"jpcrp_cor:NetSalesSummaryOfBusinessResults":1})


class MongoDBControllerJpcrp050200(MongoDBConnector,MongoDBCommonModule ):
    '''
    企業内容等の開示に関する内閣府令 第五号の二様式 半期報告書  (jpcrp050200-ssr)
    '''

    def __init__(self):
        # noinspection PyUnresolvedReferences
        MongoDBConnector.__init__(self)
        self.collection = self.db['jpcrp050200']

        self.target_element = [
            'jpdei_cor:EDINETCodeDEI',
            'jpdei_cor:FundCodeDEI',
            'jpdei_cor:SecurityCodeDEI',
            'jpdei_cor:FundNameInJapaneseDEI',
            'jpdei_cor:FundNameInEnglishDEI',
            'jpdei_cor:IndustryCodeWhenConsolidatedFinancialStatementsArePreparedInAccordanceWithIndustrySpecificRegulationsDEI',
            'jpdei_cor:IndustryCodeWhenFinancialStatementsArePreparedInAccordanceWithIndustrySpecificRegulationsDEI',
            'jpdei_cor:CurrentFiscalYearStartDateDEI',
            'jpdei_cor:CurrentPeriodEndDateDEI',
            'jpdei_cor:TypeOfCurrentPeriodDEI',
            'jpdei_cor:CurrentFiscalYearEndDateDEI',
            'jpdei_cor:WhetherConsolidatedFinancialStatementsArePreparedDEI',
            'jpdei_cor:AccountingStandardsDEI',
            'jpcrp_cor:CoverPageHeading',
            'jpcrp_cor:DocumentTitleCoverPage',
            'jpcrp_cor:PlaceOfFilingCoverPage',
            'jpcrp_cor:FilingDateCoverPage',
            'jpcrp_cor:SemiAnnualAccountingPeriodCoverPage',
            'jpcrp_cor:CompanyNameCoverPage',
            'jpcrp_cor:CompanyNameInEnglishCoverPage',
            'jpcrp_cor:TitleAndNameOfRepresentativeCoverPage',
            'jpcrp_cor:AddressOfRegisteredHeadquarterCoverPage',
            'jpcrp_cor:TelephoneNumberAddressOfRegisteredHeadquarterCoverPage',
            'jpcrp_cor:NameOfContactPersonAddressOfRegisteredHeadquarterCoverPage',
            'jpcrp_cor:NearestPlaceOfContactCoverPage',
            'jpcrp_cor:TelephoneNumberNearestPlaceOfContactCoverPage',
            'jpcrp_cor:NameOfContactPersonNearestPlaceOfContactCoverPage',
            'jpcrp_cor:PlaceForPublicInspectionCoverPageTextBlock',
            'jpcrp_cor:PlaceForPublicInspectionCoverPageNA',
            'jpcrp_cor:BusinessResultsOfGroupHeading',
            'jpcrp_cor:BusinessResultsOfGroupTable',
            'jppfs_cor:ConsolidatedOrNonConsolidatedAxis',
            'jppfs_cor:ConsolidatedMember',
            'jpcrp_cor:BusinessResultsOfGroupLineItems',
            'jpcrp_cor:NetSalesSummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue2SummaryOfBusinessResults',
            'jpcrp_cor:GrossOperatingRevenueSummaryOfBusinessResults',
            'jpcrp_cor:OrdinaryIncomeSummaryOfBusinessResults',
            'jpcrp_cor:NetPremiumsWrittenSummaryOfBusinessResultsINS',
            'jpcrp_cor:OrdinaryIncomeLossSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossAttributableToOwnersOfParentSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioInternationalStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioBISStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandard2SummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquitySummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInOperatingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInInvestingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInFinancingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsSummaryOfBusinessResults',
            'jpcrp_cor:NumberOfEmployees',
            'jpcrp_cor:AverageNumberOfTemporaryWorkers',
            'jpcrp_cor:RevenueIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossBeforeTaxIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossFromContinuingOperationsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossAttributableToOwnersOfParentIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeIFRSSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeAttributableToOwnersOfParentIFRSSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentIFRSSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioIFRSSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareIFRSSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsLossPerShareIFRSSummaryOfBusinessResults',
            'jpcrp_cor:RatioOfOwnersEquityToGrossAssetsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquityIFRSSummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesIFRSSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsIFRSSummaryOfBusinessResults',
            'jpcrp_cor:RevenueJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossBeforeTaxJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossFromContinuingOperationsJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossJMISSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossAttributableToOwnersOfParentJMISSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeJMISSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeAttributableToOwnersOfParentJMISSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentJMISSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsJMISSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioJMISSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareJMISSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsLossPerShareJMISSummaryOfBusinessResults',
            'jpcrp_cor:RatioOfOwnersEquityToGrossAssetsJMISSummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquityJMISSummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesJMISSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsJMISSummaryOfBusinessResults',
            'jpcrp_cor:RevenuesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:OperatingIncomeLossUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:ProfitLossBeforeTaxUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:NetIncomeLossAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:ComprehensiveIncomeAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityIncludingPortionAttributableToNonControllingInterestUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityAttributableToOwnersOfParentPerShareUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsLossPerShareUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquityUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsUSGAAPSummaryOfBusinessResults',
            'jpcrp_cor:BusinessResultsOfReportingCompanyHeading',
            'jpcrp_cor:BusinessResultsOfReportingCompanyTable',
            'jppfs_cor:ConsolidatedOrNonConsolidatedAxis',
            'jppfs_cor:NonConsolidatedMember',
            'jpcrp_cor:BusinessResultsOfReportingCompanyLineItems',
            'jpcrp_cor:NetSalesSummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults',
            'jpcrp_cor:OperatingRevenue2SummaryOfBusinessResults',
            'jpcrp_cor:GrossOperatingRevenueSummaryOfBusinessResults',
            'jpcrp_cor:OrdinaryIncomeSummaryOfBusinessResults',
            'jpcrp_cor:NetPremiumsWrittenSummaryOfBusinessResultsINS',
            'jpcrp_cor:OrdinaryIncomeLossSummaryOfBusinessResults',
            'jpcrp_cor:NetIncomeLossSummaryOfBusinessResults',
            'jpcrp_cor:NetLossRatioSummaryOfBusinessResultsINS',
            'jpcrp_cor:NetOperatingExpenseRatioSummaryOfBusinessResultsINS',
            'jpcrp_cor:InterestAndDividendIncomeSummaryOfBusinessResultsINS',
            'jpcrp_cor:InvestmentAssetsYieldIncomeYieldSummaryOfBusinessResultsINS',
            'jpcrp_cor:InvestmentYieldRealizedYieldSummaryOfBusinessResultsINS',
            'jpcrp_cor:EquityInEarningsLossesOfAffiliatesIfEquityMethodIsAppliedSummaryOfBusinessResults',
            'jpcrp_cor:CapitalStockSummaryOfBusinessResults',
            'jpcrp_cor:TotalNumberOfIssuedSharesSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsSummaryOfBusinessResults',
            'jpcrp_cor:TotalAssetsSummaryOfBusinessResults',
            'jpcrp_cor:DepositsSummaryOfBusinessResults',
            'jpcrp_cor:LoansAndBillsDiscountedSummaryOfBusinessResults',
            'jpcrp_cor:SecuritiesSummaryOfBusinessResults',
            'jpcrp_cor:NetAssetsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:DividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:InterimDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:FirstQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:SecondQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:ThirdQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:FourthQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:FifthQuarterDividendPaidPerShareSummaryOfBusinessResults',
            'jpcrp_cor:BasicEarningsLossPerShareSummaryOfBusinessResults',
            'jpcrp_cor:DilutedEarningsPerShareSummaryOfBusinessResults',
            'jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioInternationalStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioBISStandardSummaryOfBusinessResults',
            'jpcrp_cor:CapitalAdequacyRatioDomesticStandard2SummaryOfBusinessResults',
            'jpcrp_cor:RateOfReturnOnEquitySummaryOfBusinessResults',
            'jpcrp_cor:PriceEarningsRatioSummaryOfBusinessResults',
            'jpcrp_cor:PayoutRatioSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInOperatingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInInvestingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:NetCashProvidedByUsedInFinancingActivitiesSummaryOfBusinessResults',
            'jpcrp_cor:CashAndCashEquivalentsSummaryOfBusinessResults',
            'jpcrp_cor:NumberOfEmployees',
            'jpcrp_cor:AverageNumberOfTemporaryWorkers'
        ]

    def get_all_records(self):
        for document in self.collection.find():
            print(document)

    def get_codes(self):
        return self.collection.find({},{"code":1,"jpcrp_cor:CompanyNameInEnglishCoverPage":1,"jpcrp_cor:NetSalesSummaryOfBusinessResults":1})
