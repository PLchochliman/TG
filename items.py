import excelDigger as excel
#kurwa mamy to
dane = excel.loader('TabelaBroni.xlsx', ['bron', 'bronbiala', 'granaty', 'lunety', 'celowniki'], ['O300', 'I19', 'I10', 'F13', 'G14'])
