# Limpieza automática del framework: elimina archivos/carpetas no esenciales
import os
import shutil

# Lista de carpetas/archivos a conservar (ajusta según tu funcionalidad principal)
KEEP = [
    '.git', '.github', 'ml_core', 'device_farm', 'gologin_automation', 'orchestration', 'monitoring', 'config', 'scripts', 'requirements.txt', 'requirements-ml.txt', 'requirements-dev.txt', 'README.md', 'README_PROD_COCO_ML.md', 'RAILWAY_DEPLOYMENT_CHECKLIST.md', 'pyproject.toml', 'setup.py', 'Makefile', 'start.sh', 'docker', 'tests', '.gitignore', 'LICENSE', 'railway_launcher.py'
]

for item in os.listdir('.'):
    if item not in KEEP:
        if os.path.isdir(item):
            print(f'Removiendo carpeta: {item}')
            shutil.rmtree(item)
        else:
            print(f'Removiendo archivo: {item}')
            os.remove(item)

print('Limpieza completada. Solo quedan los archivos y carpetas esenciales.')
