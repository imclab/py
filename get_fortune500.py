import logging
logger = logging.getLogger(__name__)

from BeautifulSoup import BeautifulSoup
import requests
import json as json
import time

def main(data=None):

    if data == None:
        company_names = get_company_names()
        company_urls = map(get_url_for_company_name, company_names)
        company_mg_score = map(get_mg_score_for_url, company_urls)
        ranking = range(1, len(company_names)+1)

        final_data = zip(ranking, company_names, company_urls, company_mg_score)
        print final_data
    else:
        final_data = data

    f = open("results.log", "w")
    for datum in final_data:
        line_format = "%s. \t%s\t%s\t%s\n" % (datum[0], datum[1], datum[2], datum[3])
        f.write(line_format)
    f.close()

def get_company_names(limit=100):
    """ return a list of all the fortune 500 fastest growing comapnies """ 
    print "GETTING LIST OF COMPANY NAMES"
    company_names = []

    r = requests.get("http://www.inc.com/inc5000/list/2012/400//")
    soup = BeautifulSoup(r.text)
    table = soup.find(id="fulltable")
    rows = soup.findAll("tr")[2:] # skip the first 2 rows, which are headers

    for row in rows[:limit]:
        name_cell = row.findAll("td")[1] # company names are in the second col
        name_str  = name_cell.a.string
        print "adding %s" % name_str
        company_names.append(name_str)

    return company_names

def get_url_for_company_name(company_name):
    """ lookup URL for a company using fortune's profile on the company """

    company_name_slug = company_name.lower().replace("& ", "").replace(".", "").replace(",", "").replace(" ", "-") # hacks to change pretty company name to slug
    company_profile_url = "http://www.inc.com/inc5000/profile/%s" % company_name_slug
    print "getting url from %s" % (company_profile_url)

    r = requests.get(company_profile_url)
    soup = BeautifulSoup(r.text)

    detail_section = soup.find("div", "companydetail")
    try:
        return detail_section.find("a")["href"]
    except:
        return None

def get_mg_score_for_url(url):
    """ take a URL and return the overall marketing grader score """
    if url == None:
        return "no url to lookup"

    print "getting mg score for %s" % (url)

    hostname = url.split("://")[1] # remove the protocol from the url
    init_url = "http://marketing.grader.com/report/init/%s" % hostname

    try:
        init = requests.get(init_url)
        response_json = json.loads(init.text)
        report_guid = response_json["report"]["guid"]
    except:
        return "error initing MG report"

    while True:
        partial_url = "http://marketing.grader.com/report/partial/%s" % (report_guid)
        partial = requests.get(partial_url)
        print "fetching partial: %s" % partial_url

        response_json = json.loads(partial.text)
        if response_json["success"] == True and response_json["report"]["finished"]:
            return response_json["report"]["finalGrade"]
        else:
            time.sleep(1) # wait and try polling the API again
            print "not ready yet, trying again"

def crunch_compiled_results(file_name):
    with open(file_name, "r") as f:
        pass


