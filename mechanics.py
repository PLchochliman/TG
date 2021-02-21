import hero
import items_new as items
import Bot as Bot


class akcje():
    costam = 0


class WalkaWrecz(akcje):
    def uderz(self, operator, cel, zasieg=0): # TODO bez testow!!!!!
        try:
            wynik = operator.rzut_na_umiejetnasc("walka wrecz")
            if operator.aktywna_bron.zasieg_maksymalny < 2:
                wynik = wynik + operator.aktywna_bron.premia
            odpowiedz = cel.rzut_na_umiejetnasc("walka wrecz")
            if cel.aktywna_bron.zasieg_maksymalny < 2:
                odpowiedz = odpowiedz + cel.aktywna_bron.premia
            if wynik > odpowiedz:
                if wynik >= cel.bazowy_unik / 2:
                    self.test_obrazen_z_egzekucja(cel)
                    return True
                else:
                    raise Exception('walczysz lepiej od wroga, ale wciąż nie jesteś w stanie go trafić')
            else:
                raise Exception('przeciwnik lepiej walczy')
        except Exception as inst:
            powod = inst.args[0]
            Bot.output('Na celu nie zrobilo to zadnego wrazenia bo ' + powod)

class Shooting(akcje):
    @staticmethod
    def strzal(operator, cel, odleglosc):
        return 0

    """
    failuje w momencie kiedy operator nie moze trafic celu.
    """

    def test_trafienia(self, operator, cel, dodatkowe, zasieg):
        return operator.aktywna_bron.test_trafienia(operator, cel, dodatkowe, zasieg)

   # @staticmethod
# wciaz nie sprawdza broni czy mozne napierdalac danym trybem, oraz nie daje możliwości do strzelania 2 wrogów naRaz.
# nie sprawdza równierz kar za różne zasięgi.
    def strzelaj(self, operator, cel, zasieg, tryb="pojedynczy"):
        try:
            if tryb in ("samoczynny", "serie"):
                if operator.aktywna_bron.statystyki_podstawowe[2] in ("sa", "ba", "bu"):
                    tryb = "pojedynczy"
            dodatkowe = 0
            if tryb == "pelne skupienie":
                dodatkowe = Bot.roll_dice_from_text("3d6")
                zasieg = zasieg/2
            wynik = self.test_trafienia(operator, cel, dodatkowe, zasieg) #failuje juz z wyjatku testu trafienia
            if wynik > 0:
                if tryb == "samoczynny":
                    if wynik > operator.aktywna_bron.statystyki_podstawowe[2]:
                        wynik = operator.aktywna_bron.statystyki_podstawowe[2]
                    for i in range(0, int(wynik)):
                        operator.aktywna_bron.test_obrazen_z_egzekucja(cel)
                if tryb == 'serie':
                    if wynik > 3:
                        wynik = 3
                    for i in range(0, int(wynik)):
                        operator.aktywna_bron.test_obrazen_z_egzekucja(cel)
                if tryb in ("pojedynczy", "pelne skupienie"):
                    premia = wynik / 3
                    if wynik > 10:
                        cel.rana(11)
                    else:
                        operator.aktywna_bron.test_obrazen_z_egzekucja(cel, premia)

                return wynik
            else:
                operator.aktywna_bron.test_obrazen_z_egzekucja(cel)
        except Exception as inst:
            powod = inst.args[0]
            Bot.output(cel.imie + " nie oberwal bo " + powod)
            return False

"""
itemki = items.Przedmioty('')
m4ka = itemki.luskacz_broni("m4a1")
M4KA = items.BronStrzelecka(m4ka)
wojtek = hero.Postac(8, 8, 8, ["bron boczna", "karabiny", "bron krotka"])
"""