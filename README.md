# Mi Watch Health Data -- Complete Mac Setup & User Manual

**Platform:** macOS\
**Watch application:** Xiaomi Mi Fitness\
**Data connector:** Mi Fitness Data Bridge\
**Dashboard:** HTML + JavaScript\
**Cloud region:** India (`i2`)

## 1. Introduction

This guide explains how to download health data from a Xiaomi Mi Watch,
store it locally on a Mac, export it to JSON/CSV and view it through a
local HTML dashboard.

Workflow:

1.  Install the Mi Fitness Data Bridge.
2.  Obtain Xiaomi `user_id` and `passToken`.
3.  Configure the bridge using India region `i2`.
4.  Verify cloud connectivity.
5.  Synchronise health data.
6.  Export data to JSON.
7.  Install and launch the HTML dashboard.
8.  Refresh the dashboard after new synchronisations.

All health data is stored locally on the Mac.

> **Important:** The bridge is an unofficial community project using
> non-public Xiaomi cloud interfaces, which may change. The `i2` region
> worked in our tested setup, but compatibility is not guaranteed for
> every account or device.

## 🏗️ Architecture

The end-to-end data flow from Mi Watch to the local analytics dashboard.

![Mi Watch Dashboard Architecture](architecture.png)

## 📊 Dashboard Preview

Explore your daily activity, sleep patterns, heart rate and other available health metrics.

![Mi Watch Health Dashboard](screenshot.png)

## 2. Prerequisites

  Requirement   Details
  ------------- -------------------------------------
  Computer      Mac running macOS
  Python        Python 3.11 or later
  Git           Installed
  Browser       Firefox or Chrome
  Mi Fitness    Installed and paired with the watch
  Internet      Required for cloud synchronisation

Check Python and Git:

``` bash
python3 --version
git --version
```

## 3. Install Mi Fitness Data Bridge

### Step 1 -- Create the working directory

``` bash
mkdir -p ~/MiWatchData
cd ~/MiWatchData
```

### Step 2 -- Clone the GitHub repository

``` bash
git clone https://github.com/shkyyy18/mi_fitness_data_bridge.git mi-fitness-data-bridge
cd ~/MiWatchData/mi-fitness-data-bridge
```

### Step 3 -- Create and activate a Python virtual environment

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 4 -- Install the bridge

``` bash
pip install -e .
```

Verify:

``` bash
mi-fitness-bridge
```

## 4. Obtain Xiaomi account credentials

The bridge requires two Xiaomi account values:

-   `user_id`
-   `passToken`

**Important:** `passToken` is a session credential, not your normal
Xiaomi account password. Treat it like a password.

### Step 1 -- Open Xiaomi account in Firefox

1.  Launch Firefox.
2.  Open https://account.xiaomi.com
3.  Sign in using your Xiaomi account.
4.  Keep the authenticated page open.

### Step 2 -- Open Firefox Developer Tools

1.  Press `F12`.
2.  Open the **Storage** tab.
3.  Expand **Cookies**.
4.  Select the Xiaomi account domain, normally
    `https://account.xiaomi.com`.
5.  Locate cookies named `userId` and `passToken`.

### Step 3 -- Copy the values locally

Copy the values of `userId` and `passToken`. Use them only in the
interactive setup below.

**Security precautions:**

-   Never paste `passToken` into ChatGPT or another online service.
-   Never put it in a Terminal command.
-   Never save it in a shell script or text file.
-   Never share screenshots showing the token.
-   Do not send browser cookies to third-party token extraction
    websites.

The token may expire or be rotated by Xiaomi. If authentication stops
working, obtain a fresh credential through a method you trust.

## 5. Configure Mi Fitness Data Bridge

### Step 1 -- Start the interactive setup

``` bash
cd ~/MiWatchData/mi-fitness-data-bridge
source .venv/bin/activate
mi-fitness-bridge setup
```

### Step 2 -- Enter your credentials

  Prompt                 Value
  ---------------------- -------------------------------
  Mi Fitness user_id     Paste your copied `userId`
  Mi Fitness passToken   Paste your copied `passToken`
  Region                 `i2`

The passToken input is hidden while typing.

**India region:** Enter `i2`. This is the region value that successfully
connected and retrieved real watch data in our tested setup. It is not
an official Xiaomi compatibility guarantee.

