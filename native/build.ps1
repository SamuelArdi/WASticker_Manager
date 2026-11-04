Set-Location $PSScriptRoot

$ErrorActionPreference = 'Stop'
$src = Join-Path $PSScriptRoot 'native.cpp'
$out = Join-Path "..\src" "native.dll"

$cxx = (Get-Command g++.exe -ErrorAction SilentlyContinue) ?? (Get-Command clang++.exe -ErrorAction SilentlyContinue)
if (-not $cxx) { throw "No compiler on PATH. Run: winget install -e --id BrechtSanders.WinLibs.POSIX.UCRT" }

& $cxx.Source -shared -O2 -static -static-libgcc -static-libstdc++ -o $out $src
if (-not (Test-Path $out)) { throw "Build failed - no $out produced" }
"Built $out"
