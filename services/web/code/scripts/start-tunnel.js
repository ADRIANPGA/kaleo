// scripts/start-tunnel.js
const localtunnel = require('localtunnel');

(async () => {
  const tunnel = await localtunnel({ port: 13000, subdomain: 'kaleowebdemo' });

  console.log(`🌍 Public URL: ${tunnel.url}`);

  tunnel.on('close', () => {
    console.log('Tunnel closed');
  });

  tunnel.on('error', err => {
    console.error('Tunnel error:', err);
  });
})();
