"""Contingencia: Odoo 20 (demo.odoo.com) ya no expone /xmlrpc/2 (responde 404).

Expone el mismo execute_kw sobre la sesion web (/web/dataset/call_kw), de modo que
guardar_contacto funciona igual con cualquiera de los dos transportes.
"""
import http.cookiejar
import json
import urllib.request


class ModelosSesion:
    def __init__(self, info):
        self.host = info['host'].rstrip('/')
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        resultado = self._post('/web/session/authenticate',
                               {'db': info['database'], 'login': info['user'], 'password': info['password']})
        self.uid = resultado.get('uid')

    def _post(self, ruta, params):
        peticion = urllib.request.Request(
            self.host + ruta, headers={'Content-Type': 'application/json'},
            data=json.dumps({'jsonrpc': '2.0', 'params': params}).encode(),
        )
        respuesta = json.loads(self.opener.open(peticion, timeout=30).read())
        if 'error' in respuesta:
            raise RuntimeError(respuesta['error'].get('data', {}).get('message', 'Error de Odoo'))
        return respuesta['result']

    def execute_kw(self, db, uid, password, modelo, metodo, args, opciones=None):
        return self._post('/web/dataset/call_kw', {'model': modelo, 'method': metodo,
                                                   'args': args, 'kwargs': opciones or {}})
