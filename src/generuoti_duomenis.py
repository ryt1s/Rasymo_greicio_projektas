import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

np.random.seed(67)
random.seed(67)

VARTOTOJU_KIEKIS = 50
SESIJU_PER_VARTOTOJA = 30

PRADZIOS_DATA = datetime(2025, 1, 1)

duomenys = []

# -----------------------------
# DUOMENŲ GENERAVIMAS
# -----------------------------
for vartotojo_id in range(1, VARTOTOJU_KIEKIS + 1):

    # kiekvienas vartotojas turi skirtingą pradinį lygį
    bazinis_wpm = np.random.normal(40, 10)  # pradedantysis / vidutinis
    mokymosi_tempo = np.random.uniform(0.1, 0.5)

    for sesijos_id in range(1, SESIJU_PER_VARTOTOJA + 1):

        # laiko progresas
        data = PRADZIOS_DATA + timedelta(days=sesijos_id)

        # tobulėjimas laikui bėgant
        progresas = np.log1p(sesijos_id) * mokymosi_tempo * 10

        # atsitiktinumas (geri / blogi pasirodymai)
        triuksmas = np.random.normal(0, 5)

        wpm = bazinis_wpm + progresas + triuksmas
        wpm = max(10, wpm)

        # tikslumas šiek tiek krenta kai didėja greitis
        tikslumas = 98 - (wpm * 0.2) + np.random.normal(0, 2)
        tikslumas = np.clip(tikslumas, 70, 100)

        # klaidos priklauso nuo tikslumo
        klaidos = max(0, int((100 - tikslumas) / 5 + np.random.randint(0, 3)))

        trukme = 60  # 1 minutės testas

        sudetingumas = random.choice(["lengvas", "vidutinis", "sunkus"])

        duomenys.append([
            vartotojo_id,
            sesijos_id,
            data,
            round(wpm, 2),
            round(tikslumas, 2),
            klaidos,
            trukme,
            sudetingumas
        ])

# -----------------------------
# DUOMENŲ RINKINYS
# -----------------------------
df = pd.DataFrame(duomenys, columns=[
    "vartotojo_id",
    "sesijos_id",
    "data",
    "wpm",
    "tikslumas",
    "klaidos",
    "trukme_sekundemis",
    "sudetingumas"
])

# išsaugome CSV failą
df.to_csv("../data/rasymo_sesija.csv", index=False)

print("Duomenų rinkinys sukurtas sėkmingai!")
print(df.head())