import model

def rezultat(datoteka, rezultat, na_vrsti):
    with open(datoteka, 'w', encoding='utf-8') as dat:
        dat.write("%rebase('base.tpl')\n")
        if rezultat == 'Z':
            dat.write('Zadel si ladjo!!\n<br>')
        if rezultat == 'M':
            dat.write('Zgrešil si, toda strel je bil dober.\n<br>\n')
        if rezultat == 'X':
            dat.write('Ladjo si potopil.\n<br>')
        if na_vrsti % 2 == 0:
            ime = str(model.preberi_ime('ime.json', 2))
            dat.write('Po pritisku na gumb se bo pokazalo polje igralca ' + ime + ':\n<br>' +
                '<form action="/napisi_rezultat/" method="post">\n' +
                '<button style="font-size:16px; padding:10px, 20px;" type="submit">' + ime + '</button>\n' +
                '</form>')
        else:
            ime = model.preberi_ime('ime.json', 1)
            dat.write('Po pritisku na gumb se bo pokazalo polje igralca ' + str(ime) + ':\n<br>' +
                '<form action="/napisi_rezultat/" method="post">\n' +
                '<button style="font-size:16px; padding:10px, 20px;" type="submit">' + str(ime) + '</button>' +
                '</form>')


