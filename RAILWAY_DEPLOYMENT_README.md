# Railway Deployment Instructions

## 1. Imagen Docker
- Asegúrate de que la imagen esté en Docker Hub:
  - agora90/albertomayday:stakas

## 2. Variables de entorno
Copia y pega estas variables en Railway (ajusta valores reales):

```
# --- Railway Environment Variables ---
DUMMY_MODE=false
POSTGRES_HOST=... # tu host de base de datos
POSTGRES_PORT=5432
POSTGRES_USER=... # tu usuario
POSTGRES_PASSWORD=... # tu password
POSTGRES_DB=... # tu base de datos
SECRET_KEY=... # clave secreta para FastAPI
# Añade aquí cualquier otra variable necesaria
```

## 3. Despliegue en Railway
1. Ve a tu proyecto en Railway.
2. Elige "Deploy from Docker Hub".
3. Usa la imagen: `agora90/albertomayday:stakas`
4. Añade las variables de entorno anteriores.
5. Lanza el deploy y espera a que el servicio esté en "Running".

## 4. Pruebas
- Accede a la URL pública de Railway.
- Comprueba que el dashboard y la API responden.

---

¿Problemas? Consulta los logs en Railway y revisa la configuración de variables.
