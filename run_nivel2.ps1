# Simple runner - just execute and see what happens
# Save as run_nivel2.ps1

param([string]$ExePath = ".\Nivel-2.exe")

Write-Host "=== Running with no args ===" -ForegroundColor Cyan
& $ExePath 2>&1 | Write-Host

Write-Host "`n=== Running with 'test' ===" -ForegroundColor Cyan  
& $ExePath "test" 2>&1 | Write-Host

Write-Host "`n=== Running with level1 flag ===" -ForegroundColor Cyan
& $ExePath "cyth_acapfh7sp9wy@cyberint.ro" 2>&1 | Write-Host

Write-Host "`nDone."
pause
