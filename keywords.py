def main():
    f = open('F:/Dropbox/web/drobe/drobe/scraper/data.py', 'r')
    
    def get_keyword(line):
        return line.split("'")[5]
        
    keywords = set( [ get_keyword(line) for line in f if "('dresses'," in line ] )
    
    g = open('keywords.log', 'w')
    g.write( "\n".join(keywords) )
    g.close
        

if __name__ == "__main__":
    main()