"""
Script para criar um executável do Puzzle de 8 Peças.
Utiliza o PyInstaller para gerar um arquivo .exe autônomo.
"""
import os
import subprocess
import sys
import shutil

def build_executable():
    """Constrói o executável usando PyInstaller."""
    print("Iniciando a criação do executável...")
    
    # Verificar se o PyInstaller está instalado
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller não encontrado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Verificar se o Pillow está instalado (necessário para a interface)
    try:
        import PIL
    except ImportError:
        print("Pillow não encontrado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
    
    # Limpar diretórios de build anteriores
    if os.path.exists("build"):
        print("Removendo diretório 'build' anterior...")
        shutil.rmtree("build")
    
    if os.path.exists("dist"):
        print("Removendo diretório 'dist' anterior...")
        shutil.rmtree("dist")
    
    # Configuração do PyInstaller
    spec_file = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['interface.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Puzzle8Pecas',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
)
    """
    
    # Criar um ícone simples se não existir
    if not os.path.exists("icon.ico"):
        print("Criando ícone padrão...")
        try:
            from PIL import Image, ImageDraw
            
            # Criar uma imagem 128x128 para o ícone
            img = Image.new('RGBA', (128, 128), color=(0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Desenhar um quadrado com números para representar o puzzle
            draw.rectangle([(10, 10), (118, 118)], outline=(139, 69, 19), width=4, fill=(210, 180, 140))
            
            # Adicionar grade
            draw.line([(10, 46), (118, 46)], fill=(139, 69, 19), width=2)
            draw.line([(10, 82), (118, 82)], fill=(139, 69, 19), width=2)
            draw.line([(46, 10), (46, 118)], fill=(139, 69, 19), width=2)
            draw.line([(82, 10), (82, 118)], fill=(139, 69, 19), width=2)
            
            # Adicionar alguns números
            draw.text((28, 28), "1", fill=(0, 0, 0), align="center")
            draw.text((64, 28), "2", fill=(0, 0, 0), align="center")
            draw.text((100, 28), "3", fill=(0, 0, 0), align="center")
            draw.text((28, 64), "8", fill=(0, 0, 0), align="center")
            draw.text((100, 64), "4", fill=(0, 0, 0), align="center")
            draw.text((28, 100), "7", fill=(0, 0, 0), align="center")
            draw.text((64, 100), "6", fill=(0, 0, 0), align="center")
            draw.text((100, 100), "5", fill=(0, 0, 0), align="center")
            
            # Salvar como .ico
            img.save("icon.ico")
        except Exception as e:
            print(f"Erro ao criar ícone: {e}")
            # Continuar sem ícone
            spec_file = spec_file.replace("icon='icon.ico',", "")
    
    # Escrever o arquivo de especificação
    with open("puzzle8.spec", "w") as f:
        f.write(spec_file)
    
    # Executar o PyInstaller
    print("Executando PyInstaller...")
    subprocess.check_call([
        sys.executable, 
        "-m", 
        "PyInstaller", 
        "puzzle8.spec", 
        "--clean"
    ])
    
    print("\nExecutável criado com sucesso!")
    print(f"Você pode encontrá-lo em: {os.path.abspath('dist/Puzzle8Pecas.exe')}")

if __name__ == "__main__":
    build_executable()
