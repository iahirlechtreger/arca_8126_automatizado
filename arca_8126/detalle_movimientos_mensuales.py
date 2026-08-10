from decimal import Decimal, ROUND_HALF_UP

# Umbral art. 3° 2° párrafo RG 4614 (personas humanas).
# Si ARCA lo modifica, se cambia SOLO esta constante.
UMBRAL_PERSONAS_HUMANAS = Decimal("50000000")
PISO_REG_06 = UMBRAL_PERSONAS_HUMANAS * Decimal("0.05")   # $2.500.000

# Conceptos que admiten registro 06 colgando: transf. a terceros (02) / transf. propia (03)
CONCEPTOS_CON_DETALLE = {"02", "03"}
# Solo monedas fiduciarias (01 a 13), no cripto
MONEDAS_FIDUCIARIAS = {f"{n:02d}" for n in range(1, 14)}


# Indica si el registro 05 admite registros 06 colgando (transferencias en moneda fiduciaria)
def corresponde_detalle(concepto, moneda):
    return concepto in CONCEPTOS_CON_DETALLE and moneda in MONEDAS_FIDUCIARIAS


# Devuelve las transferencias individuales que superan el piso, de mayor a menor
def calcular_registros_06(movimientos, concepto, moneda):
    if not corresponde_detalle(concepto, moneda):
        return []

    detalle = []
    for m in movimientos:
        monto = Decimal(str(m["monto_pesos"]))
        if monto > PISO_REG_06:        # estrictamente mayor
            detalle.append((m["cbu_contraparte"], monto.quantize(Decimal("1"), rounding=ROUND_HALF_UP)))
    return sorted(detalle, key=lambda x: x[1], reverse=True)

# Tipo de registro de detalle de movimientos mensuales (2 digitos)
tipoRegistroDetalleMovimientosMensuales = "06"

# Valida que el CBU/CVU tenga exactamente 22 digitos
def validar_cbu_cvu(cbu) -> str:
    valor = str(cbu).strip()
    if not valor.isdigit():
        raise ValueError(f"CBU/CVU invalido: {cbu}. Debe contener solo digitos.")
    if len(valor) != 22:
        raise ValueError(f"CBU/CVU invalido: {cbu}. Debe tener 22 digitos.")
    return valor


# Formatea la linea del registro 06 con el CBU y el monto del detalle
def formatear_registro_06(cbu, monto):
    cbu_valido = validar_cbu_cvu(cbu)
    assert monto >= 0, "los montos van siempre en positivo"
    return f"{tipoRegistroDetalleMovimientosMensuales}{cbu_valido}{int(monto):012d}"