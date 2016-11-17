# Static Values for PLAC processing

ignored_text = """
mlk
msrk
ksrk
tksrk
maalaiskunta
maaseurakunta
kaupunkiseurakunta
tuomiokirkkoseurakunta
rykmentti
pitäjä
kylä

hl
tl
ol
ul
vpl
vl

tai

de
las

"""

auto_combines = [
    "n pitäjä",
    "n srk",
    "n seurakunta",
    "n maalaiskunta",
    "n maaseurakunta",
    "n kaupunkiseurakunta",
    "n tuomiokirkkoseurakunta",
    "n rykmentti",
    "n kylä",
    "n mlk",
    "n msrk",
    "n ksrk",
]

countries = {
    "Finland", "Suomi",
    "USA", "Yhdysvallat",
    "Kanada",
    "Alankomaat",
    "Ruotsi",
    "Australia",
    "Venäjä",
    "Eesti", "Viro",
}

