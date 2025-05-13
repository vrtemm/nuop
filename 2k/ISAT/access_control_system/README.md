# Access Control System for Distributed Web Resources

## Features
- Signature-based threat detection
- Manual URL/IP blocking
- Traffic logging with timestamps and actions

## How to Run
1. Install Node.js
2. Navigate to project directory
3. Run:
```bash
node index.js
```
4. Use browser or curl to simulate requests:
```bash
curl http://localhost:8080/malicious
```

Logs are stored in `data/logs.json`
Blocking rules can be edited in `data/blocklist.json`