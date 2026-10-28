# Registro rápido (NO incluye contrasenas)

Alias de evaluacion: CAND-01
URL de la base temporal: https://demo4.odoo.com
Modelo actualizado: res.partner
Referencia del contacto: WT-JUNIOR-CAND-01
ID del contacto: 180 (mismo ID antes y despues de actualizar)
Pruebas locales (n/3): 3/3
Repositorio GitHub (privado): https://github.com/Cesar183/wondertech-odoo-reto
Hash del commit: 7249b28 (solucion)
Herramienta IA: Claude Code
Que parte sugirio la IA: diagnostico de los dos fallos, estructura de guardar_contacto con execute_kw
  (search_read -> write/create) y el transporte de contingencia odoo_sesion.py.
Que se valido manualmente: 3 tests locales; dos ejecuciones reales con el mismo ID (180);
  nombre "... - ACTUALIZADO" y telefono 3112223344 en Odoo; .odoo_demo_local.json ignorado por Git.

## Errores corregidos
1. normalizar_telefono: `digitos[-9:]` recortaba el primer digito ('3001234567' -> '001234567').
   Ya se validan 10 digitos, por lo que se devuelve el numero completo.
2. conectar: autenticaba con la contrasena fija 'clave_equivocada'; ahora usa info['password']
   leida del archivo local (no versionado).

## Como se evitan duplicados
guardar_contacto busca primero por la referencia tecnica exacta (ref = WT-JUNIOR-ALIAS) con search_read.
Si existe, hace write sobre ese ID; si no, hace create. La segunda llamada siempre encuentra el registro,
por eso el ID no cambia y el script verifica que exista exactamente un registro.

Incidentes externos (si hubo): demo.odoo.com entrega bases Odoo 20.0, donde /xmlrpc/2/common responde
  404 (XML-RPC no disponible). conectar intenta XML-RPC primero y, solo ante 404, avisa en pantalla y usa
  la sesion web (/web/dataset/call_kw) con la misma interfaz execute_kw. Reportado al evaluador.
