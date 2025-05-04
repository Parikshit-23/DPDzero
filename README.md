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
Run this in CMD
```bash
python agent_performance.py --roster agent_roster.csv --logs call_logs.csv --summary disposition_summary.csv
```
---

## Output Columns in Summary
The script generates a CSV with:

1. `agent_id`
2. `users_first_name`
3. `users_last_name`
4. `call_date`
5. `total_calls`
6. `unique_loans_contacted`
7. `completed_calls`
8. `avg_call_duration_min`
9. `presence`
10. `Connect_Rate`

---

## Slack-style Summary
For the hardcoded date 2025-04-28, the script prints:
```yaml
Agent Summary for 2025-04-28
Top Performer: John Doe (85.0% connect rate)
Total Active Agents: 12
Average Duration: 4.57 min
```
---

## Logging
All info and error logs are written to:

```lua
agent_analysis.log
```
Logging Format
```vbnet
2025-05-04 16:24:22,100 - INFO - Files loaded successfully.
2025-05-04 16:24:22,103 - ERROR - Error merging data: 'call_id'
```

---

## Directory Structure

```lua
.
├── agent_performance.py
├── agent_roster.csv
├── call_logs.csv
├── disposition_summary.csv
├── agent_performance_summary.csv
├── agent_analysis.log
└── README.md
```
---
