import random
import json
import uuid

MORJE = 'M'
LADJA = 'L'
ZADETA_LADJA = 'Z'
POTOPLJENA_LADJA = 'X'
NEODKRITO = 'N'
ZAPRTO_POLJE = 'I'
KONEC_IGRE = 'K'
ZACETEK = 'y'

class Morje:
    
    def __init__(self, velikost, mapa=None, odkrivanje=None, proste_kooridnate=None, trenutna_ladja=None, ladje=None):
        self.velikost = velikost
        moja_mapa = [0] * (velikost ** 2)
        neodkrita_mapa = [0] * (velikost ** 2)
        koordinate = []
        for x in range(velikost**2):
            moja_mapa[x] = MORJE
            neodkrita_mapa[x] = NEODKRITO
            koordinate.append(x)
        if mapa == None:
            self.mapa = moja_mapa
        else:
            self.mapa = mapa
        if odkrivanje == None:
            self.odkrivanje = neodkrita_mapa
        else:
            self.odkrivanje = odkrivanje
        if proste_kooridnate == None:
            self.proste_koordinate = koordinate
        else:
            self.proste_koordinate = proste_kooridnate
        if trenutna_ladja == None:
            self.trenutna_ladja = []
        else:
            self.trenutna_ladja = trenutna_ladja
        if ladje == None:
            self.ladje = []
        else:
            self.ladje = ladje
    
    def velikosti_ladij_glede_na_velikost(self):
        l = 0
        for ladja in self.ladje:
            l += len(ladja)
        l += len(self.trenutna_ladja)
        if self.velikost == 11:
            pogoj = (l == 4 or l == 7 or l == 10 or l == 12 or l == 14 or l == 16 or l == 17 or l == 18 or l == 19)
        #prva stevilka pove koliko ladij je, druga pa kaksne velikosti so
            return [(1, 4), (2, 3), (3, 2), (4, 1)], pogoj, l == 20
        if self.velikost == 8:
            pogoj = (l == 3 or l == 5 or l == 7 or l == 8 or l == 9)
            return [(1, 3), (2, 2), (3, 1)], pogoj, l == 10
        if self.velikost == 6:
            pogoj = (l == 2 or l == 3)
            return[(1, 2), (2, 1)], pogoj, l == 4
        if self.velikost == 2:
            pogoj = (l == 1)
            return[(1,1)], pogoj, l == 1
            
    def predlagaj_naslednji_kvadratek_za_sestavljanje_ladje(self, k):
        tocke = []
        for x in okolica(k, self.velikost):
            if x in nediagonalna_okolica(k, self.velikost) and x in self.proste_koordinate and self.mapa[x] == MORJE:
                tocke.append(x)
        return tocke

    def predlagaj_okolico_ladje(self, ladja):
        okol = set()
        for tocka in ladja:
            okol.update(self.predlagaj_naslednji_kvadratek_za_sestavljanje_ladje(tocka))
        for tocka in ladja:
            if tocka in okol:
                okol.remove(tocka)
        return list(okol)

    def izbrisi_iz_prostih_koordinat(self, okolica):
        for tocka in okolica:
            if tocka in self.proste_koordinate:
                self.proste_koordinate.remove(tocka)

    def dodaj_ladjico_rac(self, velikost):
        ladja = []
        zacetni = random.choice(self.proste_koordinate)
        self.mapa[zacetni] = LADJA
        ladja.append(zacetni)
        for _ in range(velikost - 1):
            if self.predlagaj_okolico_ladje(ladja) == []:
                self.izbrisi_ladjo()
                self.dodaj_ladjico_rac(velikost)
            else:
                naslednji = random.choice(self.predlagaj_okolico_ladje(ladja))
                self.mapa[naslednji] = LADJA
                ladja.append(naslednji)
        self.izbrisi_iz_prostih_koordinat(okolica_ladje(ladja, self.velikost))
        self.izbrisi_iz_prostih_koordinat(ladja)
        self.ladje.append(ladja)

    def izbrisi_ladjo(self):
        for tocka in self.trenutna_ladja:
            self.mapa[tocka] = MORJE

    def potopljena(self, koordinata):
        self.mapa[koordinata] = ZADETA_LADJA
        for ladja in self.ladje:
            if isinstance(ladja, list):
                if str(koordinata) in ladja:
                    a = len(ladja)
                    for str_tocka in ladja:
                        tocka = int(str_tocka)
                        if self.mapa[tocka] == LADJA:
                            a -= 1
                    return a == len(ladja)

    def oznaci_potopljeno(self, koordinata):
        for ladja in self.ladje:
            if str(koordinata) in ladja:
                if isinstance(ladja, list):
                    for str_tocka in ladja:
                        tocka = int(str_tocka)
                        self.mapa[tocka] = POTOPLJENA_LADJA
                    return ladja

    def konec_igre(self):
        a = 0
        for ladja in self.ladje:
            tocka = int(ladja[0])
            if self.mapa[tocka] == POTOPLJENA_LADJA:
                a += 1
        return a == len(self.ladje)
    
    def ugib_rac(self):
        mozni_ugibi = []
        neodkrito = []
        zadeto = []
        for tocka in range(len(self.odkrivanje)):
            if self.odkrivanje[tocka] == NEODKRITO:
                neodkrito.append(tocka)
            if self.odkrivanje[tocka] == ZADETA_LADJA:
                zadeto.append(tocka)
        for tocka in zadeto:
            for t in nediagonalna_okolica(tocka, self.velikost):
                if t in neodkrito:
                    mozni_ugibi.append(t)
        if mozni_ugibi == []:
            mozni_ugibi = neodkrito
        return random.choice(mozni_ugibi)

