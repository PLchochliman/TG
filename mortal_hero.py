import mortal_base as mortal
import Bot as Bot
import excelDigger as excelDigger
import constans as constans
import przedmioty_bron as przedmioty_bron
import przedmioty_ochronne as przedmioty_ochronne
#import specialisations as specialisations

"""starting creating real playable character"""


class Postac(mortal.IstotaZywa): #pełne pokrycie, nie skończone
    #obsluga_specek = specialisations.Specialisations()
    punktyUmiejetnasci = 0
    pieniadze = 0
    element_szpeju = []
    zalozony_mundur = None
    specjalizacje = []
    aktywna_bron = []

    def __init__(self, sila, zrecznasc, intelekt, specjalizacje=None, imie="bob", pu=150, kasa=9000, ):
        super().__init__(sila, zrecznasc, intelekt, imie)
        self.punktyUmiejetnasci = pu + pu / 10 * self.mod_intelekt
        self.pieniadze = kasa
        self.specjalizacje = []
        self.element_szpeju = ["", "", "", "", "", "", "", "", "", "", ""]
        # mundur, klata, plecy, glowa, twarz, udo, ochraniacze, ramie, ramie2, uszy
        if specjalizacje:
            self.przypisz_specjalizacje(specjalizacje[0])
            self.przypisz_specjalizacje(specjalizacje[1])
            self.przypisz_specjalizacje(specjalizacje[2])
            self.nastaw_koszt_umiejetnasci_automatycznie()
        else:
            self.wybierz_specjalizacje()
            self.nastaw_koszt_umiejetnasci_recznie()

    def redukuj_obrazenia(self, rzut_na_obrazenia, penetracja):
        lista_elementow_zaaplikowanych = []
        for element in self.element_szpeju:
            if isinstance(element, przedmioty_ochronne.ElementSzpeju):
                if element.nazwa in lista_elementow_zaaplikowanych:
                    continue
                if element.redukcja:
                    rzut_na_obrazenia = element.przyjmij_obrazenia(penetracja, rzut_na_obrazenia)
                    lista_elementow_zaaplikowanych.append(element.nazwa)
        return rzut_na_obrazenia

    def aktualny_unik(self):
        premia_do_uniku_z_dodatkow = 0
        for element in self.element_szpeju:
            try:
                premia_do_uniku_z_dodatkow += element.premia_do_uniku
            except AttributeError:
                continue
        return self.unik + self.oslona + premia_do_uniku_z_dodatkow

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
                    self.umiejetnosci[constans.UmiejetnasciDoInt[umiejetnascWyciagnieta]][2] = \
                        self.umiejetnosci[constans.UmiejetnasciDoInt[umiejetnascWyciagnieta]][2] + 1

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
                            if self.umiejetnosci[constans.UmiejetnasciDoInt[wejscie]][2] != 3:
                                self.umiejetnosci[constans.UmiejetnasciDoInt[wejscie]][2] = \
                                    self.umiejetnosci[constans.UmiejetnasciDoInt[wejscie]][2] + 1
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
                            if self.umiejetnosci[constans.UmiejetnasciDoInt[wejscie]][2] != 3:
                                self.umiejetnosci[constans.UmiejetnasciDoInt[wejscie]][2] = \
                                    self.umiejetnosci[constans.UmiejetnasciDoInt[wejscie]][2] + 1
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
                            if self.umiejetnosci[constans.UmiejetnasciDoInt[wejscie]][2] != 3:
                                self.umiejetnosci[constans.UmiejetnasciDoInt[wejscie]][2] = \
                                    self.umiejetnosci[constans.UmiejetnasciDoInt[wejscie]][2] + 1
                                hamulec += 1
                            else:
                                Bot.output("juz 3 raz wybrales te umiejetnasc. wybierz inna.")
                        else:
                            Bot.output("zle wprowadzona dana. sproboj jeszcze raz")
                    else:
                        Bot.output("wybrano umiejetnosc spoza spektrum! \n sprobuj ponownie")
        except KeyError:
            Bot.output("Zle podales nazwe umiejetnosci, sproboj jeszcze raz")
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
                        if self.umiejetnosci[constans.UmiejetnasciDoInt["dyscyplina naukowa Medycyna"]][2] < 3:
                            self.umiejetnosci[constans.UmiejetnasciDoInt["dyscyplina naukowa Medycyna"]][2] += 1
                        elif self.umiejetnosci[constans.UmiejetnasciDoInt["zawod Rusznikarz"]][2] < 3:
                            self.umiejetnosci[constans.UmiejetnasciDoInt["zawod Rusznikarz"]][2] += 1
                        elif self.umiejetnosci[constans.UmiejetnasciDoInt["dyscyplina naukowa Informatyka"]][2] < 3:
                            self.umiejetnosci[constans.UmiejetnasciDoInt["dyscyplina naukowa Informatyka"]][2] += 1
                        hamulec = 1
                else:
                    self.umiejetnosci[constans.UmiejetnasciDoInt[umiejetnasc]][2] = self.umiejetnosci[constans.UmiejetnasciDoInt[umiejetnasc]][2] + 1

    def wykup_range(self, nazwaUmiejetnasci):
        if nazwaUmiejetnasci in constans.UmiejetnasciDoInt:
            umiejetnasc = constans.UmiejetnasciDoInt[nazwaUmiejetnasci]
            # jeżeli w 3 speckach jest dana umiejka to wtedy jest specjalne wykupowanie
            if self.umiejetnosci[umiejetnasc][2] == 3:
                if self.umiejetnosci[umiejetnasc][0] == 0:
                    self.umiejetnosci[umiejetnasc][0] = 1
                else:
                    if self.punktyUmiejetnasci >= (self.umiejetnosci[umiejetnasc][0]):
                        self.punktyUmiejetnasci = self.punktyUmiejetnasci - (self.umiejetnosci[umiejetnasc][0])
                        self.umiejetnosci[umiejetnasc][0] = self.umiejetnosci[umiejetnasc][0] + 1
                        self.umiejetnosci[umiejetnasc][1] = self.umiejetnosci[umiejetnasc][0] + \
                                                            (self.umiejetnosci[umiejetnasc][0])
                    else:
                        Bot.output("nie stać Cię. Podexp")

            #dla reszty
            else:
                if self.punktyUmiejetnasci >= (self.umiejetnosci[umiejetnasc][0] + 1)*(3 - self.umiejetnosci[umiejetnasc][2]):
                    self.punktyUmiejetnasci = self.punktyUmiejetnasci - \
                                    ((self.umiejetnosci[umiejetnasc][0] + 1) * (3 - self.umiejetnosci[umiejetnasc][2]))
                    self.umiejetnosci[umiejetnasc][0] = self.umiejetnosci[umiejetnasc][0] + 1
                    self.umiejetnosci[umiejetnasc][1] = self.umiejetnosci[umiejetnasc][1] + \
                                                        (self.umiejetnosci[umiejetnasc][0] * (3 - self.umiejetnosci[umiejetnasc][2]))
                else:
                    Bot.output("nie stać Cię. Podexp")
            if umiejetnasc == constans.UmiejetnasciDoInt["jezyki"]:
                self.podnies_jezyki("angielski")    #PAMIĘTAJ ŻE TRZYBA TO ROZWIĄZA INACZEJ W KLASIE WYBORU DOCELOWEJ!!!!!
            if umiejetnasc == constans.UmiejetnasciDoInt["zmysl bitewny"]:
                self.nastaw_unik()
        else:
            Bot.output("nie ma takiej umiejetnosci")

    def podnies_predyspozycje(self, specjalizacja):
        for i in self.specjalizacje:
            if specjalizacja == i[0]:
                i = i[1].split(", ")
                for j in range(0, len(i)):
                    i[j] = i[j].strip()
                for umiejetnasc in i:
                    umiejetnasc = constans.UmiejetnasciDoInt[umiejetnasc]
                    self.umiejetnosci[umiejetnasc][3] = self.umiejetnosci[umiejetnasc][3] + 1

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

    def podnies_umiejetnosc_specjalizacji(self, ktora_specjalizacja, ktora_umiejetnasc):
        for specjalizacja in self.specjalizacje:
            if specjalizacja[0] == ktora_specjalizacja:
                for umiejetnasc_index in range(0, len(specjalizacja)):
                    if specjalizacja[umiejetnasc_index] == ktora_umiejetnasc:
                        mnoznik_ceny = 2
                        if umiejetnasc_index == 12:
                            mnoznik_ceny = 3
                        cena_podniesienia_umiejetnasci = (specjalizacja[umiejetnasc_index - 1] + 1) * mnoznik_ceny
                        if self.punktyUmiejetnasci >= cena_podniesienia_umiejetnasci:
                            if specjalizacja[umiejetnasc_index - 1] < 6:
                                self.punktyUmiejetnasci = int(self.punktyUmiejetnasci - cena_podniesienia_umiejetnasci)
                                specjalizacja[umiejetnasc_index - 1] = specjalizacja[umiejetnasc_index - 1] + 1
                        else:
                            Bot.output("nie stać Cię. Podexp")
                        return True
        return False

    def rzut_na_umiejetnasc(self, testowana_umiejetnasc, modyfikator=0):
        if testowana_umiejetnasc == "strzelectwo":
            umiejka = constans.UmiejetnasciDoInt[testowana_umiejetnasc]
            doRzutu = self.umiejetnosci[umiejka]
            wynik = []
            for kosc in range(0, constans.liczba_kosci_umiejetnosci[doRzutu[0]]):
                    rzut_koscia = Bot.roll_dice(6)
                    wynik.append(rzut_koscia)
            wynik = self.__aplikuj_wprawe_izsumuj_wynik(wynik)
            wynik += int(doRzutu[3] + modyfikator + self.kara())
            return wynik
        return super(Postac, self).rzut_na_umiejetnasc(testowana_umiejetnasc,
                                                       self.handling_specialisations_about_skills(testowana_umiejetnasc))

    def handling_specialisations_before_hit(self):
        return 0

    def handling_specialisations_reducing_recoil(self, tryb):
        return 0

    def handling_specialisations_about_ammo_consuption(self, result):
        return 0

    def handling_specialisations_after_hit(self):
        return 0

    def handling_specialisations_about_skills(self, umiejetnosc):
        return 0

    def handling_specialisations_changing_stats(self):
        return 0

    def __aplikuj_wprawe_izsumuj_wynik(self, result):
        if self.aktywna_bron:
            for specjalizacja in self.specjalizacje:
                check = min(result)
                for zasada_broni in self.aktywna_bron.zasady_specjalne:
                    if zasada_broni in specjalizacja[4]:
                        if specjalizacja[2] > check:
                            result[result.index(check)] = specjalizacja[2]
                            check = specjalizacja[2]
                if self.aktywna_bron.aktualny_magazynek.amunicja.charakterystyka_naboju in specjalizacja[4]:
                    if specjalizacja[2] >= check:
                        result[result.index(check)] = specjalizacja[2]
                        break
        wyjscie = 0
        for i in result:
            wyjscie += i
        return wyjscie

    def __bron_boczna(self):
        return 0

    def otrzymaj_pieniadze(self, kasa):
        self.pieniadze += kasa
        Bot.output(self.imie + " otrzymał " + str(kasa) + "$. \nPosiada teraz " + str(self.pieniadze) + "$.")
        return True

    def wydaj_pieniadze(self, kasa):
        if self.pieniadze - kasa < 0:
            Bot.output("Nie stac Cię!!!!")
            return False
        self.pieniadze -= kasa
        Bot.output(self.imie + " wydał " + str(kasa) + "$. \nPosiada teraz " + str(self.pieniadze) + "$.")
        return True