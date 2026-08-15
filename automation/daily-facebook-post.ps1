<<<<<<< HEAD
# ============================================
# AI Social Media Manager - Daily Facebook Post
# ============================================

$ErrorActionPreference = "Stop"

# ---------- Configuration ----------
$flowiseBaseUrl = "http://localhost:3000"
$flowId = "0a25104b-9f24-4867-9bfa-643a0d9324a7"

# Leave empty if your Flowise flow is not API-key protected
$flowiseApiKey = ""

$logDirectory = "C:\AI Agent\logs"
$today = Get-Date -Format "yyyy-MM-dd"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$logFile = Join-Path $logDirectory "facebook-post-$today.log"

# ---------- Create log directory ----------
if (-not (Test-Path $logDirectory)) {
    New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
}

function Write-Log {
    param([string]$Message)

    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - $Message"
    Add-Content -Path $logFile -Value $line
    Write-Output $line
}

try {
    Write-Log "Daily Facebook automation started."

    
    # ---------- Check Flowise ----------
    try {
        Invoke-WebRequest `
            -Uri $flowiseBaseUrl `
            -UseBasicParsing `
            -TimeoutSec 15 | Out-Null

        Write-Log "Flowise is available."
    }
    catch {
        throw "Flowise is not running at $flowiseBaseUrl."
    }

    # ---------- Daily prompt ----------
    $prompt = @"
Create today's professional Facebook post for an AI technology page.

Choose one fresh, useful topic related to:
- Artificial intelligence
- Business automation
- Generative AI
- Machine learning
- Digital transformation
- AI productivity
- Cloud and AI
- Future technology

Requirements:
- Write a professional Facebook caption.
- Include a clear call to action.
- Add exactly 5 relevant hashtags.
- Generate a premium square 1:1 image.
- Do not include logos, watermarks, or embedded text in the image.
- Publish the generated caption and image to my configured Facebook Page.
- Return only the real Facebook publishing result.
"@

    $requestBody = @{
        question = $prompt
        streaming = $false
        overrideConfig = @{
            sessionId = "daily-facebook-$today"
        }
    } | ConvertTo-Json -Depth 10

    $headers = @{}

    if (-not [string]::IsNullOrWhiteSpace($flowiseApiKey)) {
        $headers["Authorization"] = "Bearer $flowiseApiKey"
    }

    $predictionUrl = "$flowiseBaseUrl/api/v1/prediction/$flowId"

    Write-Log "Calling Flowise Prediction API."

    $response = Invoke-RestMethod `
        -Method Post `
        -Uri $predictionUrl `
        -Headers $headers `
        -ContentType "application/json" `
        -Body $requestBody `
        -TimeoutSec 600

    $responseJson = $response | ConvertTo-Json -Depth 20
    Write-Host "----- RAW FLOWISE RESPONSE -----"
    Write-Host $responseJson
    Write-Host "-------------------------------"

    Write-Log "Flowise response:"
    Add-Content -Path $logFile -Value $responseJson

    # Basic success validation
   # Extract the actual Flowise text output
$responseText = ""

if ($null -ne $response.text) {
    $responseText = [string]$response.text
}
else {
    $responseText = $responseJson
}

Write-Log "Flowise text output:"
Add-Content -Path $logFile -Value $responseText

try {
    $facebookResult = $responseText | ConvertFrom-Json

    if (
        -not [string]::IsNullOrWhiteSpace($facebookResult.post_id) -and
        -not [string]::IsNullOrWhiteSpace($facebookResult.id)
    ) {
        Write-Log "Facebook post published successfully."
        Write-Log "Facebook photo ID: $($facebookResult.id)"
        Write-Log "Facebook post ID: $($facebookResult.post_id)"
        exit 0
    }
}
catch {
    Write-Log "Flowise text was not valid Facebook JSON."
}

Write-Log "Workflow completed, but no valid Facebook post ID was detected."
exit 1
}
catch {
    Write-Log "ERROR: $($_.Exception.Message)"

    if ($_.ErrorDetails.Message) {
        Write-Log "DETAILS: $($_.ErrorDetails.Message)"
    }

    exit 1
=======
# ============================================
# AI Social Media Manager - Daily Facebook Post
# ============================================

$ErrorActionPreference = "Stop"

# ---------- Configuration ----------
$flowiseBaseUrl = "http://localhost:3000"
$flowId = "0a25104b-9f24-4867-9bfa-643a0d9324a7"

# Leave empty if your Flowise flow is not API-key protected
$flowiseApiKey = ""

$logDirectory = "C:\AI Agent\logs"
$today = Get-Date -Format "yyyy-MM-dd"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$logFile = Join-Path $logDirectory "facebook-post-$today.log"

# ---------- Create log directory ----------
if (-not (Test-Path $logDirectory)) {
    New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
}

function Write-Log {
    param([string]$Message)

    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - $Message"
    Add-Content -Path $logFile -Value $line
    Write-Output $line
}

try {
    Write-Log "Daily Facebook automation started."

    
    # ---------- Check Flowise ----------
    try {
        Invoke-WebRequest `
            -Uri $flowiseBaseUrl `
            -UseBasicParsing `
            -TimeoutSec 15 | Out-Null

        Write-Log "Flowise is available."
    }
    catch {
        throw "Flowise is not running at $flowiseBaseUrl."
    }

    # ---------- Daily prompt ----------
    $prompt = @"
Create today's professional Facebook post for an AI technology page.

Choose one fresh, useful topic related to:
- Artificial intelligence
- Business automation
- Generative AI
- Machine learning
- Digital transformation
- AI productivity
- Cloud and AI
- Future technology

Requirements:
- Write a professional Facebook caption.
- Include a clear call to action.
- Add exactly 5 relevant hashtags.
- Generate a premium square 1:1 image.
- Do not include logos, watermarks, or embedded text in the image.
- Publish the generated caption and image to my configured Facebook Page.
- Return only the real Facebook publishing result.
"@

    $requestBody = @{
        question = $prompt
        streaming = $false
        overrideConfig = @{
            sessionId = "daily-facebook-$today"
        }
    } | ConvertTo-Json -Depth 10

    $headers = @{}

    if (-not [string]::IsNullOrWhiteSpace($flowiseApiKey)) {
        $headers["Authorization"] = "Bearer $flowiseApiKey"
    }

    $predictionUrl = "$flowiseBaseUrl/api/v1/prediction/$flowId"

    Write-Log "Calling Flowise Prediction API."

    $response = Invoke-RestMethod `
        -Method Post `
        -Uri $predictionUrl `
        -Headers $headers `
        -ContentType "application/json" `
        -Body $requestBody `
        -TimeoutSec 600

    $responseJson = $response | ConvertTo-Json -Depth 20
    Write-Host "----- RAW FLOWISE RESPONSE -----"
    Write-Host $responseJson
    Write-Host "-------------------------------"

    Write-Log "Flowise response:"
    Add-Content -Path $logFile -Value $responseJson

    # Basic success validation
   # Extract the actual Flowise text output
$responseText = ""

if ($null -ne $response.text) {
    $responseText = [string]$response.text
}
else {
    $responseText = $responseJson
}

Write-Log "Flowise text output:"
Add-Content -Path $logFile -Value $responseText

try {
    $facebookResult = $responseText | ConvertFrom-Json

    if (
        -not [string]::IsNullOrWhiteSpace($facebookResult.post_id) -and
        -not [string]::IsNullOrWhiteSpace($facebookResult.id)
    ) {
        Write-Log "Facebook post published successfully."
        Write-Log "Facebook photo ID: $($facebookResult.id)"
        Write-Log "Facebook post ID: $($facebookResult.post_id)"
        exit 0
    }
}
catch {
    Write-Log "Flowise text was not valid Facebook JSON."
}

Write-Log "Workflow completed, but no valid Facebook post ID was detected."
exit 1
}
catch {
    Write-Log "ERROR: $($_.Exception.Message)"

    if ($_.ErrorDetails.Message) {
        Write-Log "DETAILS: $($_.ErrorDetails.Message)"
    }

    exit 1
>>>>>>> 8765d3c6c178c0579b55bbaf6e8cedcffc29f69b
}