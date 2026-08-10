 # Tipo de registro fijo para titular de cuenta (2 dígitos)
tipo_registro_titular = "02" 

# Determina si es persona humana (1) o juridica (2) segun los primeros 2 digitos del CUIT
def determinar_tipo_persona(cuit) -> str:
    prefijo = str(cuit).strip()[:2]
    if prefijo in ("20", "23", "24", "27"):
        return "1"
    if prefijo in ("30", "33", "34"):
        return "2"
    raise ValueError(
        f"CUIT invalido: {cuit}. Los primeros 2 digitos deben ser 20,23,24,27 (humana) o 30,33,34 (juridica)."
    )


# Valida que el tipo de titular sea 1 (humana) o 2 (juridica)
def validar_tipo_titular(tipo) -> str:
    valor = str(tipo).strip()
    if valor in ("1", "2"):
        return valor
    raise ValueError(f"Tipo de titular invalido: {tipo}. Debe ser 1 o 2.")


# Devuelve el tipo de titular a un solo digito
def formatear_titular_cuenta(tipo) -> str:
    return validar_tipo_titular(tipo).zfill(1)[:1]


# Valida que el origen sea N (Argentina) o E (Extranjero)
def validar_origen(origen: str) -> str:
    valor = str(origen).strip().upper()
    if valor in ("N", "E"):
        return valor
    raise ValueError(f"Origen invalido: {origen}. Debe ser N o E.")


# Valida tipo de documento de 2 digitos segun el origen
def validar_tipo_documento(origen: str, codigo) -> str:
    valor = validar_origen(origen)
    codigo = str(codigo).strip().zfill(2)[:2]
    permitidos_argentina = {"80", "86", "87"}
    permitidos_extranjero = {"80", "86", "87", "88", "94", "99"}
    permitidos = permitidos_argentina if valor == "N" else permitidos_extranjero
    if codigo not in permitidos:
        raise ValueError(f"Tipo de documento invalido {codigo} para origen {valor}. Permitidos: {sorted(permitidos)}")
    return codigo


# Devuelve 200 si es Argentina, o valida el codigo de pais de 3 digitos
def validar_codigo_pais_3(origen: str, codigo) -> str:
    valor = validar_origen(origen)
    if valor == "N":
        return "200"
    codigo = str(codigo).strip()
    if not codigo.isdigit():
        raise ValueError(f"Codigo de pais invalido: {codigo}. Debe contener solo digitos.")
    if len(codigo) != 3:
        raise ValueError(f"Codigo de pais invalido: {codigo}. Debe tener 3 digitos.")
    return codigo

# Valida el CUIT de maximo 11 digitos
def validar_cuit(cuit) -> str:
    valor = str(cuit).strip()
    if not valor.isdigit():
        raise ValueError(f"CUIT invalido: {cuit}. Debe contener solo digitos.")
    if len(valor) > 11:
        raise ValueError(f"CUIT invalido: {cuit}. Maximo 11 digitos.")
    return valor.zfill(11)

# Si es extranjero (88,94,99) formatea el numero a 20 digitos; si es Argentina va vacio
def formatear_numero_otro_documento(pais_codigo: str, numero) -> str:
    pais = str(pais_codigo).strip()
    if pais == "200":
        return " " * 20
    if pais in ("88", "94", "99"):
        valor = str(numero).strip()
        if not valor.isdigit():
            raise ValueError(f"Numero otro documento invalido: {numero}. Debe contener solo digitos.")
        if len(valor) > 20:
            raise ValueError(f"Numero otro documento invalido: {numero}. Maximo 20 digitos.")
        return valor.zfill(20)
    raise ValueError(f"Codigo de pais invalido para otro documento: {pais_codigo}. Debe ser 88, 94, 99 o 200.")

# Convierte a mayusculas y rellena nombre y apellido (o empresa) a 60 caracteres
def formatear_nombre_apellido(texto: str) -> str:
    return str(texto).strip().upper().ljust(60)[:60]


# Rellena el id de cuenta/cliente a 50 lugares; si no hay id, usa el cuit
def formatear_id_cuenta_cliente(id_cliente, cuit: str) -> str:
    valor = str(id_cliente).strip() if id_cliente else validar_cuit(cuit)
    return valor.ljust(50)[:50]


