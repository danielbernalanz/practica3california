# Prueba de error controlado (apartado e) - P3

La aplicación no se rompe ante errores de la API: captura la respuesta, muestra el código HTTP
y el texto del error en un único mensaje rojo y sigue disponible para otra consulta.

1. `captura_url_incorrecta_P3.png`: la URL de la API se cambia a
   `https://api-que-no-existe-p3.onrender.com`. Render responde 404 a un subdominio que no existe y la
   app muestra «Error 404 devuelto por la API: Not Found».
2. `captura_error_422_P3.png`: con las casillas «omitir HouseAge» y «saltar la validación local»
   marcadas, la petición sale sin `HouseAge` y la API la rechaza. La app muestra
   «Error 422 devuelto por la API: ...» con el detalle de FastAPI (`type: missing`, `loc: body, HouseAge`).

Si no hay ninguna respuesta (servicio caído o sin red), la app muestra «No se pudo contactar con la API...».
