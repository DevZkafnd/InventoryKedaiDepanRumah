; Inno Setup Script untuk Inventory Kedai Depan Rumah
; Installer otomatis dengan Python embedded

#define MyAppName "Inventory Kedai"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Kedai Depan Rumah"
#define MyAppURL "https://github.com/yourusername/inventory-kedai-depan-rumah"
#define MyAppExeName "jalankan.bat"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=output
OutputBaseFilename=InventoryKedai-Setup-{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
SetupIconFile=..\static\img\logo.ico
UninstallDisplayIcon={app}\static\img\logo.ico

[Languages]
Name: "indonesian"; MessagesFile: "compiler:Languages\Indonesian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "quicklaunchicon"; Description: "Create a Quick Launch icon"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Semua file aplikasi
Source: "..\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "*.pyc,__pycache__,*.git*,.env,.vscode,installer,build,dist,*.spec"
; Python embedded (akan di-download atau di-bundle)
Source: "python-embed\*"; DestDir: "{app}\python-embed"; Flags: ignoreversion recursesubdirs createallsubdirs

[Dirs]
Name: "{app}\logs"; Permissions: users-modify
Name: "{app}\media"; Permissions: users-modify

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"
Name: "{group}\Stop {#MyAppName}"; Filename: "taskkill"; Parameters: "/F /IM python.exe"; WorkingDir: "{app}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
; Setup awal setelah install
Filename: "{app}\setup_first_run.bat"; Description: "Setup awal database dan dependencies"; Flags: postinstall runhidden waituntilterminated
Filename: "{app}\{#MyAppExeName}"; Description: "Jalankan {#MyAppName}"; Flags: postinstall nowait skipifsilent

[Code]
var
  PortPage: TInputQueryWizardPage;
  SecretKeyPage: TInputQueryWizardPage;

procedure InitializeWizard;
begin
  // Page untuk konfigurasi port
  PortPage := CreateInputQueryPage(wpSelectDir,
    'Konfigurasi Server', 'Atur port untuk web server',
    'Masukkan port yang akan digunakan (default: 8000)');
  PortPage.Add('Port:', False);
  PortPage.Values[0] := '8000';
  
  // Page untuk secret key
  SecretKeyPage := CreateInputQueryPage(PortPage.ID,
    'Konfigurasi Keamanan', 'Atur Django Secret Key',
    'Biarkan kosong untuk generate otomatis');
  SecretKeyPage.Add('Secret Key (opsional):', False);
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  Port: String;
  SecretKey: String;
  EnvFile: String;
begin
  if CurStep = ssPostInstall then
  begin
    Port := PortPage.Values[0];
    SecretKey := SecretKeyPage.Values[0];
    EnvFile := ExpandConstant('{app}\.env');
    
    // Copy .env_default ke .env dan update values
    FileCopy(ExpandConstant('{app}\.env_default'), EnvFile, False);
    
    // Buat file config untuk port
    SaveStringToFile(ExpandConstant('{app}\config_port.txt'), Port, False);
    
    if SecretKey <> '' then
    begin
      SaveStringToFile(ExpandConstant('{app}\config_secretkey.txt'), SecretKey, False);
    end;
  end;
end;
