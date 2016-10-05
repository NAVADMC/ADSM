##########
# NSIS for ADSM
##########
!define APP_NAME "ADSM"
!define COMP_NAME "Newline Technical Innovations"
!define WEB_SITE "https://www.newline.us"
!define DOC_SITE "https://github.com/NAVADMC/ADSM/wiki"
!define VERSION "3.3.8.0"
!define COPYRIGHT ""
!define DESCRIPTION "ADSM GUI Application"
!define LICENSE_TXT "LICENSE"
!define INSTALLER_NAME "dist\ADSM_Installer.exe"
!define MAIN_APP_EXE "ADSM.exe"
!define INSTALL_TYPE "SetShellVarContext current"
!define REG_ROOT "HKCU"
!define REG_APP_PATH "Software\Microsoft\Windows\CurrentVersion\App Paths\${MAIN_APP_EXE}"
!define UNINSTALL_PATH "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"

!define REG_START_MENU "Start Menu Folder"

var SM_Folder

##########
VIProductVersion  "${VERSION}"
VIAddVersionKey "ProductName"  "${APP_NAME}"
VIAddVersionKey "CompanyName"  "${COMP_NAME}"
VIAddVersionKey "LegalCopyright"  "${COPYRIGHT}"
VIAddVersionKey "FileDescription"  "${DESCRIPTION}"
VIAddVersionKey "FileVersion"  "${VERSION}"

##########
SetCompressor ZLIB
Name "${APP_NAME}"
Caption "${APP_NAME}"
OutFile "${INSTALLER_NAME}"
BrandingText "${APP_NAME}"
XPStyle on
InstallDirRegKey "${REG_ROOT}" "${REG_APP_PATH}" ""
InstallDir "$PROGRAMFILES64\ADSM"

##########
!define StrRep "!insertmacro StrRep"
!macro StrRep output string old new
Push `${string}`
Push `${old}`
Push `${new}`
!ifdef __UNINSTALL__
    Call un.StrRep
!else
    Call StrRep
!endif
Pop ${output}
!macroend

!macro Func_StrRep un
Function ${un}StrRep
Exch $R2 ;new
Exch 1
Exch $R1 ;old
Exch 2
Exch $R0 ;string
Push $R3
Push $R4
Push $R5
Push $R6
Push $R7
Push $R8
Push $R9

StrCpy $R3 0
StrLen $R4 $R1
StrLen $R6 $R0
StrLen $R9 $R2
loop:
StrCpy $R5 $R0 $R4 $R3
StrCmp $R5 $R1 found
StrCmp $R3 $R6 done
IntOp $R3 $R3 + 1 ;move offset by 1 to check the next character
Goto loop
found:
StrCpy $R5 $R0 $R3
IntOp $R8 $R3 + $R4
StrCpy $R7 $R0 "" $R8
StrCpy $R0 $R5$R2$R7
StrLen $R6 $R0
IntOp $R3 $R3 + $R9 ;move offset by length of the replacement string
Goto loop
done:

Pop $R9
Pop $R8
Pop $R7
Pop $R6
Pop $R5
Pop $R4
Pop $R3
Push $R0
Push $R1
Pop $R0
Pop $R1
Pop $R0
Pop $R2
Exch $R1
FunctionEnd
!macroend

!insertmacro Func_StrRep ""
!insertmacro Func_StrRep "un."

##########
!include "MUI.nsh"

!define MUI_ABORTWARNING
!define MUI_UNABORTWARNING

!insertmacro MUI_PAGE_WELCOME

!ifdef LICENSE_TXT
!insertmacro MUI_PAGE_LICENSE "${LICENSE_TXT}"
!endif

!insertmacro MUI_PAGE_DIRECTORY

Var WorkspacePath
!define MUI_PAGE_HEADER_SUBTEXT "Choose the User Workspace folder for ADSM."
!define MUI_DIRECTORYPAGE_TEXT_TOP "The installer will tell ADSM to use the following workspace folder. To use a different folder, click Browse and select another folder.$\r$\n$\r$\nTo allow MULTIPLE USERS, leave the field blank so ADSM will attempt to detect the appropriate workspace folder for each user$\r$\nNote: this MAY not work on systems where user files are stored on networked shares.$\r$\nClick Next to continue."
!define MUI_DIRECTORYPAGE_VARIABLE $WorkspacePath
!define MUI_PAGE_CUSTOMFUNCTION_LEAVE DirectoryLeave
!define MUI_DIRECTORYPAGE_VERIFYONLEAVE
!insertmacro MUI_PAGE_DIRECTORY

Var good
Function DirectoryLeave
StrCpy $good 0
Pop $good
FunctionEnd

!ifdef REG_START_MENU
!define MUI_STARTMENUPAGE_DEFAULTFOLDER "${APP_NAME}"
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "${REG_ROOT}"
!define MUI_STARTMENUPAGE_REGISTRY_KEY "${UNINSTALL_PATH}"
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "${REG_START_MENU}"
!insertmacro MUI_PAGE_STARTMENU Application $SM_Folder
!endif

!insertmacro MUI_PAGE_INSTFILES

!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM

!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

##########
Function .onInit
StrCpy $WorkspacePath "$DOCUMENTS\ADSM Workspace"
FunctionEnd

##########
!include LogicLib.nsh
Var CleanedWSP

