---
name: marketplace-installer
description: Generuje skrypt instalacyjny Marketplace dla prawników - Windows .bat (bez Git/npm). Użyj gdy - /marketplace install, "zainstaluj skille", "installer dla kancelarii", "jak zainstalować skille bez GitHub".
allowed-tools: Bash, Read, Write
license: Apache-2.0
data-residency: local
requires-human-approval: true
pii-egress: none
---

# Marketplace Installer

Generuje gotowe skrypty instalacyjne skilli dla docelowych użytkowników
bez wymagania Git, npm ani wiedzy technicznej.

## Safety Tiers

| Tier | Operacje | Reguła |
|------|----------|--------|
| **R** | Podgląd listy skilli do instalacji | Bez potwierdzenia |
| **M** | Generowanie skryptu .bat / .ps1 | Pokaż zawartość przed zapisem |
| **D** | Nadpisanie istniejących skilli w `~/.claude/skills/` | Użytkownik wpisuje "potwierdzam" |

## Tryby

### `/marketplace install [skill-slug]`
Generuje `install-lex-skills.bat` gotowy do uruchomienia.

### `/marketplace list`
Wyświetla dostępne skille z grounding-prawo z opisem.

### `/marketplace check`
Sprawdza co jest już zainstalowane w `~/.claude/skills/`.

## Workflow generowania instalatora

1. Pobierz `marketplace.json` z `elconcept/grounding-prawo` (ścieżka: `.claude-plugin/marketplace.json`)
3. Wygeneruj `install-skills.bat` (patrz szablon poniżej)
4. Wygeneruj `README-instalacja.txt` z instrukcją krok po kroku
5. Dostarcz oba gotowe pliki

## Szablon install-skills.bat

> **Szablon, nie gotowy plik.** Tryb `/marketplace install` podstawia dwa placeholdery przed zapisem `.bat` na dysk:
>
> - `__GIT_REF__` -> domyślnie tag najnowszej publikacji z `marketplace.json` (np. `refs/tags/v0.6.0`); k
> - `__SKILL_SLUGS__` -> lista slugów wybranych skilli, oddzielona spacjami (np. `redline-docx-pl saos-orzecznictwo`).
>
> Surowy szablon poniżej **nie zadziała** uruchomiony bez podstawienia.

```batch
@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

echo Marketplace Installer
echo ================================
echo Instaluje skille AI dla Claude Code
echo.

:: Katalog docelowy
set "SKILLS_DIR=%USERPROFILE%\.claude\skills"
if not exist "%SKILLS_DIR%" mkdir "%SKILLS_DIR%"

:: Tymczasowy katalog pobrania
set "TMP_DIR=%TEMP%\grounding-prawo-install-%RANDOM%"
mkdir "%TMP_DIR%"

echo [1/3] Pobieranie skilli z Marketplace...
:: __GIT_REF__ = refs/tags/vX.Y.Z (domyślnie najnowszy tag z marketplace.json) lub refs/heads/main (bleeding-edge).
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/elconcept/grounding-prawo/archive/__GIT_REF__.zip' -OutFile '%TMP_DIR%\skills.zip' -UseBasicParsing"

if not exist "%TMP_DIR%\skills.zip" (
    echo BLAD: Nie udalo sie pobrac. Sprawdz polaczenie z Internetem.
    pause
    exit /b 1
)

echo [2/3] Rozpakowywanie...
powershell -Command "Expand-Archive -Path '%TMP_DIR%\skills.zip' -DestinationPath '%TMP_DIR%\extracted' -Force"

echo [3/3] Instalowanie skilli...
:: [LISTA SKILLI - generowana dynamicznie]
:: UWAGA: nazwa katalogu po Expand-Archive zalezy od ref ZIPa - dla taga vX.Y.Z bedzie "grounding-prawo-X.Y.Z", dla main "grounding-prawo-main". Tryb /marketplace install podstawia __EXTRACTED_DIR__.
for %%S in (__SKILL_SLUGS__) do (
    set "SRC=%TMP_DIR%\extracted\__EXTRACTED_DIR__\skills\%%S"
    set "DST=%SKILLS_DIR%\%%S"
    if exist "!SRC!" (
        :: UWAGA: rd /s /q usuwa lokalne modyfikacje w skillu. Ostrzeżenie w README-instalacja.txt.
        if exist "!DST!" rd /s /q "!DST!"
        xcopy /e /i /q "!SRC!" "!DST!" >nul
        echo   OK: %%S
    ) else (
        echo   POMINIETY: %%S (nie znaleziono)
    )
)

:: Czyszczenie
rd /s /q "%TMP_DIR%"

echo.
echo ================================
echo Instalacja zakonczona!
echo Uruchom nowa sesje Claude Code.
echo Skille beda dostepne jako /nazwa-skilla
echo ================================
pause
```

## Szablon README-instalacja.txt

```
INSTRUKCJA INSTALACJI - Marketplace
=============================================

WYMAGANIA:
- Claude Code (pobierz z claude.ai/code)
- Polaczenie z Internetem

INSTALACJA:
1. Zweryfikuj zrodlo pliku - powinien pochodzic z oficjalnego release
   github.com/elconcept/grounding-prawo/releases.
2. Kliknij dwukrotnie install-skills.bat
   (Windows SmartScreen moze pokazac ostrzezenie. Jezeli plik pochodzi z innego
    zrodla niz oficjalny release - NIE uruchamiaj. Jezeli jest z release i polityka
    kancelarii pozwala - kliknij "Wiecej informacji" -> "Uruchom i tak".
    Prawa administratora NIE sa wymagane - skrypt pisze do %USERPROFILE%.)
4. Poczekaj az pojawi sie "Instalacja zakonczona!"
5. Uruchom Claude Code od nowa
6. Sprawdz: wpisz /szukaj-orzeczen "dobro dziecka" - komenda jest dostepna

PROBLEMY:
- Jesli Windows blokuje skrypt: Wlasciwosci pliku -> Odblokuj
```

## Uwagi techniczne

- Nie wymaga Git (używa `Invoke-WebRequest` + `Expand-Archive`)
- Nie wymaga npm/node
- Działa na Windows 10/11 z PowerShell 5.1+
- Skrypt **nadpisuje** istniejące skille o tych samych nazwach (lokalne modyfikacje skopiowanych skilli przepadają).
- Ścieżka docelowa: `%USERPROFILE%\.claude\skills\` (katalog skilli Claude Code w profilu użytkownika)
- **Reproducible install**: domyślny ref to **najnowszy tag** z `marketplace.json` (audytowalna wersja). Tryb `--ref main` pobiera `HEAD` (do testowania, nie do produkcji w kancelarii).
