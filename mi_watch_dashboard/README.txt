# Mi Watch Health Dashboard (Mac)

This is a local HTML + JavaScript dashboard. It uses Python's standard library only to serve the HTML and your JSON export locally. No pip installation is needed.

## Install
1. Unzip this folder anywhere, for example in `~/MiWatchData/`.
2. Open Terminal and run:

```bash
cd ~/MiWatchData/mi_watch_dashboard
python3 server.py
```

The default JSON path is:

`~/MiWatchData/mi-fitness-data-bridge/exports/mi_fitness_export.json`

If your export is elsewhere, run:

```bash
python3 server.py --data "/full/path/to/mi_fitness_export.json"
```

3. Open `http://127.0.0.1:8765` in your browser.
4. Keep the Terminal window running while using the dashboard.

## Updating data
After collecting new watch data, run in another Terminal window:

```bash
cd ~/MiWatchData/mi-fitness-data-bridge
mi-fitness-bridge sync
mi-fitness-bridge export
```

Return to the dashboard and click **Refresh JSON**, or wait up to 60 seconds. The dashboard reads the JSON file again; it does not need to be restarted.

## Notes
- The dashboard is bound to `127.0.0.1`, so it is accessible only from this Mac by default.
- It does not upload your health data to a website.
- Charts show only datasets present in your export. Empty SpO2, stress, workout and body-measurement datasets will show zero records.
- This is a personal data viewer, not a medical diagnostic tool.
