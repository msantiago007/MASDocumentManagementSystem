# DeployDatabase.ps1
param(
    [string]$ServerInstance = "localhost",
    [string]$DatabaseName = "DocumentManagement",
    [string]$ScriptsPath = ".\DatabaseScripts"
)

# Function to execute SQL scripts
function Execute-SqlScript {
    param(
        [string]$ScriptPath,
        [string]$ServerInstance,
        [string]$DatabaseName
    )
    
    try {
        Write-Host "Executing $ScriptPath..."
        $script = Get-Content -Path $ScriptPath -Raw
        Invoke-Sqlcmd -ServerInstance $ServerInstance -Database "master" -Query $script -ErrorAction Stop
        Write-Host "Successfully executed $ScriptPath" -ForegroundColor Green
    }
    catch {
        Write-Host "Error executing $ScriptPath" -ForegroundColor Red
        Write-Host $_.Exception.Message
        throw
    }
}

# Main deployment script
try {
    Write-Host "Starting database deployment..." -ForegroundColor Yellow
    
    # Execute scripts in order
    $scripts = @(
        "01_CreateDatabase.sql",
        "02_CreateTables.sql",
        "03_CreateConstraints.sql",
        "04_CreateIndexes.sql",
        "05_InitialData.sql"
    )
    
    foreach ($script in $scripts) {
        $scriptPath = Join-Path $ScriptsPath $script
        Execute-SqlScript -ScriptPath $scriptPath -ServerInstance $ServerInstance -DatabaseName $DatabaseName
    }
    
    Write-Host "Database deployment completed successfully!" -ForegroundColor Green
}
catch {
    Write-Host "Database deployment failed!" -ForegroundColor Red
    Write-Host $_.Exception.Message
    exit 1
}