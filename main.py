from pathlib import Path
import csv

from arca_8126.cabecera import (
    CUIT,
    generar_cabecera,
    obtener_hora_actual,
    obtener_periodo_anterior,
    formatear_cantidad_registros,
)
from arca_8126.titular_cuenta import generar_titular_cuenta
from arca_8126.cuentas_asociadas import generar_cuentas_asociadas
from arca_8126.otros_integrantes_cuenta import generar_otros_integrantes
from arca_8126.movimientos_mensuales import generar_movimientos_con_detalle
from arca_8126.detalle_movimientos_mensuales import corresponde_detalle


# ========== RUTAS DE ENTRADA (cambiar aca cuando haya archivos nuevos) ==========
CARPETA_DATOS = Path(r"C:\Users\arigr\Downloads")
RUTA_TITULARES = CARPETA_DATOS / "arca_f8126_30712345689_20260604-06_titulares.csv"
RUTA_CUENTAS = CARPETA_DATOS / "arca_f8126_30712345689_20260604-06_cuentas.csv"
RUTA_MOVIMIENTOS = CARPETA_DATOS / "arca_f8126_30712345689_20260604-06_movimientos.csv"
RUTA_OTROS_INTEGRANTES = Path(r"C:\Users\arigr\OneDrive\Desktop\formulario 8126\datos_otros_integrantes.txt")

# ========== RUTA DE SALIDA (cambiar si el archivo se genera en otro lugar) ==========
RUTA_SALIDA = Path(r"C:\Users\arigr\OneDrive\Desktop\formulario 8126\arca_8126\F8126.30718725840.20260600.0000.txt")


# Arma la lista final de lineas agregando la cantidad de registros a la cabecera
def construir_lineas(resultados: list[str]) -> list[str]:
    if not resultados:
        return []

    total_registros = len(resultados)
    cabecera_con_sufijo = resultados[0] + formatear_cantidad_registros(total_registros)
    return [cabecera_con_sufijo] + resultados[1:]


# Convierte una fila del CSV de titulares en un dict de campos (el cuit con 30 es tipo de doc 80)
def parsear_titular_csv(fila: dict) -> dict:
    cuit = str(fila.get("cuit_titular", "")).strip()
    tipo_persona = str(fila.get("tipo_persona", "")).strip()
    origen = "N"
    tipo_documento = "80" if cuit[:2] == "30" else ""
    codigo_pais_3 = "200"
    return {
        "tipo": tipo_persona,
        "origen": origen,
        "tipo_documento": tipo_documento,
        "codigo_pais_3": codigo_pais_3,
        "cuit": cuit,
        "numero_otro_documento": "",
        "nombre": str(fila.get("denominacion", "")).strip(),
        "id_cuenta_cliente": str(fila.get("id_cliente", "")).strip(),
        "fecha_alta": str(fila.get("fecha_alta_cuenta", "")).strip(),
        "tipo_operacion": str(fila.get("tipo_operacion", "")).strip(),
        "signo_saldo_pesos": "0",
        "saldos_pesos": fila.get("saldo_pesos", "0"),
        "signo_saldo_me": "0",
        "saldos_me": "",
        "signo_saldo_mv": "0",
        "saldos_mv": "",
        "cantidad_cuentas": str(fila.get("cant_cuentas", "1")).strip(),
    }


# Convierte un texto de saldos separados por comas en una lista de enteros
def saldos(dato: str) -> list:
    return [int(x) for x in dato.split(",")] if dato else []


# Convierte una fila del CSV de cuentas en un dict de campos, enlazada a su titular
def parsear_cuentas_csv(fila: dict) -> dict:
    return {
        "cuit_titular": str(fila.get("cuit_titular", "")).strip(),
        "tipo_cuenta": str(fila.get("tipo_cuenta", "")).strip(),
        "cvu_cbu": str(fila.get("cvu", "")).strip(),
        "identificador_otro_tipo": "",
        "cantidad_integrantes": str(fila.get("cant_integrantes", "1")).strip(),
        "emisor_denominacion": str(fila.get("emisor_denominacion", "")).strip(),
        "por_orden_terceros": str(fila.get("por_cuenta_y_orden_de_terceros", "0")).strip(),
        "denominacion_tercero": str(fila.get("tercero_denominacion", "")).strip(),
        "signo_saldo_pesos": "0",
        "saldos_pesos": str(fila.get("saldo_pesos", "0")).strip(),
        "signo_saldo_me": "0",
        "saldos_me": "",
        "signo_saldo_mv": "0",
        "saldos_mv": "",
    }