if __name__ == "__main__":
    # data = [(1, u'MSi SSL', u'http://MSiSSL.com', 50), (2, u'DefySupply.com', u'http://www.DefySupply.com', 73), (3, u'Advanced Chemical Concepts', u'http://AdvancedChemicalConcepts.com', 38), (4, u'ScribeAmerica', u'http://www.ScribeAmerica.com', 44), (5, u'Smashburger', u'http://www.Smashburger.com', 73), (6, u'Gnarus Advisors', u'http://www.GnarusLLC.com', 55), (7, u'Iconic Development', u'http://www.IconicDevelopment.com', 10), (8, u'Slate Rock Safety', u'http://SlateRockSafety.com', 28), (9, u'Triad Semiconductor', u'http://www.TriadSemi.com', 36), (10, u'DreamBrands', u'http://www.DreamBrands.com', 49), (11, u'NW Auto Recyclers', u'http://NWAutoRecyclers.com', 28), (12, u'WealthClasses', u'http://WealthClasses.com', 65), (13, u'Consumer United', u'http://www.ConsumerUnited.com', 38), (14, u'Wound Care Advantage', u'http://WoundCareAdvantage.com', 38), (15, u'Braintree', u'http://www.BraintreePayments.com', 65), (16, u'Medicare.com', u'http://www.Medicare.com', 47), (17, u'Star2Star Communications', u'http://www.star2star.com', 26), (18, u'ChaiONE', u'http://www.ChaiONE.com', 76), (19, u'Prudent Infotech', u'http://PrudentItInc.com', 7), (20, u'One Source Networks', u'http://OneSourceNetworks.com', 28), (21, u'USP&E; Global', None, 'no url to lookup'), (22, u'Shockoe Commerce', u'http://www.ShockoeCommerce.com', 27), (23, u'Deluxe Marketing', u'http://DeluxeMarketingInc.com', 51), (24, u'ShopAtHome.com', u'http://www.ShopAtHome.com', 91), (25, u'MyTicketIn.com', u'http://www.MyTicketIn.com', 47), (26, u'BOS Security', u'http://www.BOSSecurity.com', 17), (27, u'Gilligan & Ferneman', u'http://GilliganAndFerneman.com', 21), (28, u'OmniPoint', u'http://OmniPointInc.com', 47), (29, u'Webmarketing123', u'http://Webmarketing123.com', 87), (30, u'JESS3', u'http://www.Jess3.com', 88), (31, u'Renewable Energy Group', None, 'no url to lookup'), (32, u'Paragon Micro', u'http://ParagonMicro.com', 21), (33, u'Insurance Care Direct', u'http://www.InsuranceCareDirect.com', 57), (34, u'Acumen', u'http://www.ProjectAcumen.com', 82), (35, u'EarthLED.com', u'http://www.EarthLED.com', 46), (36, u'Three Pillar Global', u'http://www.ThreePillarGlobal.com', 78), (37, u'Launchpad Advertising', u'http://LPNYC.com', 64), (38, u'Graybach', u'http://www.Graybach.com', 62), (39, u'Standard Solar', u'http://www.standardsolar.com', 77), (40, u'FM Facility Maintenance', u'http://www.FMFacilityMaintenance.com', 27), (41, u'Global Telesourcing', u'http://www.GlobalTelesourcing.com', 11), (42, u'Utopia', u'http://UtopiaInc.com', 88), (43, u'Elicere', u'http://www.Elicere.com', 47), (44, u'Old Town IT', u'http://www.OldTownIT.com', 45), (45, u'StanSource', u'http://www.StanSource.com', 5), (46, u'Rise Interactive', u'http://www.RiseInteractive.com', 87), (47, u'Varrow', u'http://www.Varrow.com', 80), (48, u'R2 Unified Technologies', u'http://www.R2UT.com', 39), (49, u'Infosemantics', u'http://www.Infosemantics.com', 37), (50, u'PrizeLogic', u'http://PrizeLogic.com', 35), (51, u'Sonatype', u'http://www.Sonatype.com', 58), (52, u'Integrity Express Logistics', u'http://www.Intxlog.com', 38), (53, u'CLEAResult', u'http://www.CLEAResult.com', 38), (54, u'Petticoat-Schmitt Civil Contractors', u'http://www.PetticoatSchmitt.com', 11), (55, u'Erickson Builders', u'http://www.EricksonBCI.com', 26), (56, u'Rhythm Engineering', u'http://www.RhythmTraffic.com', 74), (57, u'FortuneBuilders.com', u'http://www.FortuneBuilders.com', 92), (58, u'YETI Coolers', u'http://YETICoolers.com', 85), (59, u'ProtectCell', u'http://www.ProtectCell.com', 67), (60, u'C2S Technologies', u'http://www.C2STechs.com', 22), (61, u'Intuitive Technology Group', u'http://www.IntuitiveTech.com', 37), (62, u'CFC Print Solutions', u'http://www.CFCPrint.com', 19), (63, u'aimClear', u'http://www.aimClear.com', 88), (64, u'Matrix Energy Services', u'http://www.MatrixESCorp.com', 8), (65, u'Pothos', u'http://www.Pothos.us', 51), (66, u'Ninety Five 5', u'http://www.nf5.com', 36), (67, u'AirWatch', u'http://www.Air-Watch.com', 64), (68, u'A+ Government Solutions', None, 'no url to lookup'), (69, u'Veteran Corps of America', u'http://www.VeteranCorps.com', 15), (70, u'Night Vision Entertainment', u'http://www.NightVisionEnt.com', 23), (71, u'Citywide Restoration', u'http://www.CityWideResto.com', 3), (72, u'ROCS Entry Level Staffing', u'http://www.rocsstaffing.com', 65), (73, u'ASE Direct', u'http://ASEDirect.com', 'error initing MG report'), (74, u'The Pedowitz Group', u'http://PedowitzGroup.com', 70), (75, u'Mobifusion', u'http://www.Mobifusion.com', 12), (76, u'TreeFrog Data Solutions', u'http://www.TreeFrogData.com', 12), (77, u'Cogent Data Solutions', u'http://www.CogentDataSolutions.com', 24), (78, u'Stonegate Mortgage', u'http://www.StonegateMtg.COM', 36), (79, u'WillowTree Apps', u'http://www.WillowTreeApps.com', 73), (80, u'Lulus.com', u'http://Lulus.com', 80), (81, u'MyNaturalMarket', u'http://www.MyNaturalMarket.com/', 59), (82, u'Metalogix', u'http://www.Metalogix.com', 'error initing MG report'), (83, u'RevGen Partners', u'http://www.RevGenPartners.com', 30), (84, u'SNS LOGISTICS', u'http://www.SNS-Logistics.com', 11), (85, u'Teknetex', u'http://www.Teknetex.com', 64), (86, u'QSS International', u'http://www.QSSInternational.com', 43), (87, u'Dean Media Group', u'http://www.DeanMediaGroup.com', 53), (88, u'Summit Learning Services', u'http://www.SummitLearning.net', 29), (89, u'LongView International Technology Solutions', u'http://LongView-inc.com', 33), (90, u'MicroTech', u'http://www.MicroTech.net', 70), (91, u'SEO.com', u'http://www.SEO.com', 74), (92, u'HeadStream', u'http://www.HeadStreamInc.com', 55), (93, u'Sweet Spot Marketing', u'http://www.SweetSpotMarketing.com', 41), (94, u'AA Metals', u'http://www.AAMetals.com', 10), (95, u'OuterBox Solutions', u'http://OuterBoxDesign.com', 58), (96, u'Arteris', u'http://www.Arteris.com', 76), (97, u'CAF Environmental Solutions', u'http://www.myCAF.com', 41), (98, u'Polu Kai Services', u'http://www.PoluKaiServices.com', 36), (99, u'Position Logic', u'http://www.PositionLogic.com', 76), (100, u'MCT Trading', u'http://www.MCT-Trading.com', 29)]
    # main(data)

    # main()

    crunch_compiled_results("results-compiled.log")