The wizard should confirm that the configuration was saved.

### Step 3 -- Verify the configuration

``` bash
mi-fitness-bridge doctor
```

Expected indicators:

-   Configuration loaded
-   Mi Fitness credentials found
-   Region: `i2`
-   Connection status: connected
-   Recognised region: `i2`

The database may initially be reported as not yet created. It is created
when the first synchronisation runs.

## 6. Synchronise Mi Watch data

The bridge can retrieve several categories of health information,
depending on account, device and upstream availability.

  Dataset                 Information
  ----------------------- -------------------------------------
  `daily_activity`        Steps, distance, active calories
  `heart_rate`            Heart-rate samples
  `sleep`                 Sleep sessions and stages
  `workouts`              Exercise sessions
  `body_measurements`     Available body measurements
  `spo2`                  Blood oxygen readings
  `stress`                Stress measurements
  `abnormal_heart_beat`   Available abnormal heartbeat events

### Step 1 -- Synchronise a date range

``` bash
mi-fitness-bridge sync --start-date 2026-11-01 --end-date 2026-11-16
```

Replace the dates with the required period.

### Step 2 -- Synchronise an individual dataset

Sleep:

``` bash
mi-fitness-bridge sync --type sleep --start-date 2026-11-01 --end-date 2026-11-16
```

Heart rate:

``` bash
mi-fitness-bridge sync --type heart_rate --start-date 2026-11-01 --end-date 2026-11-16
```

### Step 3 -- Understand sync results

The bridge reports how many records were added and updated.

Example from the tested setup:

  Dataset               New records   Updated records
  ------------------- ------------- -----------------
  Daily activity                 16                 2
  Heart rate                  2,475                 0
  Sleep                           0                16
  Body measurements               0                 0
  Workouts                        0                 0
  SpO₂                            0                 0
  Stress                          0                 0

This confirmed successful retrieval of actual watch records.

> A successful sync with zero records is not necessarily an error. Some
> datasets may not be available for your watch, account or selected
> period.

## 7. Export data to JSON

After synchronisation:

``` bash
mi-fitness-bridge export
```

The tested setup generated:

``` text
exports/mi_fitness_export.json
```

Inspect the export:

``` bash
ls -lh exports/
```

Inspect the JSON structure:

``` bash
python -m json.tool exports/mi_fitness_export.json | head -80
```

Display dataset counts and field names without printing health readings:

``` bash
python - <<'PY'
import json

with open("exports/mi_fitness_export.json") as f:
    data = json.load(f)

print("Generated:", data["generated_at"])

for name, records in data["records"].items():
    print(f"\n{name}: {len(records)} records")
    if records:
        print("Fields:", ", ".join(records[0].keys()))
PY
```

The JSON export does not contain the saved passToken. However, it can
contain your Xiaomi user ID and sensitive personal health information.
Keep it private.

## 8. Install the HTML dashboard

The dashboard provides a visual interface for the exported JSON file.

### Step 1 -- Download and extract the dashboard package

Download `mi_watch_dashboard_mac.zip` and extract it into:

``` text
~/MiWatchData/
```

Expected directory structure:

``` text
MiWatchData/
├── mi-fitness-data-bridge/
│   ├── .venv/
│   ├── exports/
│   │   └── mi_fitness_export.json
│   └── ...
└── mi_watch_dashboard/
    ├── index.html
    ├── server.py
    └── README.txt
```

### Step 2 -- Start the dashboard server

``` bash
cd ~/MiWatchData/mi_watch_dashboard
python3 server.py
```

Expected output:

``` text
Dashboard: http://127.0.0.1:8765
Reading latest JSON from:
.../MiWatchData/mi-fitness-data-bridge/exports/mi_fitness_export.json
```

Keep this Terminal window open while using the dashboard.

### Step 3 -- Open the dashboard

Open Firefox or Chrome and navigate to:

**http://127.0.0.1:8765**

The dashboard loads the JSON export automatically.

### Step 4 -- Dashboard features

1.  **Overview:** average daily steps, sleep duration, heart rate and
    active calories.
2.  **Heart rate:** history, BPM readings, minimum and maximum readings.
3.  **Sleep analysis:** duration, history, awake/asleep duration and
    score where available.
