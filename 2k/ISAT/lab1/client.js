const http = require('http');

// Define options for the HTTP request
const options = {
  hostname: '127.0.0.1',
  port: 3000,
  path: '/message',
  method: 'POST',
  headers: {
    'Content-Type': 'text/plain',
  },
};

// Send request to the server
const req = http.request(options, res => {
  console.log(`Statu: ${res.statusCode}`);

  // Receive response from server
  res.on('data', d => {
    process.stdout.write(`Answer from server: ${d}\n`);
  });
});

// Handle errors
req.on('error', error => {
  console.error(`Error: ${error}`);
});

// Send the message to the server
req.write('Test message');
req.end();
