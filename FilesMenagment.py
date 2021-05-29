

def OtworzPlik(nazwa):
   try:
      zawartosc = []
      for line in open(nazwa, 'r'):
         zawartosc.append(line.strip("\n"))
      assert zawartosc != [], 'puste odczyt z pliku'
      return zawartosc
   except IOError:
      print('\n \n Błąd otwarcia pliku \n \n')