def poskus(napaden, napadalec, koordinata):
    if napaden.mapa[koordinata] == MORJE:
        napaden.mapa[koordinata] = ZAPRTO_POLJE
        napadalec.odkrivanje[koordinata] = ZAPRTO_POLJE
        return MORJE
    elif napaden.mapa[koordinata] == LADJA:
        if napaden.potopljena(koordinata):
            ladja = napaden.oznaci_potopljeno(koordinata)
            for str_tocka in ladja:
                tocka = int(str_tocka)
                napadalec.odkrivanje[tocka] = POTOPLJENA_LADJA
            for tocka in okolica_ladje(ladja, napaden.velikost):
                napadalec.odkrivanje[tocka] = ZAPRTO_POLJE
                napaden.mapa[tocka] = ZAPRTO_POLJE
            if napaden.konec_igre():
                return KONEC_IGRE
            else:
                return POTOPLJENA_LADJA
        else:
            napaden.mapa[koordinata] = ZADETA_LADJA
            napadalec.odkrivanje[koordinata] = ZADETA_LADJA
            return ZADETA_LADJA
    
def okolica(k, velikost):
    i = int(k)
    koordinata = [0, 0]
    koordinata[0] = i // velikost
    koordinata[1] = i % velikost 
    tocke = []
    for x in range(koordinata[0] - 1, koordinata[0] + 2):
        for y in range(koordinata[1] - 1, koordinata[1] + 2):
            if 0 <= x < velikost and 0 <= y < velikost:
                k1 = x * velikost + y
                if k1 != i:
                    tocke.append(k1)
    return tocke

def okolica_ladje(ladja, velikost):
    okol = set()
    for tocka in ladja:
        okol.update(okolica(tocka, velikost))
    for str_tocka in ladja:
        tocka = int(str_tocka)
        if tocka in okol:
            okol.remove(tocka)
    return list(okol)

def nediagonalna_okolica(k, velikost):
    okol = []
    for x in okolica(k, velikost):
        i = int(k)
        if x in [i + 1, i - 1, i + velikost, i - velikost]:
            okol.append(x)
    return okol 

def dodaj_mapo(igr):
    velikosti_ladij, _, _ = igr.velikosti_ladij_glede_na_velikost()
    for velikosti_ladje in velikosti_ladij:
        st = velikosti_ladje[0]
        vel = velikosti_ladje[1]
        for _ in range(st):
            igr.dodaj_ladjico_rac(vel)

def nova_igra(velikost):
    igr1 = Morje(velikost)
    igr2 = Morje(velikost)
    dodaj_mapo(igr1)
    return igr1, igr2




