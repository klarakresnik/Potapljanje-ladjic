import model

def napisi_tabelo_naprej(datoteka, morje, velikost, st):
    vsebina = ''
    with open(datoteka, 'w', encoding='utf-8') as dat:
        dat.write("%rebase('base_za_sestavljanje_ladjic" + str(velikost) + ".tpl')\n")
        dat.write('Izberi si nadaljne kvadratke tvoje ladjice.\n')
        if st == 0:
            dat.write('<form action="/oblikovanje_mape/ladja/" method="post">\n')
        if st == 1:
            dat.write('<form action="/oblikovanje_mape/ladja_prvi/" method="post">\n')
        if st == 2:
            dat.write('<form action="/oblikovanje_mape/ladja_drugi/" method="post">\n')
        dat.write('<div style="margin:20px">\n<table>\n')
        for x in range(velikost ** 2):
            stanje = morje.mapa[x]
            ime = str(x)
            if x in morje.predlagaj_okolico_ladje(morje.trenutna_ladja):
                vsebina = '<button class="velikost_gumba" style="background-color:#3394b5;" name="ladja" type="submit" value="' + ime + '"></button>'
            else:
                if stanje == model.MORJE:
                    vsebina = '<button class="velikost_gumba" style="background-color:##4bafd1;" type="button" disabled></button>'
                if stanje == model.LADJA:
                    vsebina = '<button class="velikost_gumba" style="background-color:#e1e3e1" type="button" disabled><i class="material-icons" style="color:black;">directions_boat</i></button>'                   
            if x % velikost == 0:
                dat.write('<tr>\n')
            dat.write('<td>')
            dat.write(vsebina)
            dat.write('</td>\n')
            if (x + 1) % velikost == 0:
                dat.write('</tr>\n')
        dat.write('</div>\n</table>\n</div>\n</form>\n')