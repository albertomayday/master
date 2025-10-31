# Railway Deployment Validation Checklist

Este checklist te permite demostrar y validar que el despliegue en Railway funciona correctamente, tanto para el examen/demo (dummy mode) como para producción real.

## 1. Validación de CI/CD y Docker Hub
- [ ] Push a `main` en GitHub dispara el workflow de CI/CD.
- [ ] El workflow construye la imagen Docker y la sube a Docker Hub (ver logs en GitHub Actions).
- [ ] La imagen contiene `DUMMY_MODE=true` para el entorno seguro de examen/demo.

## 2. Despliegue en Railway
- [ ] Railway detecta la nueva imagen/tag y lanza el despliegue automáticamente, o lo lanzas manualmente con los scripts:
  - Linux/Mac: `bash scripts/railway/deploy.sh`
  - Windows: `pwsh ./deploy-integrated-system.ps1`
- [ ] El proyecto Railway está correctamente enlazado a tu repo y Docker Hub.

## 3. Variables de entorno y seguridad
- [ ] Todas las API keys y secretos se configuran manualmente en Railway (nunca en el repo ni en el build).
- [ ] `DUMMY_MODE=true` en Railway para el examen/demo. Para producción, cambiar a `DUMMY_MODE=false` y añadir modelos reales.

## 4. Validación de servicios
- [ ] El dashboard Streamlit es accesible desde la URL pública de Railway.
- [ ] La API FastAPI responde en `/docs` o `/analyze_screenshot`.
- [ ] Un endpoint ML responde (aunque sea dummy).
- [ ] Los logs en Railway muestran arranque correcto de todos los servicios.

## 5. Producción real (cuando toque)
- [ ] Cambiar `DUMMY_MODE=false` en Railway y en Dockerfile.
- [ ] Añadir modelos reales y credenciales de producción.
- [ ] Validar endpoints con datos reales.

---

**Consejo:** Adjunta capturas de pantalla de Railway (servicios activos, logs, endpoints funcionando) para el examen o la entrega.

**Extra:** El README y la guía de migración a producción (`README_PROD_COCO_ML.md`) están actualizados y enlazados.
