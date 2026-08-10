from arca_8126.titular_cuenta import formatear_saldo, validar_signo_saldo

# Tipo de registro valor fijo de 2 dígitos
tipo_registro_cuentas_asociadas = "03"

# Valida tipo de cuenta asociada de 2 digitos: 01 o 02
def validar_tipo_cuenta_asociada(tipo) -> str:
    valor = str(tipo).strip().zfill(2)[:2]
    if valor in ("01", "02"):
        return valor
    raise ValueError(f"Tipo de cuenta asociada invalido: {tipo}. Debe ser 01 o 02.")


# Si tipo_cuenta es 01 rellena CVU/CBU a 22 digitos; si es 02 va vacio
def formatear_cvu_cbu(tipo_cuenta: str, cvu_cbu: str) -> str:
    tipo = validar_tipo_cuenta_asociada(tipo_cuenta)
    if tipo != "01":
        return " " * 22
    valor = str(cvu_cbu).strip()
    if not valor.isdigit():
        raise ValueError(f"CVU/CBU invalido: {cvu_cbu}. Debe contener solo digitos.")
    if len(valor) > 22:
        raise ValueError(f"CVU/CBU invalido: {cvu_cbu}. Maximo 22 digitos.")
    return valor.zfill(22)


# Si tipo_cuenta es 02 rellena el identificador a 50 lugares; si es 01 va vacio
def formatear_identificador_otro_tipo(tipo_cuenta: str, identificador: str) -> str:
    tipo = validar_tipo_cuenta_asociada(tipo_cuenta)
    if tipo != "02":
        return " " * 50
    return str(identificador).strip().ljust(50)[:50]


# Valida la cantidad de integrantes (1 a 99) y la formatea a 2 digitos
def formatear_cantidad_integrantes(cantidad) -> str:
    valor = int(str(cantidad).strip())
    if valor < 1 or valor > 99:
        raise ValueError(f"Cantidad de integrantes invalida: {cantidad}. Debe estar entre 1 y 99.")
    return str(valor).zfill(2)


# Denominacion de la entidad emisora: va vacia porque el nombre ya esta en la cabecera
def formatear_denominacion_entidad(texto: str = "") -> str:
    return str(texto).strip().upper().ljust(200)[:200]

# Tipo de documento de la entidad emisora: 2 lugares vacios
tipo_documento_entidad = "  "

# Numero de documento de la entidad emisora: 20 lugares vacios
numero_documento_entidad = " " * 20

# Valida si la cuenta actua por cuenta y orden de terceros: 0 no, 1 si
def validar_cuenta_por_orden_terceros(valor) -> str:
    v = str(valor).strip()
    if v in ("0", "1"):
        return v
    raise ValueError(f"Valor invalido: {valor}. Debe ser 0 (no) o 1 (si).")


# Si actua por orden de terceros (1) rellena la denominacion a 200 lugares; si no, va vacio
def formatear_denominacion_tercero(por_orden: str, denominacion: str) -> str:
    if validar_cuenta_por_orden_terceros(por_orden) != "1":
        return " " * 200
    return str(denominacion).strip().upper().ljust(200)[:200]

# Signo del saldo en pesos: 0 positivo, 1 negativo
def validar_signo_saldo_pesos(signo, saldo_total: int = 0) -> str:
    return validar_signo_saldo(signo, saldo_total)


# Saldo total en pesos a 12 digitos
def formatear_saldo_pesos(saldos: list) -> str:
    return formatear_saldo(saldos, 12)


# Signo del saldo en moneda extranjera: 0 positivo, 1 negativo
def validar_signo_saldo_moneda_extranjera(signo, saldo_total: int = 0) -> str:
    return validar_signo_saldo(signo, saldo_total)


# Saldo total en moneda extranjera a 12 digitos
def formatear_saldo_moneda_extranjera(saldos: list) -> str:
    return formatear_saldo(saldos, 12)


# Signo del saldo en moneda virtual: 0 positivo, 1 negativo
def validar_signo_saldo_moneda_virtual(signo, saldo_total: int = 0) -> str:
    return validar_signo_saldo(signo, saldo_total)


# Saldo total en moneda virtual a 12 digitos
def formatear_saldo_moneda_virtual(saldos: list) -> str:
    return formatear_saldo(saldos, 12)


# ========== RESULTADO DE CUENTAS ASOCIADAS ==========
# Arma la linea de la cuenta (registro 03): cada cuenta del titular y sus saldos
def generar_cuentas_asociadas(
    tipo_cuenta: str,
    cvu_cbu: str,
    identificador_otro_tipo: str,
    cantidad_integrantes: int,
    por_orden_terceros: str,
    denominacion_tercero: str,
    signo_saldo_pesos: str,
    saldos_pesos: list,
    signo_saldo_me: str,
    saldos_me: list,
    signo_saldo_mv: str,
    saldos_mv: list,
    emisor_denominacion: str = "",
) -> str:
    saldo_total_pesos = sum(int(str(s).strip()) for s in saldos_pesos)
    saldo_total_me = sum(int(str(s).strip()) for s in saldos_me)
    saldo_total_mv = sum(int(str(s).strip()) for s in saldos_mv)

    return (
        tipo_registro_cuentas_asociadas
        + validar_tipo_cuenta_asociada(tipo_cuenta)
        + formatear_cvu_cbu(tipo_cuenta, cvu_cbu)
        + formatear_identificador_otro_tipo(tipo_cuenta, identificador_otro_tipo)
        + formatear_cantidad_integrantes(cantidad_integrantes)
        + formatear_denominacion_entidad(emisor_denominacion)
        + tipo_documento_entidad
        + numero_documento_entidad
        + validar_cuenta_por_orden_terceros(por_orden_terceros)
        + formatear_denominacion_tercero(por_orden_terceros, denominacion_tercero)
        + validar_signo_saldo_pesos(signo_saldo_pesos, saldo_total_pesos)
        + formatear_saldo_pesos(saldos_pesos)
        + validar_signo_saldo_moneda_extranjera(signo_saldo_me, saldo_total_me)
        + formatear_saldo_moneda_extranjera(saldos_me)
        + validar_signo_saldo_moneda_virtual(signo_saldo_mv, saldo_total_mv)
        + formatear_saldo_moneda_virtual(saldos_mv)
    )

