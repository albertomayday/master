# Checklist y Guía de Transición a Producción Real (COCO/ML)

Este documento te ayuda a migrar el sistema de modo dummy a producción real con modelos COCO y ML, evitando errores típicos y asegurando un despliegue profesional.

## 1. Cambia a modo producción
- Edita tu `.env` o variables de entorno:
  ```
  DUMMY_MODE=false
  ENVIRONMENT=production
  ```
- (Opcional) Edita el Dockerfile para que `ENV DUMMY_MODE=false`.

## 2. Prepara los modelos y datasets reales
- Descarga los modelos YOLOv8 entrenados o entrena los tuyos propios.
- Coloca los pesos en `/app/data/models/production/`.
- Descarga el dataset COCO completo y colócalo en `/app/data/datasets/coco/`.
- Edita `config/ml/model_config.yaml` para que apunte a los paths y dispositivos correctos.

## 3. Configura credenciales y secretos reales
- Rellena `.env` con:
  - API_KEY, API_SECRET_KEY
  - META_ACCESS_TOKEN, META_APP_ID, META_PIXEL_ID, etc.
  - POSTGRES_USER, POSTGRES_PASSWORD, etc.
  - Cualquier otro secreto necesario para servicios externos.
- Usa los secretos de GitHub Actions y Railway para producción.

## 4. Verifica dependencias y recursos
- GPU: Si usas GPU, asegúrate de que el entorno Docker y Railway soportan CUDA.
- RAM/CPU: Los modelos grandes requieren más recursos.
- Prueba los scripts de setup y entrenamiento (`scripts/setup_yolo_models.py`, `ml_core/training/train_yolo.py`).

## 5. Despliegue seguro
- Haz push a `main` en GitHub.
- El workflow construirá y subirá la imagen a Docker Hub.
- Railway desplegará automáticamente la nueva imagen.
- Verifica logs y endpoints en Railway para asegurar que todo funciona.

## 6. Validación final
- Accede al dashboard y la API en Railway.
- Prueba endpoints de inferencia y entrenamiento.
- Lanza campañas y workflows reales.

---

**Consejo:** Mantén siempre un entorno dummy para pruebas rápidas y un entorno producción bien aislado para datos y modelos reales.

---

_Actualiza este documento con cada nueva integración o cambio de arquitectura._