class Potapljanje:

    def __init__(self, datoteka_s_stanjem):
        self.datoteka_s_stanjem = datoteka_s_stanjem

    def prost_id_igre(self):
        return str(uuid.uuid4())

    def slovar_s_stanjem(self, igr1, igr2, id_igre, na_vrsti):
        velikost = igr1.velikost
        # mapa 1
        mapa1 = ''
        for v in igr1.mapa:
            mapa1 += v + '.'
        # odkrivanje 1
        odkrivanje1 = ''
        for v in igr1.odkrivanje:
            odkrivanje1 += v + '.'
        # mapa 2
        mapa2 = ''
        for v in igr2.mapa:
            mapa2 += v + '.'
        # odkrivanje 2
        odkrivanje2 = ''
        for v in igr2.odkrivanje:
            odkrivanje2 += v + '.'
        #trenutna ladja1
        trenutna_ladja1 = ''
        for k in igr1.trenutna_ladja:
            trenutna_ladja1 += str(k) + '.'
        #trenutna_ladja2
        trenutna_ladja2 = ''
        for k in igr2.trenutna_ladja:
            trenutna_ladja2 += str(k) + '.'
        #ladje1
        ladje1 = ''
        x = ''
        for ladja in igr1.ladje:
            for tocka in ladja:
                x += str(tocka) + '.'
            ladje1 += str(x) + ':'
            x = ''
        #ladje2
        ladje2 = ''
        x = ''
        for ladja in igr2.ladje:
            for tocka in ladja:
                x += str(tocka) + '.'
            ladje2 += str(x) + ':'
            x = ''
        return {
            id_igre : [
            {
                'mapa1' : mapa1, 
                'odkrivanje1' : odkrivanje1,
                'proste_koordinate' : igr1.proste_koordinate,
                'trenutna_ladja' : trenutna_ladja1,
                'ladje' : ladje1
            },
            {
                'mapa2' : mapa2,
                'odkrivanje2' : odkrivanje2,
                'proste_koordinate' : igr2.proste_koordinate,
                'trenutna_ladja' : trenutna_ladja2,
                'ladje' : ladje2
            },
            {
                'na_vrsti' : na_vrsti,
            },
            {
                'velikost': velikost
            }
            ]
        }

    def zapis_igre_v_datoteko(self, igr1, igr2, id_igre, na_vrsti):
        zapis = self.slovar_s_stanjem(igr1, igr2, id_igre, na_vrsti)
        with open(self.datoteka_s_stanjem, 'w', encoding='utf-8') as f:
            json.dump(zapis, f)
    
    def nalozi_igro_iz_datoteke(self, id_igre):
        with open(self.datoteka_s_stanjem, 'r', encoding='utf-8') as f:
            zapis = json.load(f)
        return zapis[id_igre]

    def nova_igra(self, velikost):
        igr1, igr2 = nova_igra(velikost)
        id_igre = self.prost_id_igre()
        self.zapis_igre_v_datoteko(igr1, igr2, id_igre, 0)
        return id_igre

    def nova_igra_duo(self, velikost):
        igr1 = Morje(velikost)
        igr2 = Morje(velikost)
        id_igre = self.prost_id_igre()
        self.zapis_igre_v_datoteko(igr1, igr2, id_igre, 0)
        return id_igre

    def sestavljanje_ladje(self, id_igre, koordinata, st):
        igr1, igr2, _ = self.igr_iz_id_igre(id_igre)
        if st == 2:
            igr2.mapa[koordinata] = LADJA
            igr2.trenutna_ladja.append(koordinata)
        else:
            igr1.mapa[koordinata] = LADJA
            igr1.trenutna_ladja.append(koordinata)
        self.zapis_igre_v_datoteko(igr1, igr2, id_igre, 0)

    def ugibaj(self, id_igre, koordinata):
        zapis = self.nalozi_igro_iz_datoteke(id_igre)
        igr1, igr2, na_vrsti = self.igr_iz_id_igre(id_igre)
        if na_vrsti % 2 == 0:
            rezultat = poskus(igr1, igr2, int(koordinata))
        else:
            rezultat = poskus(igr2, igr1, int(koordinata))
        na_vrsti += 1
        self.zapis_igre_v_datoteko(igr1, igr2, id_igre, na_vrsti)
        return rezultat
        
    def igr_iz_id_igre(self, id_igre):
        zapis = self.nalozi_igro_iz_datoteke(id_igre)
        na_vrsti = zapis[2]['na_vrsti']
        velikost = zapis[3]['velikost']
        mapa1_spremenjena = zapis[0]['mapa1'].split('.')[:-1]
        odkrivanje1_spremenjena = zapis[0]['odkrivanje1'].split('.')[:-1]
        mapa2_spremenjena = zapis[1]['mapa2'].split('.')[:-1]
        odkrivanje2_spremenjena = zapis[1]['odkrivanje2'].split('.')[:-1]
        proste_koordinate1 = zapis[0]['proste_koordinate']
        proste_koordinate2 = zapis[1]['proste_koordinate']
        trenutna_ladja1 = zapis[0]['trenutna_ladja'].split('.')[:-1]
        trenutna_ladja11 = []
        for x in trenutna_ladja1:
            trenutna_ladja11.append(int(x))
        trenutna_ladja2 = zapis[1]['trenutna_ladja'].split('.')[:-1]
        trenutna_ladja22 = []
        for x in trenutna_ladja2:
            trenutna_ladja22.append(int(x))
        ladje1 = zapis[0]['ladje'].split(':')[:-1]
        ladje11 = []
        for ladja in ladje1:
            if isinstance(ladja, str):
                x = ladja.split('.')[:-1]
                ladje11.append(x)
        ladje2 = zapis[1]['ladje'].split(':')[:-1]
        ladje22 = []
        for ladja in ladje2:
            if isinstance(ladja, str):
                x = ladja.split('.')[:-1]
                ladje22.append(x)
        igr1 = Morje(velikost, mapa1_spremenjena, odkrivanje1_spremenjena, proste_koordinate1, trenutna_ladja11, ladje11)
        igr2 = Morje(velikost, mapa2_spremenjena, odkrivanje2_spremenjena, proste_koordinate2, trenutna_ladja22, ladje22)
        return igr1, igr2, na_vrsti