4.  **Daily activity:** daily step count and activity trends.
5.  **Data availability:** number of records available for each dataset.
6.  **Data export:** date filters and CSV download for filtered data.

The dashboard refreshes the JSON automatically every 60 seconds while
open. You can also click **Refresh JSON**.

## 9. Routine procedure -- Daily or periodic update

### Step 1 -- Synchronise the required period

``` bash
cd ~/MiWatchData/mi-fitness-data-bridge
source .venv/bin/activate

mi-fitness-bridge sync --start-date 2026-11-01 --end-date 2026-11-16
```

Change the dates to cover the period you want to retrieve.

### Step 2 -- Export the latest data

``` bash
mi-fitness-bridge export
```

### Step 3 -- Refresh the dashboard

Return to **http://127.0.0.1:8765**. Click **Refresh JSON**, or wait for
the automatic refresh.

The dashboard reads the newly generated JSON file. You do not need to
restart the dashboard server.

## 10. Troubleshooting

  ----------------------------------------------------------------------------
  Problem                                  Suggested action
  ---------------------------------------- -----------------------------------
  `mi-fitness-bridge: command not found`   Enter the project directory and
                                           activate `.venv`

  Authentication failure                   Obtain a fresh Xiaomi session token
                                           and rerun `setup`

  Doctor reports the wrong region          Check that the configured region is
                                           `i2`

  Sync returns zero records                Check the date range and
                                           account/device data availability

  JSON export not found                    Run `mi-fitness-bridge export`

  Dashboard says data unavailable          Confirm the JSON file exists at the
                                           expected path

  Dashboard does not show new readings     Run sync and export again, then
                                           click Refresh JSON

  Port 8765 is already in use              Run `python3 server.py --port 8766`
                                           and open `http://127.0.0.1:8766`
  ----------------------------------------------------------------------------

**Important:** Do not delete the database to troubleshoot zero records.
The local SQLite database contains previously synchronised records.
Re-running sync for the same date range is designed not to duplicate
existing records. Keep your database intact unless you have a verified
backup and a specific reason to replace it.

## 11. Important file locations

  --------------------------------------------------------------------------------------------------
  File or directory                                              Purpose
  -------------------------------------------------------------- -----------------------------------
  `~/MiWatchData/mi-fitness-data-bridge/`                        Bridge source and installation

  `~/MiWatchData/mi-fitness-data-bridge/exports/`                JSON and CSV exports

  `~/Library/Application Support/mi-fitness-mcp/mi_fitness.db`   Local SQLite database

  `~/Library/Application Support/mi-fitness-mcp/config.json`     Bridge configuration

  `~/MiWatchData/mi_watch_dashboard/`                            HTML dashboard
  --------------------------------------------------------------------------------------------------

Back up the SQLite database and important exports securely. Keep
configuration and credential-related files private.

## 12. Security and privacy

This workflow handles sensitive personal health information.

-   Keep the Xiaomi passToken private.
-   Do not upload the database or exports to public repositories.
-   Do not commit health records to GitHub.
-   Do not expose the dashboard server to the public internet.
-   The dashboard server binds to `127.0.0.1`, making it accessible from
    the local Mac.
-   Store backups in a location protected by your normal Mac security
    controls.

The bridge is an unofficial data-access utility. The dashboard is for
personal data viewing and trend analysis, not medical diagnosis.

## 13. Complete command reference

### Initial installation

``` bash
mkdir -p ~/MiWatchData
cd ~/MiWatchData

git clone https://github.com/shkyyy18/mi_fitness_data_bridge.git mi-fitness-data-bridge

cd mi-fitness-data-bridge

python3 -m venv .venv
source .venv/bin/activate

pip install -e .
```

### Configure and verify

``` bash
mi-fitness-bridge setup
mi-fitness-bridge doctor
```

Enter the Xiaomi `user_id`, hidden `passToken` and region `i2` when
prompted.

### Synchronise and export

``` bash
mi-fitness-bridge sync --start-date 2026-11-01 --end-date 2026-11-16

mi-fitness-bridge export
```

### Start dashboard

``` bash
cd ~/MiWatchData/mi_watch_dashboard
python3 server.py
```

Open **http://127.0.0.1:8765**.

------------------------------------------------------------------------

**End of manual**
