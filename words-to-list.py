def main():
    w = open('words.txt', 'r')
    list = [ word.strip().lower() for word in w ]
    w.close()
    
    f = open( 'words.list.txt', 'w' )
    f.write( '[' )
    for word in list:
        f.write("'"+word+"', ")
    f.write( ']' )
    f.close
        

if __name__ == "__main__":
    main()