# Convierte una linea de otros integrantes (separada por ";") en un dict
def parsear_otros_integrantes(linea: str) -> dict:
    partes = linea.strip().split(";")
    return {
        "origen": partes[0],
        "tipo_documento": partes[1],
        "codigo_pais_3": partes[2],
        "cuit": partes[3],
        "numero_otro_documento": partes[4],
        "nombre": partes[5],
        "caracter": partes[6],
    }


# BLOQUE 1: arma la cabecera y genera un registro 02 (titular) por cada fila del CSV de titulares
periodo = obtener_periodo_anterior()
hora = obtener_hora_actual()
cabecera = generar_cabecera(CUIT, periodo, hora)

# Lee el CSV de titulares y genera un registro 02 por cada fila
titulares = []
titulares_cuit = []
with RUTA_TITULARES.open(encoding="utf-8", newline="") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        datos = parsear_titular_csv(fila)
        titulares_cuit.append(datos["cuit"])
        titulares.append(
            generar_titular_cuenta(
                tipo=datos["tipo"],
                origen=datos["origen"],
                tipo_documento=datos["tipo_documento"],
                codigo_pais_3=datos["codigo_pais_3"],
                cuit=datos["cuit"],
                numero_otro_documento=datos["numero_otro_documento"],
                nombre=datos["nombre"],
                id_cuenta_cliente=datos["id_cuenta_cliente"],
                fecha_alta=datos["fecha_alta"],
                tipo_operacion=datos["tipo_operacion"],
                signo_saldo_pesos=datos["signo_saldo_pesos"],
                saldos_pesos=saldos(datos["saldos_pesos"]),
                signo_saldo_me=datos["signo_saldo_me"],
                saldos_me=saldos(datos["saldos_me"]),
                signo_saldo_mv=datos["signo_saldo_mv"],
                saldos_mv=saldos(datos["saldos_mv"]),
                cantidad_cuentas=int(datos["cantidad_cuentas"]),
            )
        )

# Lee el CSV de cuentas y genera un registro 03 por cada fila, agrupadas por titular
cuentas_por_cuit = {}
with RUTA_CUENTAS.open(encoding="utf-8", newline="") as archivo_c:
    for fila_c in csv.DictReader(archivo_c):
        datos_cuenta = parsear_cuentas_csv(fila_c)
        cuenta_linea = generar_cuentas_asociadas(
            tipo_cuenta=datos_cuenta["tipo_cuenta"],
            cvu_cbu=datos_cuenta["cvu_cbu"],
            identificador_otro_tipo=datos_cuenta["identificador_otro_tipo"],
            cantidad_integrantes=int(datos_cuenta["cantidad_integrantes"]),
            por_orden_terceros=datos_cuenta["por_orden_terceros"],
            denominacion_tercero=datos_cuenta["denominacion_tercero"],
            signo_saldo_pesos=datos_cuenta["signo_saldo_pesos"],
            saldos_pesos=saldos(datos_cuenta["saldos_pesos"]),
            signo_saldo_me=datos_cuenta["signo_saldo_me"],
            saldos_me=saldos(datos_cuenta["saldos_me"]),
            signo_saldo_mv=datos_cuenta["signo_saldo_mv"],
            saldos_mv=saldos(datos_cuenta["saldos_mv"]),
            emisor_denominacion=datos_cuenta["emisor_denominacion"],
        )
        cuentas_por_cuit.setdefault(datos_cuenta["cuit_titular"], []).append(
            (datos_cuenta["cvu_cbu"], cuenta_linea)
        )

