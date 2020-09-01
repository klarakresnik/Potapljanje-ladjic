import bottle
import model
import napisi_zacetno_tabelo
import napisi_tabelo_naprej
import napisi_tabelo_za_igro
import napisi_rezultat
import konec

SKRIVNOST = 'iwillnevertell'

potapljanje = model.Potapljanje('stanje.json')


@bottle.get('/')
def index():
    return bottle.template('index.tpl')


@bottle.post('/velikost_polja/')
def velikost_polja():
    return bottle.template('velikost_polja.tpl')

@bottle.post('/velikost_polja_duo/')
def velikost_polja():
    return bottle.template('velikost_polja_duo.tpl')


@bottle.post('/nova_igra/')
def nova_igra():
    velikost = int(bottle.request.forms.get('velikost'))
    id_igre = potapljanje.nova_igra(velikost)
    bottle.response.set_cookie('id_igre', 'id_igre{}'.format(id_igre), secret=SKRIVNOST, path='/')
    bottle.redirect('/oblikovanje_mape/')


@bottle.post('/nova_igra_duo/')
def nova_igra():
    velikost = int(bottle.request.forms.get('velikost'))
    id_igre = potapljanje.nova_igra_duo(velikost)
    bottle.response.set_cookie('id_igre', 'id_igre{}'.format(id_igre), secret=SKRIVNOST, path='/')
    bottle.redirect('/ime_prvi/')


@bottle.get('/oblikovanje_mape/')
def izbira():
    return bottle.template('postavitev_polja.tpl')


@bottle.get('/ime_prvi/')
def ime_prvi():
    return bottle.template('ime_prvi.tpl')


@bottle.get('/ime_drugi/')
def ime_drugi():
    return bottle.template('ime_drugi.tpl')


@bottle.post('/postavitev_polja_prvi/')
def postavitev_polja_prvi():
    ime = bottle.request.forms.getunicode('igr1')
    model.zapisi_ime('ime.json', ime, 1)
    return bottle.template('postavitev_polja_prvi.tpl')


@bottle.post('/postavitev_polja_drugi/')
def postavitev_polja_drugi():
    ime = bottle.request.forms.getunicode('igr2')
    model.zapisi_ime('ime.json', ime, 2)
    return bottle.template('postavitev_polja_drugi.tpl')


@bottle.post('/rac_polje/')
def rac_polje():
    id_igre = bottle.request.get_cookie('id_igre', secret=SKRIVNOST)[7:]
    igr1, igr2, _ = potapljanje.igr_iz_id_igre(id_igre)
    model.dodaj_mapo(igr2)
    potapljanje.zapis_igre_v_datoteko(igr1, igr2, id_igre, 0)
    igr1, igr2, na_vrsti = potapljanje.igr_iz_id_igre(id_igre)
    napisi_tabelo_za_igro.tabela_za_igro('igra.tpl', igr1.velikost, igr1, igr2, 0, na_vrsti)
    return bottle.template('igra.tpl')

@bottle.post('/rac_polje_prvi/')
def rac_polje():
    id_igre = bottle.request.get_cookie('id_igre', secret=SKRIVNOST)[7:]
    igr1, igr2, _ = potapljanje.igr_iz_id_igre(id_igre)
    model.dodaj_mapo(igr1)
    potapljanje.zapis_igre_v_datoteko(igr1, igr2, id_igre, 0)
    igr1, igr2, _ = potapljanje.igr_iz_id_igre(id_igre)
    return bottle.template('ime_drugi.tpl')

@bottle.post('/rac_polje_drugi/')
def rac_polje():
    id_igre = bottle.request.get_cookie('id_igre', secret=SKRIVNOST)[7:]
    igr1, igr2, _ = potapljanje.igr_iz_id_igre(id_igre)
    model.dodaj_mapo(igr2)
    potapljanje.zapis_igre_v_datoteko(igr1, igr2, id_igre, 0)
    igr1, igr2, na_vrsti = potapljanje.igr_iz_id_igre(id_igre)
    napisi_tabelo_za_igro.tabela_za_igro('igra.tpl', igr1.velikost, igr2, igr1, 1, na_vrsti)
    return bottle.template('igra.tpl')


@bottle.post('/zacetna_tabela/')
def zacetna():
    id_igre = bottle.request.get_cookie('id_igre', secret=SKRIVNOST)[7:]
    _, igr2, _ = potapljanje.igr_iz_id_igre(id_igre)
    napisi_zacetno_tabelo.napisi_zacetno_tabelo('zacetna_tabela.tpl', igr2, igr2.velikost, 0)
    return bottle.template('zacetna_tabela.tpl')

@bottle.post('/zacetna_tabela_prvi/')
def zacetna():
    id_igre = bottle.request.get_cookie('id_igre', secret=SKRIVNOST)[7:]
    igr1, _, _ = potapljanje.igr_iz_id_igre(id_igre)
    napisi_zacetno_tabelo.napisi_zacetno_tabelo('zacetna_tabela.tpl', igr1, igr1.velikost, 1)
    return bottle.template('zacetna_tabela.tpl')


@bottle.post('/zacetna_tabela_drugi/')
def zacetna():
    id_igre = bottle.request.get_cookie('id_igre', secret=SKRIVNOST)[7:]
    _, igr2, _ = potapljanje.igr_iz_id_igre(id_igre)
    napisi_zacetno_tabelo.napisi_zacetno_tabelo('zacetna_tabela.tpl', igr2, igr2.velikost, 2)
    return bottle.template('zacetna_tabela.tpl')


