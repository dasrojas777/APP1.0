import json
import re

# Palabras clave para tipos de protocolo
PROTOCOLOS = {
    'GROUT': ['GROUT', 'CONTROL DE VACIADO'],
    'HORMIGON': ['HORMIGÓN', 'HORMIGON'],
    'RELLENO': ['RELLENO'],
    # Agrega más tipos según tus necesidades
}

def detectar_protocolo(texto):
    """Detecta el tipo de protocolo según palabras clave en el texto."""
    for tipo, claves in PROTOCOLOS.items():
        for clave in claves:
            if clave.upper() in texto.upper():
                return tipo
    return 'DESCONOCIDO'

def extraer_secciones(texto):
    """
    Extrae secciones principales del formulario según encabezados típicos.
    Devuelve un dict con las secciones encontradas y su contenido.
    """
    # Definir patrones de encabezados (puedes ajustar)
    patrones = [
        r'ENCABEZADO',
        r'LIBERACIÓN.*?GROUT',
        r'CONTROLES ANTES.*?GROUT',
        r'CONTROLES DURANTE.*?GROUT',
        r'OBSERVACIONES',
        r'RESPONSABLE.*?ENTREGADO',
        r'FIRMAS?',
    ]
    # Unir patrones en una sola regex
    regex = '|'.join(patrones)
    # Separar por encabezados
    secciones = re.split(regex, texto, flags=re.IGNORECASE)
    # Mapear a nombres
    nombres = ['encabezado', 'liberacion', 'controles_antes', 'controles_durante_post', 'observaciones', 'firmas']
    resultado = {}
    for i, nombre in enumerate(nombres):
        if i < len(secciones):
            resultado[nombre] = secciones[i].strip()
    return resultado

def analizar_formulario(texto):
    """
    Analiza el texto de un formulario, detecta protocolo y secciones, y guarda como JSON.
    """
    tipo = detectar_protocolo(texto)
    secciones = extraer_secciones(texto)
    resultado = {
        'tipo_protocolo': tipo,
        'secciones': secciones
    }
    # Guardar como JSON
    with open('formulario_detectado.json', 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    print('Protocolo detectado:', tipo)
    print('Secciones encontradas:', list(secciones.keys()))
    print('JSON guardado en formulario_detectado.json')

if __name__ == '__main__':
    # Ejemplo de uso: leer texto desde un archivo o string
    texto = """
    PROTOCOLO GROUT (AUTORIZACIÓN Y CONTROL DE VACIADO)
    ...
    LIBERACIÓN ELEMENTO A GROUTEAR
    ...
    CONTROLES ANTES DE VACIADO DE GROUT
    ...
    CONTROLES DURANTE Y POST VACIADO DE GROUT
    ...
    OBSERVACIONES
    ...
    RESPONSABLE DE TRABAJO ENTREGADO
    ...
    """
    analizar_formulario(texto)
