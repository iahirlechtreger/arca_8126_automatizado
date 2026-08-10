from arca_8126.fetch import obtener_cotizaciones
from arca_8126.detalle_movimientos_mensuales import (
    corresponde_detalle,
    calcular_registros_06,
    formatear_registro_06,
)


c = obtener_cotizaciones()

# Tipo de registro de movimientos mensuales (2 digitos)
Tipo_registro = "05"

# Tabla de monedas: codigo -> nombre.
MONEDAS = {
    "02": c["dolar_usa"],
    "03": c["euro"],
    "06": c["real_brasileno"],
    "10": c["peso_chileno"],
    "12": c["uruguay"],
    }    

# Tabla de tipo de cambio: codigo de moneda -> valor en pesos argentinos.
# Completar el dia de registro con la cotizacion de cada moneda.
TIPO_CAMBIO = {
     "02": c["dolar_usa"][0]["compra"],
     "03": c["euro"]["compra"],
     "06": c["real_brasileno"]["compra"],
     "10": c["peso_chileno"]["compra"],
     "12": c["uruguay"]["compra"],   
     } 

# Valida tipo de operacion: 01 (ingreso) o 02 (egreso)
def validar_tipo_operacion(tipo) -> str:
    valor = str(tipo).strip().zfill(2)[:2]
    if valor in ("01", "02"):
        return valor
    raise ValueError(f"Tipo de operacion invalido: {tipo}. Debe ser 01 (ingreso) o 02 (egreso).")

# Valida detalle de operacion de 2 digitos: 01 a 09
def validar_detalle_operacion(detalle) -> str:
    valor = str(detalle).strip().zfill(2)[:2]
    if valor in ("01", "02", "03", "04", "05", "06", "07", "08", "09"):
        return valor
    raise ValueError(f"Detalle de operacion invalido: {detalle}. Debe estar entre 01 y 09.")

# Valida moneda original de 2 digitos: 01 a 42
def validar_moneda_original(codigo) -> str:
    valor = str(codigo).strip()
    if not valor.isdigit():
        raise ValueError(f"Moneda original invalida: {codigo}. Debe contener solo digitos.")
    if len(valor) > 2:
        raise ValueError(f"Moneda original invalida: {codigo}. No se aceptan numeros de 3 digitos.")
    numero = int(valor)
    if numero < 1 or numero > 42:
        raise ValueError(f"Moneda original invalida: {codigo}. Debe estar entre 01 y 42.")
    return valor.zfill(2)


# Corta los decimales con punto o coma y deja el monto como entero
def monto_entero(monto) -> int:
    valor = str(monto).strip()
    if "." in valor or "," in valor:
        valor = valor.replace(",", ".").split(".")[0]
    if not valor.isdigit():
        raise ValueError(f"Monto invalido: {monto}. Debe contener solo digitos.")
    return int(valor)


# Formatea un numero a 13 digitos con ceros a la izquierda
def formatear_monto_13_digitos(numero) -> str:
    valor = str(numero)
    if not valor.isdigit():
        raise ValueError(f"Monto invalido: {numero}. Debe contener solo digitos.")
    if len(valor) > 13:
        raise ValueError(f"Monto invalido: {numero}. Maximo 13 digitos.")
    return valor.zfill(13)

# Devuelve el monto a 13 digitos; si la moneda es 01 (pesos) devuelve 13 ceros
def formatear_monto_mensual_moneda_original(moneda_original: str, monto) -> str:
    if validar_moneda_original(moneda_original) == "01":
        return "0" * 13
    return formatear_monto_13_digitos(monto_entero(monto))


# Devuelve el tipo de cambio de una moneda en pesos argentinos
def tasa_cambio(moneda_original: str) -> float:
    moneda = validar_moneda_original(moneda_original)
    if moneda not in TIPO_CAMBIO:
        raise ValueError(f"No hay tipo de cambio para la moneda {moneda}. Completar TIPO_CAMBIO.")
    return TIPO_CAMBIO[moneda]

# Devuelve el monto en pesos a 13 digitos; si la moneda no es pesos, convierte con el tipo de cambio
def formatear_monto_mensual_pesos(moneda_original: str, monto) -> str:
    if validar_moneda_original(moneda_original) == "01":
        return formatear_monto_13_digitos(monto_entero(monto))
    importe = monto_entero(monto) * tasa_cambio(moneda_original)
    return formatear_monto_13_digitos(round(importe))


# Genera la linea del movimiento mensual: tipo, operacion, detalle, moneda y montos
def generar_movimientos_mensuales(
    tipo_operacion: str,
    detalle_operacion: str,
    moneda_original: str,
    monto: str,
) -> str:
    return (
        Tipo_registro
        + validar_tipo_operacion(tipo_operacion)
        + validar_detalle_operacion(detalle_operacion)
        + validar_moneda_original(moneda_original)
        + formatear_monto_mensual_moneda_original(moneda_original, monto)
        + formatear_monto_mensual_pesos(moneda_original, monto)
    )


# Genera el registro 05 y, si corresponde, los registros 06.
# El 05 (y sus 06) solo se muestran si el monto total en pesos supera $50M.
UMBRAL_MOVIMIENTOS_MENSUALES = 50000000

def generar_movimientos_con_detalle(
    tipo_operacion: str,
    detalle_operacion: str,
    moneda_original: str,
    monto: str,
    movimientos: list = None,
) -> list:
    """Devuelve [linea 05, ...lineas 06] si el monto total supera $50M, si no []. Si corresponde el detalle por contraparte."""
    monto_pesos = int(formatear_monto_mensual_pesos(moneda_original, monto))
    if monto_pesos < UMBRAL_MOVIMIENTOS_MENSUALES:
        return []
    linea_05 = generar_movimientos_mensuales(tipo_operacion, detalle_operacion, moneda_original, monto)
    if not corresponde_detalle(detalle_operacion, moneda_original) or not movimientos:
        return [linea_05]

    registros_06 = calcular_registros_06(movimientos, detalle_operacion, moneda_original)
    if not registros_06:
        return [linea_05]
    return [linea_05] + [formatear_registro_06(cbu, monto_pesos) for cbu, monto_pesos in registros_06]