Section -MainProgram
${INSTALL_TYPE}
SetOverwrite ifnewer
SetOutPath "$INSTDIR"
${StrRep} $CleanedWSP $WorkspacePath '\' '\\'
File /r "build\*"
FileOpen $0 $INSTDIR\settings.ini w
FileWrite $0 "WORKSPACE_PATH = '$CleanedWSP'"
FileClose $0
SectionEnd

##########

Section -Icons_Reg
SetOutPath "$INSTDIR"
WriteUninstaller "$INSTDIR\uninstall.exe"

!ifdef REG_START_MENU
!insertmacro MUI_STARTMENU_WRITE_BEGIN Application
CreateDirectory "$SMPROGRAMS\$SM_Folder"
CreateShortCut "$SMPROGRAMS\$SM_Folder\${APP_NAME}.lnk" "$INSTDIR\${MAIN_APP_EXE}"
CreateShortCut "$SMPROGRAMS\$SM_Folder\Uninstall ${APP_NAME}.lnk" "$INSTDIR\uninstall.exe"

!ifdef WEB_SITE
WriteIniStr "$INSTDIR\${COMP_NAME} Website.url" "InternetShortcut" "URL" "${WEB_SITE}"
CreateShortCut "$SMPROGRAMS\$SM_Folder\${COMP_NAME} Website.lnk" "$INSTDIR\${COMP_NAME} Website.url"
!endif
!ifdef DOC_SITE
WriteIniStr "$INSTDIR\${APP_NAME} Documentation.url" "InternetShortcut" "URL" "${DOC_SITE}"
CreateShortCut "$SMPROGRAMS\$SM_Folder\${APP_NAME} Documentation.lnk" "$INSTDIR\${APP_NAME} Documentation.url"
!endif
!insertmacro MUI_STARTMENU_WRITE_END
!endif

!ifndef REG_START_MENU
CreateDirectory "$SMPROGRAMS\ADSM"
CreateShortCut "$SMPROGRAMS\ADSM\${APP_NAME}.lnk" "$INSTDIR\${MAIN_APP_EXE}"
CreateShortCut "$SMPROGRAMS\ADSM\Uninstall ${APP_NAME}.lnk" "$INSTDIR\uninstall.exe"

!ifdef WEB_SITE
WriteIniStr "$INSTDIR\${COMP_NAME} Website.url" "InternetShortcut" "URL" "${WEB_SITE}"
CreateShortCut "$SMPROGRAMS\ADSM\${COMP_NAME} Website.lnk" "$INSTDIR\${COMP_NAME} Website.url"
!endif
!ifdef DOC_SITE
WriteIniStr "$INSTDIR\${APP_NAME} Documentation.url" "InternetShortcut" "URL" "${DOC_SITE}"
CreateShortCut "$SMPROGRAMS\ADSM\${APP_NAME} Documentation.lnk" "$INSTDIR\${APP_NAME} Documentation.url"
!endif
!endif

WriteRegStr ${REG_ROOT} "${REG_APP_PATH}" "" "$INSTDIR\${MAIN_APP_EXE}"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "DisplayName" "${APP_NAME}"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "UninstallString" "$INSTDIR\uninstall.exe"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "DisplayIcon" "$INSTDIR\${MAIN_APP_EXE}"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "DisplayVersion" "${VERSION}"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "Publisher" "${COMP_NAME}"

!ifdef WEB_SITE
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "URLInfoAbout" "${WEB_SITE}"
!endif
!ifdef DOC_SITE
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "URLInfoDocumentation" "${DOC_SITE}"
!endif
SectionEnd

##########
Section Uninstall
${INSTALL_TYPE}
Delete "$INSTDIR\uninstall.exe"
!ifdef WEB_SITE
Delete "$INSTDIR\${COMP_NAME} Website.url"
!endif
!ifdef DOC_SITE
Delete "$INSTDIR\${APP_NAME} Documentation.url"
!endif

RMDir /r /REBOOTOK "$INSTDIR"

!ifdef REG_START_MENU
!insertmacro MUI_STARTMENU_GETFOLDER "Application" $SM_Folder
Delete "$SMPROGRAMS\$SM_Folder\${APP_NAME}.lnk"
Delete "$SMPROGRAMS\$SM_Folder\Uninstall ${APP_NAME}.lnk"
!ifdef WEB_SITE
Delete "$SMPROGRAMS\$SM_Folder\${COMP_NAME} Website.lnk"
!endif
!ifdef DOC_SITE
Delete "$SMPROGRAMS\$SM_Folder\${APP_NAME} Documentation.lnk"
!endif
RmDir "$SMPROGRAMS\$SM_Folder"
!endif

!ifndef REG_START_MENU
Delete "$SMPROGRAMS\ADSM\${APP_NAME}.lnk"
Delete "$SMPROGRAMS\ADSM\Uninstall ${APP_NAME}.lnk"
!ifdef WEB_SITE
Delete "$SMPROGRAMS\ADSM\${COMP_NAME} Website.lnk"
!endif
!ifdef DOC_SITE
Delete "$SMPROGRAMS\ADSM\${APP_NAME} Documentation.lnk"
!endif
RmDir "$SMPROGRAMS\ADSM"
!endif

DeleteRegKey ${REG_ROOT} "${REG_APP_PATH}"
DeleteRegKey ${REG_ROOT} "${UNINSTALL_PATH}"
SectionEnd

