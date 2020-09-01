import model

def konec(datoteka, igr1, igr2, na_vrsti, rac):
    velikost = igr1.velikost
    with open(datoteka, 'w', encoding='utf-8') as dat:
        dat.write("%rebase('base.tpl')\n")
        if rac:
            dat.write('<b>Izgubil si.</b> Več sreče naslednjič!\n<br>')
            zmagovalec = igr1
            porazenec = igr2
        elif na_vrsti % 2 == 1:
            st1 = 1
            st2 = 2
            zmagovalec = igr1
            porazenec = igr2
        else:
            st1 = 2
            st2 = 1
            zmagovalec = igr2
            porazenec = igr1
        if rac:
            ime = 'Računalnik'
        else:
            ime = model.preberi_ime('ime.json', st1)
        dat.write('Zmagal je <b>' + str(ime) + ':</b>')
        dat.write('<table>\n')
        for x in range(velikost ** 2):
            stanje = zmagovalec.mapa[x]
            if stanje == model.LADJA:
                vsebina = '<button class="velikost_gumba" style="background-color:#e1e3e1" type="button" disabled><i class="material-icons" style="color:black;">directions_boat</i></button>'                   
            if stanje == model.ZAPRTO_POLJE:
                vsebina = '<button class="velikost_gumba" style="background-color:#67b4cf; color=#000000" type="button" disabled>X</button>'
            if stanje == model.ZADETA_LADJA:
                vsebina = '<button class="velikost_gumba" style="background-color:#f0a400" type="button" disabled><i class="material-icons" style="color:black;">directions_boat</i></button>'
            if stanje == model.POTOPLJENA_LADJA:
                vsebina = '<button class="velikost_gumba" style="background-color:#d90000" type="button" disabled><i class="material-icons" style="color:black;">directions_boat</i></button>'
            if stanje == model.MORJE:
                vsebina = '<button class="velikost_gumba" style="background-color:#3394b5;" type="button" disabled></button>'
            if x % velikost == 0:
               dat.write('<tr>\n')
            dat.write('<td>')
            dat.write(vsebina)
            dat.write('</td>\n')
            if (x + 1) % velikost == 0:
                dat.write('</tr>\n')
        dat.write('</table>\n<br>')
        if rac:
            dat.write('Tvoje polje:')
        else:
            ime = model.preberi_ime('ime.json', st2)
            dat.write('Polje igralca ' + str(ime) + ':\n')
        dat.write('<table>\n')
        for x in range(velikost ** 2):
            stanje = porazenec.mapa[x]
            if stanje == model.ZAPRTO_POLJE:
                vsebina = '<button class="velikost_gumba" style="background-color:#67b4cf; color=#000000" type="button" disabled>X</button>'
            if stanje == model.ZADETA_LADJA:
                vsebina = '<button class="velikost_gumba" style="background-color:#f0a400" type="button" disabled><i class="material-icons" style="color:black;">directions_boat</i></button>'
            if stanje == model.POTOPLJENA_LADJA:
                vsebina = '<button class="velikost_gumba" style="background-color:#d90000" type="button" disabled><i class="material-icons" style="color:black;">directions_boat</i></button>'
            if stanje == model.MORJE:
                vsebina = '<button class="velikost_gumba" style="background-color:#3394b5;" type="button" disabled></button>'
            if x % velikost == 0:
               dat.write('<tr>\n')
            dat.write('<td>')
            dat.write(vsebina)
            dat.write('</td>\n')
            if (x + 1) % velikost == 0:
                dat.write('</tr>\n')
        dat.write('</table>\n<br>')
        dat.write('Si še za eno igro?\n<br>\n' +
            '<form action="/velikost_polja/" method="post">' +
            '<button type="submit" style="font-size:16px; padding:10px, 20px;">Igra proti računalniku</button>' +
            '</form>\n'+
            '<form action="/velikost_polja_duo/" method="post">'+
            '<button type="submit" style="font-size:16px; padding:10px, 20px;">Igra proti prijatelju</button>'+
            '</form>')