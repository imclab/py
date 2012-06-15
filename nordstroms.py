f = open('nordstroms-data.txt', 'r')
g = open('nordstroms-data-2.txt', 'w')

line_num = 0
for line in f:

    try:
        long_url = line.split('\'')[7].strip()
    except IndexError:
        long_url = None
    
    if long_url:
        pieces = line.split(long_url)
        
        if not long_url.find('#') == -1:
            first_frag = long_url.split('#')[0]
            middle_frag = "&page="
            last_frag = long_url.split('&page=')[1]
            
            new_url = first_frag + middle_frag + last_frag
            new_line = pieces[0] + new_url + pieces[1]
            
            g.write(new_line)
            
        else:
            g.write(line)
            
    

f.close()
g.close()