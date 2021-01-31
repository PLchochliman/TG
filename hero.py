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
    #TODO nie wiem na chuj pojawia sie komunikat.
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
                    for juzwybrane in self.specjalizacje:
                        if specjalizacja == juzwybrane:
                            system.Output("Ta specjalizacja zostala juz wybrana")
                        else:
                            self.specjalizacje.append(specjalizacja)
                            wyjscie = wyjscie + 1
            else:
                system.Output("Zle wprowadzona specjalizacja. Sproboj jescze raz")

    #TODO zrobic zawody i dyscypliny naukowe
    def nastawKosztUmiejetnasciRecznie(self):
        for specjalizacja in self.specjalizacje:
            specjalizacja = specjalizacja[1]
            umiejetnasciSpecjalizacji = specjalizacja.split(',')
            ostateczne = []
            for umiejetnasciWyluskane in umiejetnasciSpecjalizacji:
                ostateczne.append(umiejetnasciWyluskane.strip())
            for umiejetnascWyciagnieta in ostateczne:
                if umiejetnascWyciagnieta == "dyscyplina naukowa lub zawod":
                    hamulec: int = 0
                    while hamulec == 0:
                        system.Output("Doprecyzuj: wybierz sposrod: \ndyscyplina naukowa Medycyna  "
                                      "  \ndyscyplina naukowa Informatyka \ndyscyplina naukowa Humanistyka,"
                                      "\nzawod Rusznikarz  \nzawod Kowal \nzawod Mechanik \nzawod Kucharz")
                        wejscie = system.Input()
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
                    self.Umiejetnasci[constans.UmiejetnasciDoInt[umiejetnascWyciagnieta]][2] = \
                    self.Umiejetnasci[constans.UmiejetnasciDoInt[umiejetnascWyciagnieta]][2] + 1

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


#wojtek = Postac(8, 8, 8, ["Bron boczna", "Karabiny", "Nauka"])
wojtek = Postac(8, 8, 8)
print(wojtek.Umiejetnasci)