@bottle.post('/oblikovanje_mape/ladja/')
def dodajanje_ladjice():
    id_igre = bottle.request.get_cookie('id_igre', secret=SKRIVNOST)[7:]
    izbrana_tocka = int(bottle.request.forms.get('ladja'))
    pogoj, zadnji_pogoj = model.sestavi(id_igre, izbrana_tocka, potapljanje, 2)
    igr1, igr2, na_vrsti = potapljanje.igr_iz_id_igre(id_igre)
    if zadnji_pogoj:
        napisi_tabelo_za_igro.tabela_za_igro('igra.tpl', igr1.velikost, igr1, igr2, 0, na_vrsti)
        return bottle.template('igra.tpl')
    if pogoj:
        napisi_zacetno_tabelo.napisi_zacetno_tabelo('zacetna_tabela.tpl', igr2, igr2.velikost, 0)
        return bottle.template('zacetna_tabela.tpl')
    napisi_tabelo_naprej.napisi_tabelo_naprej('tabela_naprej.tpl', igr2, igr2.velikost, 0)
    return bottle.template('tabela_naprej.tpl')


@bottle.post('/oblikovanje_mape/ladja_prvi/')
def dodajanje_ladjice():
    id_igre = bottle.request.get_cookie('id_igre', secret=SKRIVNOST)[7:]
    izbrana_tocka = int(bottle.request.forms.get('ladja'))
    pogoj, zadnji_pogoj = model.sestavi(id_igre, izbrana_tocka, potapljanje, 1)
    igr1, _, _ = potapljanje.igr_iz_id_igre(id_igre)
    if zadnji_pogoj:
        return bottle.template('ime_drugi.tpl')
    if pogoj:
        napisi_zacetno_tabelo.napisi_zacetno_tabelo('zacetna_tabela.tpl', igr1, igr1.velikost, 1)
        return bottle.template('zacetna_tabela.tpl')
    napisi_tabelo_naprej.napisi_tabelo_naprej('tabela_naprej.tpl', igr1, igr1.velikost, 1)
    return bottle.template('tabela_naprej.tpl')


@bottle.post('/oblikovanje_mape/ladja_drugi/')
def dodajanje_ladjice():
    id_igre = bottle.request.get_cookie('id_igre', secret=SKRIVNOST)[7:]
    izbrana_tocka = int(bottle.request.forms.get('ladja'))
    pogoj, zadnji_pogoj = model.sestavi(id_igre, izbrana_tocka, potapljanje, 2)
    igr1, igr2, na_vrsti = potapljanje.igr_iz_id_igre(id_igre)
    if zadnji_pogoj:
        napisi_tabelo_za_igro.tabela_za_igro('igra.tpl', igr1.velikost, igr1, igr2, 1, na_vrsti)
        return bottle.template('igra.tpl')
    if pogoj:
        napisi_zacetno_tabelo.napisi_zacetno_tabelo('zacetna_tabela.tpl', igr2, igr2.velikost, 2)
        return bottle.template('zacetna_tabela.tpl')
    napisi_tabelo_naprej.napisi_tabelo_naprej('tabela_naprej.tpl', igr2, igr2.velikost, 2)
    return bottle.template('tabela_naprej.tpl')


@bottle.post('/igra/')
def igraj():
    id_igre = bottle.request.get_cookie('id_igre', secret=SKRIVNOST)[7:]
    koordinata = int(bottle.request.forms.get('ladja'))
    rezultat = potapljanje.ugibaj(id_igre, koordinata)
    if rezultat == model.KONEC_IGRE:
        return bottle.template('konec1.tpl')
    else:
        igr1, igr2, _ = potapljanje.igr_iz_id_igre(id_igre)
        koordinata = igr1.ugib_rac()
        rezultat = potapljanje.ugibaj(id_igre, koordinata)
        igr1, igr2, _ = potapljanje.igr_iz_id_igre(id_igre)
        if rezultat == model.KONEC_IGRE:
            konec.konec('konec.tpl', igr1, igr2, 1, True)
            return bottle.template('konec.tpl')
        else:
            igr1, igr2, na_vrsti = potapljanje.igr_iz_id_igre(id_igre)
            napisi_tabelo_za_igro.tabela_za_igro('igra.tpl', igr1.velikost, igr1, igr2, 0, na_vrsti)
            return bottle.template('igra.tpl')

@bottle.post('/igra_duo/')
def igraj():
    id_igre = bottle.request.get_cookie('id_igre', secret=SKRIVNOST)[7:]
    koordinata = int(bottle.request.forms.get('ladja'))
    rezultat = potapljanje.ugibaj(id_igre, koordinata)
    igr1, igr2, na_vrsti = potapljanje.igr_iz_id_igre(id_igre)
    if rezultat == model.KONEC_IGRE:
        konec.konec('konec.tpl', igr1, igr2, na_vrsti - 1, False)
        return bottle.template('konec.tpl')
    else:
        napisi_rezultat.rezultat('napisi_rezultat.tpl', rezultat, na_vrsti)
        return bottle.template('napisi_rezultat.tpl')

@bottle.post('/napisi_rezultat/')
def preklopi_na_naslednjega():
    id_igre = bottle.request.get_cookie('id_igre', secret=SKRIVNOST)[7:43]
    igr1, igr2, na_vrsti = potapljanje.igr_iz_id_igre(id_igre)
    napisi_tabelo_za_igro.tabela_za_igro('igra.tpl', igr1.velikost, igr1, igr2, 1, na_vrsti)
    return bottle.template('igra.tpl')



bottle.run(reloader=True, debug=True)