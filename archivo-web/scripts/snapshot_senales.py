import json, os, re, sys
carpeta, modelo, salida = sys.argv[1:4]
PUB = ["clearance_relativo","contratos_adquisicion","contratos_ancla","drop_semanal","propietarios_atendidos","open_cierre","margen_contribucion","listados_7d","recortes_propios","recorte_medio_casa","ventas_salida","lag_cierre","fuera_web","opciones_open"]
QUITAR = {"notas","porque","formato","medicion"}
def fuera(k):
    return k in QUITAR or (re.match(r"(nota|aviso)", k) and k != "aviso_en") or k.endswith("_nota") or k.startswith("lectura")
def limpia(o):
    if isinstance(o, dict): return {k: limpia(v) for k, v in o.items() if not fuera(k)}
    if isinstance(o, list): return [limpia(x) for x in o]
    return o
def senal(d):
    r = {}
    for k, v in d.items():
        if fuera(k): continue
        if k == "puntos" and isinstance(v, list):
            r[k] = [{a: b for a, b in p.items() if not fuera(a) and not isinstance(b, (list, dict)) and not (isinstance(b, str) and len(b) > 100)} for p in v]
        else: r[k] = limpia(v)
    return r
res = {}
for s in PUB:
    p = os.path.join(carpeta, s + ".json")
    if os.path.exists(p): res[s] = senal(json.load(open(p, encoding="utf-8")))
    else: print("aviso: falta", s)
os.makedirs(salida, exist_ok=True)
json.dump(res, open(os.path.join(salida, "senales.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
json.dump(json.load(open(modelo, encoding="utf-8")), open(os.path.join(salida, "modelo.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
