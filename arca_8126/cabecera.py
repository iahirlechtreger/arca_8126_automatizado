from datetime import datetime

# Numero fijo de identificador de registro (2 dígitos)
IDENTIFICADOR_CABECERA = "01"

# CUIT fijo
CUIT = "30718725840"

# Obtiene el mes anterior en formato YYYYMM
def obtener_periodo_anterior() -> str:
    hoy = datetime.now()
    if hoy.month == 1:
        mes_anterior = (hoy.year - 1, 12)
    else:
        mes_anterior = (hoy.year, hoy.month - 1)
    return f"{mes_anterior[0]}{mes_anterior[1]:02d}"


# secuencia numero fijo de 2 dígitos
SECUENCIA = "00"

# denominacion del prestador de servicios, rellena a 200 caracteres
DENOMINACION = "HAPPYPAY S.A."

# Convierte a mayusculas y rellena la denominacion a 200 caracteres
def formatear_denominacion(texto: str) -> str:
    return str(texto).strip().upper().ljust(200)[:200]

# Obtiene la hora actual en formato HHMMSS
def obtener_hora_actual() -> str:
    return datetime.now().strftime("%H%M%S")

# codigo de impuesto fijo de 4 dígitos
CODIGO_DE_IMPUESTO = "0103"

# codigo de concepto fijo de 3 dígitos
CODIGO_DE_CONCEPTO = "812"

# numero verificador max 6 digitos
NUMERO_VERIFICADOR = "111111"

# Numero de formulario fijo de 4 dígitos
NUMERO_DE_FORMULARIO = "8126"

# Numero de version del aplicativo fijo de 5 dígitos
VERSION = "00300"

# Rellena un numero con ceros a la izquierda hasta el largo pedido
def formatear_numero(numero, longitud: int) -> str:
    return str(numero).zfill(longitud)[:longitud]


# Formatea el numero verificador a 6 digitos
def formatear_numero_verificador(numero) -> str:
    return formatear_numero(numero, 6)

# ========== RESULTADO DE CABECERA ==========
# Arma la primera linea del formulario (identificacion del archivo)
def generar_cabecera(cuit: str, periodo: str, hora: str) -> str:
    return (
        IDENTIFICADOR_CABECERA
        + CUIT
        + periodo
        + SECUENCIA
        + formatear_denominacion(DENOMINACION)
        + hora
        + CODIGO_DE_IMPUESTO
        + CODIGO_DE_CONCEPTO
        + formatear_numero_verificador(NUMERO_VERIFICADOR)
        + NUMERO_DE_FORMULARIO
        + VERSION
        
    )



# Formatea la cantidad de registros a 10 digitos
def formatear_cantidad_registros(numero: int) -> str:
    return formatear_numero(numero, 10)




