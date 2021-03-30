import mortal as mortal
import Bot as Bot
import excelDigger as excelDigger
import constans as constans

"starting creating real character"


class Postac(mortal.IstotaZywa): #pełne pokrycie, nie skończone
    punktyUmiejetnasci = 0
    pieniadze = 0
    wyposazenie_zalozone = ["", "", "", "", "", "", "", ""]     #  states for Head, torso (tactical vest), belt, leg panel1, legpanel2, backpack, backpackslot1, backpackslot2
    zalozony_mundur = None
    specjalizacje = []
    aktywna_bron = []

    def __init__(self, sila, zrecznasc, intelekt, specjalizacje=None, imie="bob", pu=150, kasa=9000, ):
        super().__init__(sila, zrecznasc, intelekt, imie)
        self.punktyUmiejetnasci = pu + pu / 10 * self.mod_intelekt
        self.pieniadze = kasa
        if specjalizacje:
            self.przypisz_specjalizacje(specjalizacje[0])
            self.przypisz_specjalizacje(specjalizacje[1])
            self.przypisz_specjalizacje(specjalizacje[2])
            self.nastaw_koszt_umiejetnasci_automatycznie()
        else:
            self.wybierz_specjalizacje()
            self.nastaw_koszt_umiejetnasci_recznie()

    #przypisuje 1 specjalizacje
    def przypisz_specjalizacje(self, specjalizacja):
        self.specjalizacje.append(constans.wyszukajSpecjalizacje(specjalizacja))

    #Pozwala uzytkownikowi wybrac sobie 3 specjalizacje
    def wybierz_specjalizacje(self):
        wyjscie = 0
        while wyjscie < 3:
            Bot.output("wybierz specjalizacje")
            specjalizacja = constans.wyszukajSpecjalizacje(Bot.input_for_bot())
            if specjalizacja:
                if wyjscie < 1:
                    self.specjalizacje.append(specjalizacja)
                    wyjscie = wyjscie + 1
                else:
                    if specjalizacja in self.specjalizacje:
                        Bot.output("Ta specjalizacja zostala juz wybrana")
                    else:
                        self.specjalizacje.append(specjalizacja)
                        wyjscie = wyjscie + 1
            else:
                Bot.output("Zle wprowadzona specjalizacja. Sproboj jescze raz")

    #nastawia koszty umiejętności
    def nastaw_koszt_umiejetnasci_recznie(self):
        for specjalizacja in self.specjalizacje:
            specjalizacja = specjalizacja[1]
            umiejetnasciSpecjalizacji = specjalizacja.split(',')
            ostateczne = []
            for umiejetnasciWyluskane in umiejetnasciSpecjalizacji:
                ostateczne.append(umiejetnasciWyluskane.strip())
            for umiejetnascWyciagnieta in ostateczne:
                if umiejetnascWyciagnieta in ["dyscyplina naukowa lub zawod", "dyscyplina naukowa", "zawod"]:
                    self.dobierz_zawod(umiejetnascWyciagnieta)
                else:
                    self.umiejetnasci[constans.UmiejetnasciDoInt[umiejetnascWyciagnieta]][2] = \
                        self.umiejetnasci[constans.UmiejetnasciDoInt[umiejetnascWyciagnieta]][2] + 1


    #rozwiązuje problem zawodu, dyscypliny naukowej.
    def dobierz_zawod(self, typDoprecyzowania):
        try:
            if typDoprecyzowania == "dyscyplina naukowa lub zawod":
                hamulec: int = 0
                while hamulec == 0:
                    Bot.output("Doprecyzuj: wybierz sposrod: \ndyscyplina naukowa Medycyna  "
                                  "  \ndyscyplina naukowa Informatyka \ndyscyplina naukowa Humanistyka,"
                                  "\nzawod Rusznikarz  \nzawod Kowal \nzawod Mechanik \nzawod Kucharz")
                    wejscie = Bot.input_for_bot()
                    if 17 < constans.UmiejetnasciDoInt[wejscie] < 25:
                        if wejscie in constans.UmiejetnasciDoInt:
                            if self.umiejetnasci[constans.UmiejetnasciDoInt[wejscie]][2] != 3:
                                self.umiejetnasci[constans.UmiejetnasciDoInt[wejscie]][2] = \
                                    self.umiejetnasci[constans.UmiejetnasciDoInt[wejscie]][2] + 1
                                hamulec += 1
                            else:
                                Bot.output("juz 3 raz wybrales te umiejetnasc. wybierz inna.")
                        else:
                            Bot.output("zle wprowadzona dana. sproboj jeszcze raz")
                    else:
                        Bot.output("wybrano umiejetnosc spoza spektrum! \n sprobuj ponownie")
            elif typDoprecyzowania == "dyscyplina naukowa":
                hamulec: int = 0
                while hamulec == 0:
                    Bot.output("Doprecyzuj: wybierz sposrod: \ndyscyplina naukowa Medycyna  "
                                  "  \ndyscyplina naukowa Informatyka \ndyscyplina naukowa Humanistyka,")
                    wejscie = Bot.input_for_bot()
                    if 17 < constans.UmiejetnasciDoInt[wejscie] < 21:
                        if wejscie in constans.UmiejetnasciDoInt:
                            if self.umiejetnasci[constans.UmiejetnasciDoInt[wejscie]][2] != 3:
                                self.umiejetnasci[constans.UmiejetnasciDoInt[wejscie]][2] = \
                                    self.umiejetnasci[constans.UmiejetnasciDoInt[wejscie]][2] + 1
                                hamulec += 1
                            else:
                                Bot.output("juz 3 raz wybrales te umiejetnasc. wybierz inna.")
                        else:
                            Bot.output("zle wprowadzona dana. sproboj jeszcze raz")
                    else:
                        Bot.output("wybrano umiejetnosc spoza spektrum! \n sprobuj ponownie")
            elif typDoprecyzowania == "zawod":
                hamulec: int = 0
                while hamulec == 0:
                    Bot.output("Doprecyzuj: wybierz sposrod: \nzawod Rusznikarz \nzawod Kowal"
                                  "\nzawod Mechanik \nzawod Kucharz")
                    wejscie = Bot.input_for_bot()
                    if 20 < constans.UmiejetnasciDoInt[wejscie] < 25:
                        if wejscie in constans.UmiejetnasciDoInt:
                            if self.umiejetnasci[constans.UmiejetnasciDoInt[wejscie]][2] != 3:
                                self.umiejetnasci[constans.UmiejetnasciDoInt[wejscie]][2] = \
                                    self.umiejetnasci[constans.UmiejetnasciDoInt[wejscie]][2] + 1
                                hamulec += 1
                            else:
                                Bot.output("juz 3 raz wybrales te umiejetnasc. wybierz inna.")
                        else:
                            Bot.output("zle wprowadzona dana. sproboj jeszcze raz")
                    else:
                        Bot.output("wybrano umiejetnosc spoza spektrum! \n sprobuj ponownie")
        except KeyError:
            Bot.output("Zle podales nazwe umiejetnasci, sproboj jeszcze raz")
            self.dobierz_zawod(typDoprecyzowania)

    """
    sets skills from predispositions autmaticly, without any question - which is impoertant when you wonna take anything 
    else than medicine, gunner, or IT specialists.
    """
    def nastaw_koszt_umiejetnasci_automatycznie(self):
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
                        if self.umiejetnasci[constans.UmiejetnasciDoInt["dyscyplina naukowa Medycyna"]][2] < 3:
                            self.umiejetnasci[constans.UmiejetnasciDoInt["dyscyplina naukowa Medycyna"]][2] += 1
                        elif self.umiejetnasci[constans.UmiejetnasciDoInt["zawod Rusznikarz"]][2] < 3:
                            self.umiejetnasci[constans.UmiejetnasciDoInt["zawod Rusznikarz"]][2] += 1
                        elif self.umiejetnasci[constans.UmiejetnasciDoInt["dyscyplina naukowa Informatyka"]][2] < 3:
                            self.umiejetnasci[constans.UmiejetnasciDoInt["dyscyplina naukowa Informatyka"]][2] += 1
                        hamulec = 1
                else:
                    self.umiejetnasci[constans.UmiejetnasciDoInt[umiejetnasc]][2] = self.umiejetnasci[constans.UmiejetnasciDoInt[umiejetnasc]][2] + 1

    """
        umiejetnasci is table for skills. from constants you 
        first states for skill level, second for Cost, 
        3rd of specializations (Cost is dependingo for it), 
        4th is for all modifiers from predispositions (skill in specialisations)and modifiers from stats
        5th is all for modifier based on base stats modifier. 0 states for none, 1 is for Power, 2 is for Dexerity, 3 is
        for Inteligence, 4 is for Power or Inteligence, 5 is for Dexerity or Inteligence, 6 is for Power or Dexerity.
    """
    def wykup_range(self, nazwaUmiejetnasci):
        if nazwaUmiejetnasci in constans.UmiejetnasciDoInt:
            umiejetnasc = constans.UmiejetnasciDoInt[nazwaUmiejetnasci]
            # jeżeli w 3 speckach jest dana umiejka to wtedy jest specjalne wykupowanie
            if self.umiejetnasci[umiejetnasc][2] == 3:
                if self.umiejetnasci[umiejetnasc][0] == 0:
                    self.umiejetnasci[umiejetnasc][0] = 1
                else:
                    if self.punktyUmiejetnasci >= (self.umiejetnasci[umiejetnasc][0]):
                        self.punktyUmiejetnasci = self.punktyUmiejetnasci - (self.umiejetnasci[umiejetnasc][0])
                        self.umiejetnasci[umiejetnasc][0] = self.umiejetnasci[umiejetnasc][0] + 1
                        self.umiejetnasci[umiejetnasc][1] = self.umiejetnasci[umiejetnasc][0] + \
                                                            (self.umiejetnasci[umiejetnasc][0])
                    else:
                        Bot.output("nie stać Cię. Podexp")

            #dla reszty
            else:
                if self.punktyUmiejetnasci >= (self.umiejetnasci[umiejetnasc][0] + 1)*(3 - self.umiejetnasci[umiejetnasc][2]):
                    self.punktyUmiejetnasci = self.punktyUmiejetnasci - \
                                    ((self.umiejetnasci[umiejetnasc][0] + 1) * (3 - self.umiejetnasci[umiejetnasc][2]))
                    self.umiejetnasci[umiejetnasc][0] = self.umiejetnasci[umiejetnasc][0] + 1
                    self.umiejetnasci[umiejetnasc][1] = self.umiejetnasci[umiejetnasc][1] + \
                                                        (self.umiejetnasci[umiejetnasc][0] * (3 - self.umiejetnasci[umiejetnasc][2]))
                else:
                    Bot.output("nie stać Cię. Podexp")
            if umiejetnasc == constans.UmiejetnasciDoInt["jezyki"]:
                self.podnies_jezyki("angielski")    #PAMIĘTAJ ŻE TRZYBA TO ROZWIĄZA INACZEJ W KLASIE WYBORU DOCELOWEJ!!!!!
            if umiejetnasc == constans.UmiejetnasciDoInt["zmysl bitewny"]:
                self.nastaw_unik()
        else:
            Bot.output("nie ma takiej umiejetnasci")

    def podnies_predyspozycje(self, specjalizacja):
        for i in self.specjalizacje:
            if specjalizacja == i[0]:
                i = i[1].split(", ")
                i[5] = i[5].strip()
                for umiejetnasc in i:
                    umiejetnasc = constans.UmiejetnasciDoInt[umiejetnasc]
                    self.umiejetnasci[umiejetnasc][3] = self.umiejetnasci[umiejetnasc][3] + 1

    def podnies_jezyki(self, jezyk=""): # do obejrzenia ANIOŁ LUDZIEJ EWOLUCJI
        if jezyk:
            switch = 0
            for i in range(0, len(self.jezyki)):
                if jezyk == self.jezyki[i][0]:
                    self.jezyki[i][1] = self.jezyki[i][1] + 1
                    switch = 1
            if switch == 0:
                self.jezyki.append([jezyk, 1])
        else:
            Bot.output("Jaki jezyk chcesz sie nauczyc/doszkolic")
            wejcie = Bot.input_for_bot()
            switch = 0
            for i in range(0, len(self.jezyki)):
                if wejcie == self.jezyki[i][0]:
                    self.jezyki[i][1] = self.jezyki[i][1] + 1
                    switch = 1
            if switch == 0:
                self.jezyki.append([wejcie, 1])

    def dodaj_umiejetnosci_specjalizacji(self):
        return 0

wojtek = Postac(8, 8, 8, ["Bron boczna", "Karabiny", "Karabiny maszynowe"])
