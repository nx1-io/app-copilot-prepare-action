# app-copilot-prepare-action

### local run (from mock)
```
OUTPUT_PATH=./output/ NX1_TEST_FILE=./mock-alpha-03.json python3 App/main.py
```

### local run (from endpoint)
```
OUTPUT_PATH=output/ NX1_API_TOKEN=<<token>> NX1_APP_ID=<<app_id>> NX1_ENV_ID=<<env_uuid>> NX1_API_URL=http://localhost:8080/api python3 App/main.py
```

