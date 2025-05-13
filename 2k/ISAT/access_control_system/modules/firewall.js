const fs = require('fs');
const path = require('path');

const blocklistPath = path.join(__dirname, '../data/blocklist.json');
const logPath = path.join(__dirname, '../data/logs.json');

function loadBlocklist() {
  try {
    const data = fs.readFileSync(blocklistPath);
    return JSON.parse(data);
  } catch {
    return { blocked_urls: [], blocked_ips: [] };
  }
}

function isBlocked(target) {
  const list = loadBlocklist();
  return list.blocked_urls.includes(target) || list.blocked_ips.includes(target);
}

function logEvent(ip, url, action, threat) {
  const entry = {
    timestamp: new Date().toISOString(),
    ip,
    url,
    action,
    threat
  };

  let logs = [];
  if (fs.existsSync(logPath)) {
    logs = JSON.parse(fs.readFileSync(logPath));
  }
  logs.push(entry);
  fs.writeFileSync(logPath, JSON.stringify(logs, null, 2));
}

module.exports = { isBlocked, logEvent };