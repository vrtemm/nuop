const http = require('http');
const fs = require('fs');
const url = require('url');
const { signatureMatch } = require('./modules/signatureCheck');
const { isBlocked, logEvent } = require('./modules/firewall');

const PORT = 8080;

const server = http.createServer((req, res) => {
  const clientIp = req.socket.remoteAddress;
  const parsedUrl = url.parse(req.url, true);
  const hostname = parsedUrl.hostname || req.headers.host;

  let threat = signatureMatch(req.url);

  if (isBlocked(hostname) || isBlocked(clientIp) || threat) {
    logEvent(clientIp, hostname, "blocked", threat || "manual block");
    res.writeHead(403, { 'Content-Type': 'text/plain' });
    res.end('Access denied');
  } else {
    logEvent(clientIp, hostname, "allowed", "none");
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('Access granted to ' + hostname);
  }
});

server.listen(PORT, () => {
  console.log(`Access Control Server running at http://localhost:${PORT}`);
});