const http = require('http');

const hostname = '127.0.0.1';
const port = 3000;

// Create HTTP server
const server = http.createServer((req, res) => {
  // Handle POST request to /message
  if (req.method === 'POST' && req.url === '/message') {
    let body = '';

    // Receive data from request body
    req.on('data', chunk => {
      body += chunk.toString();
    });

    // When all data is received
    req.on('end', () => {
      console.log(`Message get: ${body}`);
      res.statusCode = 200;
      res.setHeader('Content-Type', 'text/plain');
      // Send back the message transformed to uppercase
      res.end(`Message changed: ${body.toUpperCase()}`);
    });
  } else {
    // Handle other routes
    res.statusCode = 404;
    res.end('Not Found');
  }
});

// Start the server
server.listen(port, hostname, () => {
  console.log(`Server run on http://${hostname}:${port}/`);
});
