import requests

# API de cotizaciones de Argentina
url_argentina = "https://dolarapi.com/v1/cotizaciones"
# API del peso uruguayo
url_uyu = "https://dolarapi.com/v1/cotizaciones/uyu"
# API del dolar USA
url_dolar_usa = "https://dolarapi.com/v1/dolares"
# Api del Euro
url_euro = "https://dolarapi.com/v1/cotizaciones/eur"
# Api del Real brasilero
url_real_brasileno = "https://dolarapi.com/v1/cotizaciones/brl"
# Api del peso chileno
url_peso_chileno = "https://dolarapi.com/v1/cotizaciones/clp"



# Trae las cotizaciones del dia de todas las monedas desde internet
def obtener_cotizaciones():
    argentina = requests.get(url_argentina).json()
    uruguay = requests.get(url_uyu).json()
    dolar_usa = requests.get(url_dolar_usa).json()
    euro = requests.get(url_euro).json()
    real_brasileno = requests.get(url_real_brasileno).json()
    peso_chileno = requests.get(url_peso_chileno).json()

    return {
        "argentina": argentina,
        "uruguay": uruguay,
        "dolar_usa": dolar_usa,
        "euro": euro,
        "real_brasileno": real_brasileno,
        "peso_chileno": peso_chileno,
    }