# Valida que la fecha de alta sea AAAAMMDD (8 digitos)
def validar_fecha_alta_cuenta(fecha) -> str:
    valor = str(fecha).strip()
    if not valor.isdigit():
        raise ValueError(f"Fecha de alta invalida: {fecha}. Debe contener solo digitos.")
    if len(valor) != 8:
        raise ValueError(f"Fecha de alta invalida: {fecha}. Debe tener 8 digitos (AAAAMMDD).")
    return valor


# Valida el tipo de operacion: 01 cierre, 02 con movimientos, 03 sin movimientos
def validar_tipo_operacion(tipo) -> str:
    valor = str(tipo).strip().zfill(2)[:2]
    if valor in ("01", "02", "03"):
        return valor
    raise ValueError(f"Tipo de operacion invalido: {tipo}. Debe ser 01, 02 o 03.")


# Devuelve 0 si el saldo es positivo (o 0) o 1 si es negativo
def validar_signo_saldo(signo, saldo_total: int = 0) -> str:
    if saldo_total == 0:
        return "0"
    valor = str(signo).strip()
    if valor in ("0", "1"):
        return valor
    raise ValueError(f"Signo del saldo invalido: {signo}. Debe ser 0 (positivo) o 1 (negativo).")


# Suma los saldos de las cuentas y los formatea a 12 digitos con ceros a la izquierda
def formatear_saldo(saldos: list, longitud: int = 12) -> str:
    total = 0
    for s in saldos:
        try:
            total += int(str(s).strip())
        except ValueError:
            raise ValueError(f"Saldo invalido: {s}. Debe ser un numero entero.")
    valor = str(total)
    if len(valor) > longitud:
        valor = valor[:longitud]
    return valor.zfill(longitud)


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


# Valida la cantidad de cuentas (1 a 9999) y la formatea a 4 digitos
def formatear_cantidad_cuentas(cantidad) -> str:
    valor = int(str(cantidad).strip())
    if valor < 1 or valor > 9999:
        raise ValueError(f"Cantidad de cuentas invalida: {cantidad}. Debe estar entre 1 y 9999.")
    return str(valor).zfill(4)


# ========== RESULTADO DE TITULAR DE CUENTA ==========
# Arma la linea del titular (registro 02): quien es el dueno y cuanta plata tiene
def generar_titular_cuenta(
    origen: str,
    codigo_pais_3: str,
    tipo_documento: str,
    cuit: str,
    numero_otro_documento: str,
    nombre: str,
    id_cuenta_cliente: str = "",
    fecha_alta: str = "",
    tipo_operacion: str = "",
    signo_saldo_pesos: str = "",
    saldos_pesos: list = None,
    signo_saldo_me: str = "",
    saldos_me: list = None,
    signo_saldo_mv: str = "",
    saldos_mv: list = None,
    cantidad_cuentas: int = 1,
    tipo: str = "",
) -> str:
    if saldos_pesos is None:
        saldos_pesos = []
    if saldos_me is None:
        saldos_me = []
    if saldos_mv is None:
        saldos_mv = []

    if not str(tipo).strip():
        tipo = determinar_tipo_persona(cuit)

    saldo_total_pesos = sum(int(str(s).strip()) for s in saldos_pesos)
    saldo_total_me = sum(int(str(s).strip()) for s in saldos_me)
    saldo_total_mv = sum(int(str(s).strip()) for s in saldos_mv)

    return (
        tipo_registro_titular
        + formatear_titular_cuenta(tipo)
        + validar_origen(origen)
        + validar_codigo_pais_3(origen, codigo_pais_3)
        + validar_tipo_documento(origen, tipo_documento)
        + validar_cuit(cuit)
        + formatear_numero_otro_documento(validar_codigo_pais_3(origen, codigo_pais_3), numero_otro_documento)
        + formatear_nombre_apellido(nombre)
        + formatear_id_cuenta_cliente(id_cuenta_cliente, cuit)
        + validar_fecha_alta_cuenta(fecha_alta)
        + validar_tipo_operacion(tipo_operacion)
        + validar_signo_saldo_pesos(signo_saldo_pesos, saldo_total_pesos)
        + formatear_saldo_pesos(saldos_pesos)
        + validar_signo_saldo_moneda_extranjera(signo_saldo_me, saldo_total_me)
        + formatear_saldo_moneda_extranjera(saldos_me)
        + validar_signo_saldo_moneda_virtual(signo_saldo_mv, saldo_total_mv)
        + formatear_saldo_moneda_virtual(saldos_mv)
        + formatear_cantidad_cuentas(cantidad_cuentas)
    )

