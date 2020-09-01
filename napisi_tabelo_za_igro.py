import model

def tabela_za_igro(datoteka, velikost, igr1, igr2, st, na_vrsti):
    with open(datoteka, 'w', encoding='utf-8') as dat:
        dat.write("%rebase('base.tpl')\n")
        if st == 0:
            dat.write('<form action="/igra/" method="post">\n')
            igr = igr2
            nasprotnik = igr1
        if st == 1:
            if na_vrsti % 2 == 0:
                igr = igr2
                nasprotnik = igr1
                dat.write('<form action="/igra_duo/" method="post">\n')
                ime = model.preberi_ime('ime.json', 2)
            else:
                igr = igr1
                nasprotnik = igr2
                dat.write('<form action="/igra_duo/" method="post">\n')
                ime = model.preberi_ime('ime.json', 1)
            dat.write('Na vrsti je <b>' + str(ime) + '</b>.\n<br>')
        a = model.prestej_nezadete_ladje(nasprotnik)
        b = model.prestej_nezadete_ladje(igr)
        dat.write('Najti moraš <b>' + str(a) + '</b> ladij.\n<br>')
        dat.write('Ti imaš še <b>' + str(b) + '</b> neodkritih ladij.\n<br>\n<br>')
        dat.write('<div style="float:left; margin:30px"><h3>Mapa nasprotnika:</h3>')
        dat.write('<table>\n')
        for x in range(velikost ** 2):
            stanje = igr.odkrivanje[x]
            ime = str(x)
            if igr.odkrivanje[x] != model.NEODKRITO:
                if stanje == model.ZAPRTO_POLJE:
                    vsebina = '<button class="velikost_gumba" style="background-color:#3394b5;" type="button" disabled></button>'
                if stanje == model.ZADETA_LADJA:
                    vsebina = '<button class="velikost_gumba" style="background-color:#f0a400" type="button" disabled><i class="material-icons" style="color:black;">directions_boat</i></button>'
                if stanje == model.POTOPLJENA_LADJA:
                    vsebina = '<button class="velikost_gumba" style="background-color:#d90000" type="button" disabled><i class="material-icons" style="color:black;">directions_boat</i></button>'
            else:
                vsebina = '<button class="velikost_gumba" name="ladja" type="submit" value="' + ime + '">?</button>'
            if x % velikost == 0:
               dat.write('<tr>\n')
            dat.write('<td>')
            dat.write(vsebina)
            dat.write('</td>\n')
            if (x + 1) % velikost == 0:
                dat.write('</tr>\n')
        if st == 0:
            dat.write('</form>\n')
        dat.write('</table></div><br>\n')
        dat.write('<div style="float:center; margin:20px">\n<h3>Tvoja mapa:<h3><table>\n')
        for x in range(velikost ** 2):
            stanje = igr.mapa[x]
            if stanje != model.LADJA:
                if stanje == model.MORJE:
                    vsebina = '<button class="velikost_gumba" style="background-color:#3394b5;" type="button" disabled></button>'
                if stanje == model.ZAPRTO_POLJE:
                    vsebina = '<button class="velikost_gumba" style="background-color:#67b4cf; color=#000000" type="button" disabled>X</button>'
                if stanje == model.ZADETA_LADJA:
                    vsebina = '<button class="velikost_gumba" style="background-color:#f0a400" type="button" disabled><i class="material-icons" style="color:black;">directions_boat</i></button>'
                if stanje == model.POTOPLJENA_LADJA:
                    vsebina = '<button class="velikost_gumba" style="background-color:#d90000" type="button" disabled><i class="material-icons" style="color:black;">directions_boat</i></button>'
            else:    
                vsebina = '<button class="velikost_gumba" style="background-color:#e1e3e1" type="button" disabled><i class="material-icons" style="color:black;">directions_boat</i></button>'                   
            if x % velikost == 0:
               dat.write('<tr>\n')
            dat.write('<td>')
            dat.write(vsebina)
            dat.write('</td>\n')
            if (x + 1) % velikost == 0:
                dat.write('</tr>\n')
        dat.write('</table>\n</div>\n<br>')