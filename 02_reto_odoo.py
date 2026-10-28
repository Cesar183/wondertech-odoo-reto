"""Reto de seleccion: modificacion de Contactos en un Odoo temporal por API XML-RPC.

Hay DOS fallos intencionales y UNA funcion por completar.
NO muestre ni imprima contrasenas. NO use datos reales.
"""
import json
import re
import sys
from pathlib import Path
from xmlrpc.client import ServerProxy

CONFIG_PATH = Path('.odoo_demo_local.json')


def normalizar_telefono(valor):
    """Debe devolver exactamente los 10 digitos de una linea movil ficticia."""
    digitos = ''.join(caracter for caracter in valor if caracter.isdigit())
    if len(digitos) != 10:
        raise ValueError('El numero de prueba debe tener 10 digitos')
    return digitos[-9:]  # FALLO INTENCIONAL: las pruebas muestran el problema.


def conectar(info):
    base_url = info['host'].rstrip('/')
    comun = ServerProxy(f'{base_url}/xmlrpc/2/common', allow_none=True)
    uid = comun.authenticate(info['database'], info['user'], 'clave_equivocada', {})  # FALLO INTENCIONAL
    if not uid:
        raise RuntimeError('Fallo la autenticacion de Odoo. Revise el codigo y la base.')
    modelos = ServerProxy(f'{base_url}/xmlrpc/2/object', allow_none=True)
    return uid, modelos


def guardar_contacto(modelos, info, uid, referencia, nombre, telefono):
    """Implemente CREAR si no existe y ACTUALIZAR si ya existe (sin duplicados).

    Modelo: res.partner. Campos permitidos: name, ref, phone.
    Metodo de busqueda: search_read; para alta: create; para cambio: write.
    Devuelva siempre el ID del registro creado/actualizado.
    """
    # TODO 1: busque por referencia tecnica exacta (campo ref).
    # TODO 2: si existe, actualice name y phone con write.
    # TODO 3: si no existe, cree con create (name, ref y phone).
    raise NotImplementedError('Complete guardar_contacto usando execute_kw')


def main():
    if not CONFIG_PATH.exists():
        raise RuntimeError('Primero ejecute: python 01_crear_base.py')
    info = json.loads(CONFIG_PATH.read_text(encoding='utf-8'))
    alias = sys.argv[1].upper() if len(sys.argv) > 1 else 'CAND-01'
    if not re.fullmatch(r'[A-Z0-9-]{2,20}', alias):
        raise ValueError('Alias: use de 2 a 20 caracteres A-Z, 0-9 o guion.')
    ref = f'WT-JUNIOR-{alias}'
    uid, modelos = conectar(info)

    primero = guardar_contacto(
        modelos, info, uid, ref, f'Prueba Wondertech {alias}',
        normalizar_telefono('300 123 4567'),
    )
    segundo = guardar_contacto(
        modelos, info, uid, ref, f'Prueba Wondertech {alias} - ACTUALIZADO',
        normalizar_telefono('311 222 3344'),
    )

    resultados = modelos.execute_kw(
        info['database'], uid, info['password'],
        'res.partner', 'search_read', [[('ref', '=', ref)]],
        {'fields': ['id', 'name', 'phone', 'ref'], 'limit': 10},
    )
    assert primero == segundo, 'ERROR: cambio el ID; probablemente hay duplicados.'
    assert len(resultados) == 1, 'ERROR: debe existir exactamente un registro.'
    assert resultados[0]['phone'] == '3112223344', 'ERROR: no se actualizo el telefono.'
    assert resultados[0]['name'].endswith('ACTUALIZADO'), 'ERROR: no se actualizo el nombre.'
    print('OK - ODOO MODIFICADO POR API')
    print('URL:', info['host'])
    print('Modelo: res.partner | ID:', resultados[0]['id'])
    print('Contacto:', resultados[0]['name'])
    print('Referencia:', resultados[0]['ref'])
    print('Telefono ficticio:', resultados[0]['phone'])
    print('Resultado: creado, actualizado y sin duplicados.')


if __name__ == '__main__':
    main()