def sestavi(id_igre, izbrana_tocka, potapljanje, st):
    potapljanje.sestavljanje_ladje(id_igre, izbrana_tocka, st)
    igr1, igr2, _ = potapljanje.igr_iz_id_igre(id_igre)
    if st == 2:
        igr = igr2
    if st == 1:
        igr = igr1
    _, pogoj, zadnji_pogoj = igr.velikosti_ladij_glede_na_velikost()
    if pogoj or zadnji_pogoj:
        igr.izbrisi_iz_prostih_koordinat(igr.trenutna_ladja)
        igr.izbrisi_iz_prostih_koordinat(okolica_ladje(igr.trenutna_ladja, igr.velikost))
        igr.ladje.append(igr.trenutna_ladja)
        igr.trenutna_ladja = []
        potapljanje.zapis_igre_v_datoteko(igr1, igr2, id_igre, 0)
    return pogoj, zadnji_pogoj

def zapisi_ime(datoteka, ime, st):
    if st == 1:
        if ime == '':
            ime = 'Prvi igralec'
        zapis = {'imena': {'1': ime}}
        with open(datoteka, 'w', encoding='utf-8') as f:
            json.dump(zapis, f)
    else:
        if ime == '':
            ime = 'Drugi igralec'
        with open(datoteka, 'r', encoding='utf-8') as f:
            zapis = json.load(f)
            zapis['imena'].update({'2': ime})
        with open(datoteka, 'w', encoding='utf-8') as dat:
            json.dump(zapis, dat)

def preberi_ime(datoteka, st):
    with open(datoteka, 'r', encoding='utf-8') as f:
        imena = json.load(f)['imena']
        ime = imena[str(st)]
    return ime

def prestej_nezadete_ladje(igr):
    a = len(igr.ladje)
    for ladja in igr.ladje:
        for str_tocka in ladja:
            tocka = int(str_tocka)
            if igr.mapa[tocka] == ZADETA_LADJA or igr.mapa[tocka] == POTOPLJENA_LADJA:
                a -= 1
                break
    return a
