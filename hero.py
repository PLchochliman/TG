import mortal as mortal
import system as system
import excelDigger as excelDigger
import constans as constans

"starting creating real character"


class Postac(mortal.IstotaZywa):
    punktyUmiejetnasci = 0
    pieniadze = 0
    wyposazenie_zalozone = ["", "", "", "", "", "", "", ""]     #states for Head, torso (tactical vest), belt, leg panel1, legpanel2, backpack, backpackslot1, backpackslot2
    specjalizacje = []


    def __init__(self, sila, zrecznasc, intelekt, imie="bob", pu=150, kasa=9000):
        super().__init__(sila, zrecznasc, intelekt, imie)
        self.punktyUmiejetnasci = pu + pu / 10 * self.modIntelekt
        self.pieniadze = kasa
        self.wybierzSpecjalizacje()
        self.nastawKosztUmiejetnasci()

    def __init__(self, sila, zrecznasc, intelekt, specjalizacje, imie="bob", pu=150, kasa=9000, ):
        super().__init__(sila, zrecznasc, intelekt, imie)
        self.punktyUmiejetnasci = pu + pu / 10 * self.modIntelekt
        self.pieniadze = kasa
        self.przypiszSpecjalizacje(specjalizacje[0])
        self.przypiszSpecjalizacje(specjalizacje[1])
        self.przypiszSpecjalizacje(specjalizacje[2])
        self.nastawKosztUmiejetnasci()

    #przypisuje 1 specjalizacje
    def przypiszSpecjalizacje(self, specjalizacja):
        self.specjalizacje.append(constans.wyszukajSpecjalizacje(specjalizacja))

    #Pozwala uzytkownikowi wybrac sobie 3 specjalizacje
    #TODO dalej mozna wybrac kilka razy te same specjalizacje!!! a nie powinno tak byc
    def wybierzSpecjalizacje(self):
        i = 0
        while(i < 3):
            system.Output("wybierz specjalizacje")
            y = constans.wyszukajSpecjalizacje(system.Input())
            if y != False:
                self.specjalizacje.append(y)
                i += 1
            else:
                system.Output("Zle wprowadzona specjalizacja. Sproboj jescze raz")

    #TODO zablokowac wiecej niz 3 razy wziecie tego samego (dyscypliny naukowe i zawodu
    def nastawKosztUmiejetnasci(self):
        for i in self.specjalizacje:
            i = i[1]
            umiejetnasciSpecjalizacji = i.split(',')
            ostateczne = []
            for y in umiejetnasciSpecjalizacji:
                ostateczne.append(y.strip())
            for z in ostateczne:
                if z == "dyscyplina naukowa lub zawod":
                    hamulec:int = 0
                    while hamulec == 0:
                        system.Output("Doprecyzuj: wybierz sposrod: \n1 dyscyplina naukowa Medycyna  "
                                      "  \n2: dyscyplina naukowa Informatyka \n3: dyscyplina naukowa Humanistyka,"
                                      "\n4: zawod Rusznikarz  \n5: zawod Kowal \n6: zawod Mechanik \n7: zawod Kucharz")
                        wejscie = system.Input()
                        if wejscie in constans.UmiejetnasciDoInt:
                            self.Umiejetnasci[constans.UmiejetnasciDoInt[wejscie]][2] = \
                            self.Umiejetnasci[constans.UmiejetnasciDoInt[wejscie]][2] + 1
                            hamulec += 1
                        else:
                            system.Output("zle wprowadzona dana. sproboj jeszcze raz")
                else:
                    self.Umiejetnasci[constans.UmiejetnasciDoInt[z]][2] = self.Umiejetnasci[constans.UmiejetnasciDoInt[z]][2] + 1


wojtek = Postac(8, 8, 8, ["Bron boczna", "Karabiny", "Nauka"])
print(wojtek.Umiejetnasci)
