# install_buildtools.ps1
# Script para instalar Visual Studio Build Tools y componentes necesarios para compilar paquetes Python con extensiones nativas

# Descargar el instalador de Build Tools
Invoke-WebRequest -Uri "https://aka.ms/vs/17/release/vs_BuildTools.exe" -OutFile "vs_BuildTools.exe"

# Instalar los componentes necesarios de forma silenciosa
Start-Process -Wait -FilePath ".\vs_BuildTools.exe" -ArgumentList `
  "--quiet --wait --norestart --nocache --installPath C:\BuildTools",
  "--add Microsoft.VisualStudio.Workload.VCTools",
  "--add Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
  "--add Microsoft.VisualStudio.Component.Windows10SDK.19041",
  "--add Microsoft.VisualStudio.Component.VC.CMake.Project",
  "--add Microsoft.VisualStudio.Component.VC.Redist.14.Latest",
  "--add Microsoft.VisualStudio.Component.VC.ATL",
  "--add Microsoft.VisualStudio.Component.VC.CoreBuildTools",
  "--add Microsoft.VisualStudio.Component.VC.Llvm.Clang",
  "--add Microsoft.VisualStudio.Component.VC.Runtimes.x86.x64",
  "--add Microsoft.VisualStudio.Component.VC.Tools.ARM64",
  "--add Microsoft.VisualStudio.Component.VC.Tools.ARM",
  "--add Microsoft.VisualStudio.Component.VC.140",
  "--add Microsoft.VisualStudio.Component.VC.141",
  "--add Microsoft.VisualStudio.Component.VC.142",
  "--add Microsoft.VisualStudio.Component.VC.143",
  "--add Microsoft.VisualStudio.Component.PythonTools",
  "--add Microsoft.VisualStudio.Component.Python3.x64"
