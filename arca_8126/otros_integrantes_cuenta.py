# tipo de registro de otros integrantes de la cuenta fijo de 2 dígitos
Tipo_registro = "04"

# Determina si es persona humana (1) o juridica (2) segun los primeros 2 digitos del CUIT
def tipo_de_persona(cuit) -> str:
    valor = str(cuit).strip()[:2]
    if valor in ("20", "23", "24", "27"):
        return "1"
    if valor in ("30", "33", "34"):
        return "2"
    raise ValueError(f"CUIT invalido para tipo de persona: {cuit}. Debe empezar con 20, 23, 24, 27, 30, 33 o 34.")


# Valida que el caracter sea de 2 digitos (01 a 06)
def validar_caracter(caracter) -> str:
    valor = str(caracter).strip().zfill(2)[:2]
    if valor in ("01", "02", "03", "04", "05", "06"):
        return valor
    raise ValueError(f"Caracter invalido: {caracter}. Debe estar entre 01 y 06.")

# Valida el origen: N (Argentina) o E (Extranjero)
def validar_origen(origen: str) -> str:
    valor = str(origen).strip().upper()
    if valor in ("N", "E"):
        return valor
    raise ValueError(f"Origen invalido: {origen}. Debe ser N o E.")

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

# Valida el CUIT de maximo 11 digitos
def validar_cuit(cuit) -> str:
    valor = str(cuit).strip()
    if not valor.isdigit():
        raise ValueError(f"CUIT invalido: {cuit}. Debe contener solo digitos.")
    if len(valor) > 11:
        raise ValueError(f"CUIT invalido: {cuit}. Maximo 11 digitos.")
    return valor.zfill(11)

# Si es extranjero (E) devuelve 11 espacios; si es argentino (N) valida el CUIT
def formatear_cuit(origen: str, tipo_documento: str, cuit) -> str:
    valor = validar_origen(origen)
    validar_tipo_documento(valor, tipo_documento)
    if valor == "E":
        return " " * 11
    return validar_cuit(cuit)

# Si es argentino (N) devuelve 20 espacios; si es extranjero (E) formatea el numero a 20 digitos
def formatear_numero_otro_documento(origen: str, numero) -> str:
    valor = validar_origen(origen)
    if valor == "N":
        return " " * 20
    numero = str(numero).strip()
    if not numero.isdigit():
        raise ValueError(f"Numero otro documento invalido: {numero}. Debe contener solo digitos.")
    if len(numero) > 20:
        raise ValueError(f"Numero otro documento invalido: {numero}. Maximo 20 digitos.")
    return numero.ljust(20)

# Convierte a mayusculas y rellena nombre y apellido (o empresa) a 60 caracteres
def formatear_nombre_apellido(texto: str) -> str:
    return str(texto).strip().upper().ljust(60)[:60]


# ========== RESULTADO DE OTROS INTEGRANTES DE CUENTA ==========
# Arma la linea de otros integrantes (registro 04): las otras personas de la cuenta
def generar_otros_integrantes(
    origen: str,
    tipo_documento: str,
    codigo_pais_3: str,
    cuit: str,
    numero_otro_documento: str,
    nombre: str,
    caracter: str = "",
) -> str:
    return (
        Tipo_registro
        + tipo_de_persona(cuit)
        + validar_caracter(caracter)
        + validar_origen(origen)
        + validar_tipo_documento(origen, tipo_documento)
        + validar_codigo_pais_3(origen, codigo_pais_3)
        + formatear_cuit(origen, tipo_documento, cuit)
        + formatear_numero_otro_documento(origen, numero_otro_documento)
        + formatear_nombre_apellido(nombre)
    )