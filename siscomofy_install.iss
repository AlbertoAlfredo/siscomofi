[Setup]
AppName=SISCOMOFI
AppVersion=1.0
DefaultDirName=C:\siscomofi
DisableDirPage=yes
DisableProgramGroupPage=yes
OutputDir=.
OutputBaseFilename=siscomofi_installer
Compression=lzma
SolidCompression=yes
AllowNoIcons=yes
PrivilegesRequired=admin

[Files]
; Copia TUDO da pasta dist/siscomofi para C:\siscomofi
Source: "dist\siscomofi\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs replaceexisting

[Icons]
; Atalho no Menu Iniciar
Name: "{group}\SISCOMOFI"; Filename: "{app}\siscomofi.exe"

; Atalho na Área de Trabalho
Name: "{desktop}\SISCOMOFI"; Filename: "{app}\siscomofi.exe"

[Run]
Filename: "{app}\siscomofi.exe"; Description: "Executar o SISCOMOFI agora"; Flags: nowait postinstall skipifsilent
