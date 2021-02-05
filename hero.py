import mortal as mortal
import system as system
import excelDigger as excelDigger
import constans as constans

"starting creating real character"


class Postac(mortal.IstotaZywa):
    punktyUmiejetnasci = 0
    pieniadze = 0
    wyposazenie_zalozone = ["", "", "", "", "", "", "", ""]     #  states for Head, torso (tactical vest), belt, leg panel1, legpanel2, backpack, backpackslot1, backpackslot2
    zalozony_mundur = None
    specjalizacje = []

    def __init__(self, sila, zrecznasc, intelekt, specjalizacje=None, imie="bob", pu=150, kasa=9000, ):
        super().__init__(sila, zrecznasc, intelekt, imie)
        self.punktyUmiejetnasci = pu + pu / 10 * self.modIntelekt
        self.pieniadze = kasa
        if specjalizacje:
            self.przypiszSpecjalizacje(specjalizacje[0])
            self.przypiszSpecjalizacje(specjalizacje[1])
            self.przypiszSpecjalizacje(specjalizacje[2])
            self.nastawKosztUmiejetnasciAutomatycznie()
        else:
            self.wybierzSpecjalizacje()
            self.nastawKosztUmiejetnasciRecznie()

    #przypisuje 1 specjalizacje
    def przypiszSpecjalizacje(self, specjalizacja):
        self.specjalizacje.append(constans.wyszukajSpecjalizacje(specjalizacja))

    #Pozwala uzytkownikowi wybrac sobie 3 specjalizacje
    def wybierzSpecjalizacje(self):
        wyjscie = 0
        while wyjscie < 3:
            system.Output("wybierz specjalizacje")
            specjalizacja = constans.wyszukajSpecjalizacje(system.Input())
            if specjalizacja:
                if wyjscie < 1:
                    self.specjalizacje.append(specjalizacja)
                    wyjscie = wyjscie + 1
                else:
                    if specjalizacja in self.specjalizacje:
                        system.Output("Ta specjalizacja zostala juz wybrana")
                    else:
                        self.specjalizacje.append(specjalizacja)
                        wyjscie = wyjscie + 1
            else:
                system.Output("Zle wprowadzona specjalizacja. Sproboj jescze raz")

    #nastawia koszty umiejętności
    def nastawKosztUmiejetnasciRecznie(self):
        for specjalizacja in self.specjalizacje:
            specjalizacja = specjalizacja[1]
            umiejetnasciSpecjalizacji = specjalizacja.split(',')
            ostateczne = []
            for umiejetnasciWyluskane in umiejetnasciSpecjalizacji:
                ostateczne.append(umiejetnasciWyluskane.strip())
            for umiejetnascWyciagnieta in ostateczne:
                if umiejetnascWyciagnieta in ["dyscyplina naukowa lub zawod", "dyscyplina naukowa", "zawod"]:
                    self.dobierzZawod(umiejetnascWyciagnieta)
                else:
                    self.Umiejetnasci[constans.UmiejetnasciDoInt[umiejetnascWyciagnieta]][2] = \
                    self.Umiejetnasci[constans.UmiejetnasciDoInt[umiejetnascWyciagnieta]][2] + 1

    #rozwiązuje problem zawodu, dyscypliny naukowej.
    def dobierzZawod(self, typDoprecyzowania):
        try:
            if typDoprecyzowania == "dyscyplina naukowa lub zawod":
                hamulec: int = 0
                while hamulec == 0:
                    system.Output("Doprecyzuj: wybierz sposrod: \ndyscyplina naukowa Medycyna  "
                                  "  \ndyscyplina naukowa Informatyka \ndyscyplina naukowa Humanistyka,"
                                  "\nzawod Rusznikarz  \nzawod Kowal \nzawod Mechanik \nzawod Kucharz")
                    wejscie = system.Input()
                    if 17 < constans.UmiejetnasciDoInt[wejscie] < 25:
                        if wejscie in constans.UmiejetnasciDoInt:
                            if self.Umiejetnasci[constans.UmiejetnasciDoInt[wejscie]][2] != 3:
                                self.Umiejetnasci[constans.UmiejetnasciDoInt[wejscie]][2] = \
                                    self.Umiejetnasci[constans.UmiejetnasciDoInt[wejscie]][2] + 1
                                hamulec += 1
                            else:
                                system.Output("juz 3 raz wybrales te umiejetnasc. wybierz inna.")
                        else:
                            system.Output("zle wprowadzona dana. sproboj jeszcze raz")
                    else:
                        system.Output("wybrano umiejetnosc spoza spektrum! \n sprobuj ponownie")
            elif typDoprecyzowania == "dyscyplina naukowa":
                hamulec: int = 0
                while hamulec == 0:
                    system.Output("Doprecyzuj: wybierz sposrod: \ndyscyplina naukowa Medycyna  "
                                  "  \ndyscyplina naukowa Informatyka \ndyscyplina naukowa Humanistyka,")
                    wejscie = system.Input()
                    if 17 < constans.UmiejetnasciDoInt[wejscie] < 21:
                        if wejscie in constans.UmiejetnasciDoInt:
                            if self.Umiejetnasci[constans.UmiejetnasciDoInt[wejscie]][2] != 3:
                                self.Umiejetnasci[constans.UmiejetnasciDoInt[wejscie]][2] = \
                                    self.Umiejetnasci[constans.UmiejetnasciDoInt[wejscie]][2] + 1
                                hamulec += 1
                            else:
                                system.Output("juz 3 raz wybrales te umiejetnasc. wybierz inna.")
                        else:
                            system.Output("zle wprowadzona dana. sproboj jeszcze raz")
                    else:
                        system.Output("wybrano umiejetnosc spoza spektrum! \n sprobuj ponownie")
            elif typDoprecyzowania == "zawod":
                hamulec: int = 0
                while hamulec == 0:
                    system.Output("Doprecyzuj: wybierz sposrod: \nzawod Rusznikarz \nzawod Kowal"
                                  "\nzawod Mechanik \nzawod Kucharz")
                    wejscie = system.Input()
                    if 20 < constans.UmiejetnasciDoInt[wejscie] < 25:
                        if wejscie in constans.UmiejetnasciDoInt:
                            if self.Umiejetnasci[constans.UmiejetnasciDoInt[wejscie]][2] != 3:
                                self.Umiejetnasci[constans.UmiejetnasciDoInt[wejscie]][2] = \
                                    self.Umiejetnasci[constans.UmiejetnasciDoInt[wejscie]][2] + 1
                                hamulec += 1
                            else:
                                system.Output("juz 3 raz wybrales te umiejetnasc. wybierz inna.")
                        else:
                            system.Output("zle wprowadzona dana. sproboj jeszcze raz")
                    else:
                        system.Output("wybrano umiejetnosc spoza spektrum! \n sprobuj ponownie")
        except KeyError:
            system.Output("Zle podales nazwe umiejetnasci, sproboj jeszcze raz")
            self.dobierzZawod(typDoprecyzowania)

    def nastawKosztUmiejetnasciAutomatycznie(self):
        for specjalizacja in self.specjalizacje:
            specjalizacja = specjalizacja[1]
            umiejetnasciSpecjalizacji = specjalizacja.split(',')
            ostateczne = []
            for umiejetnasci in umiejetnasciSpecjalizacji:
                ostateczne.append(umiejetnasci.strip())
            for umiejetnasc in ostateczne:
                if umiejetnasc == "dyscyplina naukowa lub zawod":
                    hamulec: int = 0
                    while hamulec == 0:
                        if self.Umiejetnasci[constans.UmiejetnasciDoInt["dyscyplina naukowa Medycyna"]][2] < 3:
                            self.Umiejetnasci[constans.UmiejetnasciDoInt["dyscyplina naukowa Medycyna"]][2] += 1
                        elif self.Umiejetnasci[constans.UmiejetnasciDoInt["zawod Rusznikarz"]][2] < 3:
                            self.Umiejetnasci[constans.UmiejetnasciDoInt["zawod Rusznikarz"]][2] += 1
                        elif self.Umiejetnasci[constans.UmiejetnasciDoInt["dyscyplina naukowa Informatyka"]][2] < 3:
                            self.Umiejetnasci[constans.UmiejetnasciDoInt["dyscyplina naukowa Informatyka"]][2] += 1
                        hamulec = 1
                else:
                    self.Umiejetnasci[constans.UmiejetnasciDoInt[umiejetnasc]][2] = self.Umiejetnasci[constans.UmiejetnasciDoInt[umiejetnasc]][2] + 1

    """
        umiejetnasci is table for skills. from constants you 
        first states for skill level, second for Cost, 
        3rd of specializations (Cost is dependingo for it), 
        4th is for all modifiers from predispositions (skill in specialisations)and modifiers from stats
        5th is all for modifier based on base stats modifier. 0 states for none, 1 is for Power, 2 is for Dexerity, 3 is
        for Inteligence, 4 is for Power or Inteligence, 5 is for Dexerity or Inteligence, 6 is for Power or Dexerity.
    """
    def wykupRange(self, nazwaUmiejetnasci):
        if nazwaUmiejetnasci in constans.UmiejetnasciDoInt:
            umiejetnasc = constans.UmiejetnasciDoInt[nazwaUmiejetnasci]
            # jeżeli w 3 speckach jest dana umiejka to wtedy jest specjalne wykupowanie
            if self.Umiejetnasci[umiejetnasc][2] == 3:
                if self.Umiejetnasci[umiejetnasc][0] == 0:
                    self.Umiejetnasci[umiejetnasc][0] = 1
                else:
                    if self.punktyUmiejetnasci >= (self.Umiejetnasci[umiejetnasc][0]):
                        self.punktyUmiejetnasci = self.punktyUmiejetnasci - (self.Umiejetnasci[umiejetnasc][0])
                        self.Umiejetnasci[umiejetnasc][0] = self.Umiejetnasci[umiejetnasc][0] + 1
                        self.Umiejetnasci[umiejetnasc][1] = self.Umiejetnasci[umiejetnasc][0] + \
                                                            (self.Umiejetnasci[umiejetnasc][0])
                    else:
                        system.Output("nie stać Cię. Podexp")
            #dla reszty
            else:
                if self.punktyUmiejetnasci >= (self.Umiejetnasci[umiejetnasc][0]+1)*(3-self.Umiejetnasci[umiejetnasc][2]):
                    self.punktyUmiejetnasci = self.punktyUmiejetnasci - \
                                    ((self.Umiejetnasci[umiejetnasc][0]+1) * (3 - self.Umiejetnasci[umiejetnasc][2]))
                    self.Umiejetnasci[umiejetnasc][0] = self.Umiejetnasci[umiejetnasc][0] + 1
                    self.Umiejetnasci[umiejetnasc][1] = self.Umiejetnasci[umiejetnasc][1] +\
                                    ((self.Umiejetnasci[umiejetnasc][0]) * (3 - self.Umiejetnasci[umiejetnasc][2]))
                else:
                    system.Output("nie stać Cię. Podexp")
        else:
            system.Output("nie ma takiej umiejetnasci")

    def podniesPredyspozycje(self, specjalizacja):
        for i in self.specjalizacje:
            if specjalizacja == i[0]:
                i = i[1].split(", ")
                i[5] = i[5].strip()
                for umiejetnasc in i:
                    umiejetnasc = constans.UmiejetnasciDoInt[umiejetnasc]
                    self.Umiejetnasci[umiejetnasc][3] = self.Umiejetnasci[umiejetnasc][3] + 1

"""
do testów
wojtek = Postac(8, 8, 8, ["Bron boczna", "Karabiny", "Karabiny maszynowe"])
"""