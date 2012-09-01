import requests
from BeautifulSoup import BeautifulSoup

def count_medals():
    """
        scrape wikipedia and pull in tabular data
        on medals by country by year
    """

    years = [1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008]
    f = open('log.txt', 'w')
    
    for year in years:
        heading = "\n\n----------------\n Medals for %s \n----------------\n\n" % str(year)
        f.write(heading)
        print heading
        
        r = requests.get("http://en.wikipedia.org/wiki/%s_Summer_Olympics_medal_table" % str(year))
        soup = BeautifulSoup(r.text)
        
        if year == 2008 or year == 2012:
            medal_table = soup.findAll("table", "wikitable")[1]
        else:
            medal_table = soup.find("table", "wikitable")
        
        rows = medal_table.findAll("tr")
        
        total_medals = 0
        total_gold = 0
        
        for row in rows[1:-1]:
            country, gold, total = parse_row(year, row)
            total_medals += int(total)
            total_gold += int(gold)
            try:
                f.write("%(country)s \t\t %(gold)s \t\t %(total)s \n" % locals())
            except:
                continue
        f.write("Total Medals: %s \t Total Golds: %s \n" % (total_medals, total_gold))    
    f.close()
                
def parse_row(year, row):

    cells = row.findAll("td")
        
    if year == 1984:
        country = row.find("th").contents[2].string
        gold = cells[-4].string
        silver = cells[-3].string
        bronze = cells[-2].string
        total = cells[-1].string
        return country, gold, total
        
    else:
        country = cells[-5].contents[2].string
        gold = cells[-4].string
        silver = cells[-3].string
        bronze = cells[-2].string
        total = cells[-1].string
        
        if total == None:
            total = cells[-1].contents[0] # correction for cells that have inline citations
        return country, gold, total

def sort_data():
    """
        take a tab-deliniated sheet of countries 
        and medal counts, sorted by year, and turn it 
        into data sorted by country over time.
    """
    
    countries = {}
    f = open('log.txt', 'r')
    for line in f:
        data = line.strip('\n').split('\t')
        year = data[0]
        country_name = data[1].strip()
        gold_count = data[2]
        gold_pct = data[3]
        total_count = data[4]
        total_pct = data[5]
        
        if country_name == "":
            continue
        
        countries_dict = countries.setdefault(country_name, {})
        countries_dict[year] = {
            #'gold_count': gold_count,
            'gold_pct': gold_pct,
            #'total_count': total_count,
            'total_pct': total_pct
        }
    
    f.close()
    
    # trim countries that don't appear every year
    for country in countries:
        if len(countries[country]) < 6:
            countries[country] = None
    
    # add in GDP data    
    h = open('log3.txt', 'r')
    for line in h:
        data = line.split("\t")
        country_name = data[0]
        eighty_total = data[1]
        eighty_pct = data[2]
        eighty_four_total = data[3]
        eighty_four_pct = data[4]
        eighty_eight_total = data[5]
        eighty_eight_pct = data[6]
        ninty_two_total = data[7]
        ninty_two_pct = data[8]
        ninty_six_total = data[9]
        ninty_six_pct = data[10]
        thousand_total = data[11]
        thousand_pct = data[12]
        thousand_four_total = data[13]
        thousand_four_pct = data[14]
        thousand_eight_total = data[15]
        thousand_eight_pct = data[16]
        
        if countries.get(country_name):
            if countries[country_name].get('1980'):
                #print "adding 1980 GDP data to %s" % country_name
                #countries[country_name]['1980']['gdp_total'] = eighty_total
                countries[country_name]['1980']['gdp_pct'] = eighty_pct
            if countries[country_name].get('1984'):
                #print "adding 1984 GDP data to %s" % country_name
                #countries[country_name]['1984']['gdp_total'] = eighty_four_total
                countries[country_name]['1984']['gdp_pct'] = eighty_four_pct
            if countries[country_name].get('1988'):
                #print "adding 1988 GDP data to %s" % country_name
                #countries[country_name]['1988']['gdp_total'] = eighty_eight_total
                countries[country_name]['1988']['gdp_pct'] = eighty_eight_pct
            if countries[country_name].get('1992'):
                #print "adding 1992 GDP data to %s" % country_name
                #countries[country_name]['1992']['gdp_total'] = ninty_two_total
                countries[country_name]['1992']['gdp_pct'] = ninty_two_pct
            if countries[country_name].get('1996'):
                #print "adding 1996 GDP data to %s" % country_name
                #countries[country_name]['1996']['gdp_total'] = ninty_six_total
                countries[country_name]['1996']['gdp_pct'] = ninty_six_pct
            if countries[country_name].get('2000'):
                #print "adding 2000 GDP data to %s" % country_name
                #countries[country_name]['2000']['gdp_total'] = thousand_total
                countries[country_name]['2000']['gdp_pct'] = thousand_pct
            if countries[country_name].get('2004'):
                #print "adding 2004 GDP data to %s" % country_name
                #countries[country_name]['2004']['gdp_total'] = thousand_four_total
                countries[country_name]['2004']['gdp_pct'] = thousand_four_pct
            if countries[country_name].get('2008'):
                #print "adding 2008 GDP data to %s" % country_name
                #countries[country_name]['2008']['gdp_total'] = thousand_eight_total
                countries[country_name]['2008']['gdp_pct'] = thousand_eight_pct
            
    
    g = open('log2.txt', 'w')
    g.write( str(countries) )
    g.close()
    
    final_country_list = [country for country, dict in countries.items() if dict]
    print final_country_list
    
    prepare_for_graphing(final_country_list, countries)
    
def prepare_for_graphing(list, data):
    
    i = open('log4.txt', 'w')
    for country in list:
        print "preparing %s data for graphing" % country
        years = sorted( data[country].keys() )
        print years
        i.write('%s\n' % country)
        i.write('Years:')
        for year in years:
            try:
                i.write('\t%s' % str(year))
            except:
                i.write('\t ')
        i.write('\n')
        
        i.write('Total Pct:')
        for year in years:
            try:
                i.write('\t%s' % data[country][year]['total_pct'])
            except: 
                i.write('\t ')
        i.write('\n')   
        
        i.write('Gold Pct:')
        for year in years:
            try:
                i.write('\t%s' % data[country][year]['gold_pct'])
            except:
                i.write('\t ')
        i.write('\n')    
        
        i.write('GDP Pct:')
        for year in years:
            try:
                i.write('\t%s' % data[country][year]['gdp_pct'])
            except:
                i.write('\t ')
        i.write('\n\n')
    
    i.close()
    
if __name__ == "__main__":
    #count_medals()
    sort_data()