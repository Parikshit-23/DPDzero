#   Agent Performance Analyzer

This is a command-line tool to analyze call center agent performance using CSV data from `agent_roster`, `call_logs`, and `disposition_summary`.  
It outputs a summary CSV and optionally prints a Slack-style daily performance summary.

---

##  Files Required

You will need the following CSV files:

1. `agent_roster.csv` – Agent metadata (ID, names, etc.)
2. `call_logs.csv` – Call details (call_id, duration, status, etc.)
3. `disposition_summary.csv` – Call disposition information

---

## How to run
```bash
python agent_performance.py --roster agent_roster.csv --logs call_logs.csv --summary disposition_summary.csv
```
