.venv\Scripts\activate

Get-Content .env | ForEach-Object {
    if ($_ -match '=') {
        $parts = $_ -split '=', 2
        $key = $parts[0].Trim()
        $value = $parts[1].Trim()
        [System.Environment]::SetEnvironmentVariable($key, $value, "Process")
    }
}

python app.py
