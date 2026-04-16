# Nivel-2 CTF Solver - Run this on Windows with .NET Framework 4.x
# Save as solve_nivel2.ps1 and run: powershell -ExecutionPolicy Bypass -File solve_nivel2.ps1

param(
    [string]$ExePath = ".\Nivel-2.exe"
)

Write-Host "[*] Loading assembly: $ExePath" -ForegroundColor Cyan

try {
    # Load the assembly bytes to avoid file locking
    $bytes = [System.IO.File]::ReadAllBytes((Resolve-Path $ExePath))
    $assembly = [System.Reflection.Assembly]::Load($bytes)
    
    Write-Host "[+] Assembly loaded: $($assembly.FullName)" -ForegroundColor Green
    
    # List all types
    Write-Host "`n[*] Types in assembly:" -ForegroundColor Cyan
    foreach ($type in $assembly.GetTypes()) {
        Write-Host "  Type: $($type.Name) (BaseType: $($type.BaseType))" -ForegroundColor Yellow
        
        # List methods
        $methods = $type.GetMethods([System.Reflection.BindingFlags]::Static -bor 
                                     [System.Reflection.BindingFlags]::NonPublic -bor
                                     [System.Reflection.BindingFlags]::Public -bor
                                     [System.Reflection.BindingFlags]::Instance)
        foreach ($method in $methods) {
            $params = ($method.GetParameters() | ForEach-Object { "$($_.ParameterType) $($_.Name)" }) -join ", "
            Write-Host "    Method: $($method.Name)($params) -> $($method.ReturnType)" -ForegroundColor Gray
        }
        
        # List fields with values
        $fields = $type.GetFields([System.Reflection.BindingFlags]::Static -bor 
                                   [System.Reflection.BindingFlags]::NonPublic -bor
                                   [System.Reflection.BindingFlags]::Public -bor
                                   [System.Reflection.BindingFlags]::Instance)
        foreach ($field in $fields) {
            Write-Host "    Field: $($field.Name) ($($field.FieldType))" -ForegroundColor DarkGray
            if ($field.IsStatic) {
                try {
                    $val = $field.GetValue($null)
                    if ($val -ne $null) {
                        if ($val -is [byte[]]) {
                            Write-Host "      Value: byte[$($val.Length)] = $([BitConverter]::ToString($val, 0, [Math]::Min(32, $val.Length)))..." -ForegroundColor White
                        } else {
                            Write-Host "      Value: $val" -ForegroundColor White
                        }
                    }
                } catch {}
            }
        }
    }
    
    # Try to find and invoke the entry point
    Write-Host "`n[*] Entry point: $($assembly.EntryPoint)" -ForegroundColor Cyan
    
    if ($assembly.EntryPoint) {
        Write-Host "[*] Attempting to run with various flag formats..." -ForegroundColor Cyan
        
        # First, try running without arguments to see default output
        Write-Host "`n--- Running with no args ---" -ForegroundColor Magenta
        try {
            $assembly.EntryPoint.Invoke($null, @(,@()))
        } catch {
            Write-Host "  Error: $($_.Exception.InnerException.Message)" -ForegroundColor Red
        }
        
        # Try with a test argument
        Write-Host "`n--- Running with test arg ---" -ForegroundColor Magenta
        try {
            $assembly.EntryPoint.Invoke($null, @(,@("test")))
        } catch {
            Write-Host "  Error: $($_.Exception.InnerException.Message)" -ForegroundColor Red
        }
    }
    
} catch {
    Write-Host "[!] Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host $_.Exception.ToString() -ForegroundColor DarkRed
}

Write-Host "`n[*] Done. Press any key..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