# Lee otros integrantes (si el archivo existe). No se emiten todavia.
otros_integrantes = []
if RUTA_OTROS_INTEGRANTES.exists():
    for fila in RUTA_OTROS_INTEGRANTES.read_text(encoding="utf-8").strip().splitlines():
        if not fila.strip():
            continue
        datos_otros_integrantes = parsear_otros_integrantes(fila)
        otros_integrantes.append(
            generar_otros_integrantes(
                origen=datos_otros_integrantes["origen"],
                tipo_documento=datos_otros_integrantes["tipo_documento"],
                codigo_pais_3=datos_otros_integrantes["codigo_pais_3"],
                cuit=datos_otros_integrantes["cuit"],
                numero_otro_documento=datos_otros_integrantes["numero_otro_documento"],
                nombre=datos_otros_integrantes["nombre"],
                caracter=datos_otros_integrantes["caracter"],
            )
        )

# Convierte una fila del CSV de movimientos en un dict (linea total o de contraparte)
def parsear_movimientos_csv(fila: dict) -> dict:
    return {
        "cvu": str(fila.get("cvu", "")).strip(),
        "tipo_operacion": str(fila.get("tipo_operacion", "")).strip(),
        "detalle_operacion": str(fila.get("detalle_operacion", "")).strip(),
        "moneda_original": str(fila.get("moneda", "")).strip(),
        "monto_total": str(fila.get("monto_pesos", "")).strip(),
        "cbu_contraparte": str(fila.get("contraparte_cbu_cvu", "")).strip(),
        "monto_contraparte": str(fila.get("monto_contraparte_pesos", "")).strip(),
    }


# Agrupa por (cvu, tipo, detalle, moneda): la linea con monto genera el 05 y las contrapartes los 06
grupos = {}
with RUTA_MOVIMIENTOS.open(encoding="utf-8", newline="") as archivo:
    lector_mov = csv.DictReader(archivo)
    for fila in lector_mov:
        datos_mov = parsear_movimientos_csv(fila)
        if not datos_mov["cvu"]:
            continue
        if datos_mov["detalle_operacion"] not in ("01", "02", "03", "04", "05", "06", "07", "08", "09"):
            continue
        clave = (
            datos_mov["cvu"],
            datos_mov["tipo_operacion"],
            datos_mov["detalle_operacion"],
            datos_mov["moneda_original"],
        )
        grupo = grupos.setdefault(clave, {"total": "", "contrapartes": []})
        if datos_mov["monto_total"]:
            grupo["total"] = datos_mov["monto_total"]
        elif datos_mov["cbu_contraparte"]:
            grupo["contrapartes"].append(
                {"cbu_contraparte": datos_mov["cbu_contraparte"], "monto_pesos": datos_mov["monto_contraparte"]}
            )

# Genera los movimientos 05/06 por cuenta (segun el umbral de $50M y el piso por transferencia)
movimientos = {}
for clave, grupo in grupos.items():
    cvu, tipo_operacion, detalle_operacion, moneda_original = clave
    if not grupo["total"]:
        continue
    movimientos.setdefault(cvu, []).extend(
        generar_movimientos_con_detalle(
            tipo_operacion=tipo_operacion,
            detalle_operacion=detalle_operacion,
            moneda_original=moneda_original,
            monto=grupo["total"],
            movimientos=grupo["contrapartes"] or None,
        )
    )

# Arma el orden final: titular 02 -> cuenta 03 -> movimientos 05/06 (solo si supero $50M)
lineas = [cabecera]
for titular, cuit_titular in zip(titulares, titulares_cuit):
    cuentas_con_movimientos = []
    for cvu_cuenta, cuenta_linea in cuentas_por_cuit.get(cuit_titular, []):
        bloques = []
        for linea in movimientos.get(cvu_cuenta, []):
            if linea[:2] == "05":
                bloques.append([linea])
            elif bloques:
                bloques[-1].append(linea)
        if not bloques:
            continue
        bloques.sort(key=lambda bloque: bloque[0][2:4])
        cuentas_con_movimientos.append((cuenta_linea, bloques))
    if not cuentas_con_movimientos:
        continue
    lineas.append(titular)
    for cuenta_linea, bloques in cuentas_con_movimientos:
        lineas.append(cuenta_linea)
        for bloque in bloques:
            lineas.extend(bloque)

# BLOQUE FINAL: cuenta el total de lineas, lo agrega a la cabecera y las une en un solo texto
resultados = construir_lineas(lineas)
contenido = "\n".join(resultados)

# Escribe el resultado en el archivo de salida
RUTA_SALIDA.write_text(contenido, encoding="utf-8")

print("Guardado en el archivo txt")