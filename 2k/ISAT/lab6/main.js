const fs = require('fs');
const readline = require('readline');
const crypto = require('crypto');
const { Blockchain } = require('./blockchain');

const chainFile = 'blockchain.json';
const keysFile = 'private_keys.json';

let blockchain = fs.existsSync(chainFile)
  ? new Blockchain(JSON.parse(fs.readFileSync(chainFile)))
  : new Blockchain();

function saveBlockchain() {
  fs.writeFileSync(chainFile, JSON.stringify(blockchain, null, 2));
}

function loadPrivateKeys() {
  return fs.existsSync(keysFile)
    ? JSON.parse(fs.readFileSync(keysFile))
    : {};
}

function savePrivateKeys(keys) {
  fs.writeFileSync(keysFile, JSON.stringify(keys, null, 2));
}

function generateKeyPair() {
  const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 512 });
  return {
    public: publicKey.export({ type: 'pkcs1', format: 'pem' }),
    private: privateKey.export({ type: 'pkcs1', format: 'pem' })
  };
}

function menu() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  let keys = loadPrivateKeys();
  let currentUser = null;

  function showMenu() {
    console.log('\n1. Register');
    console.log('2. Login');
    console.log('3. Add Transaction');
    console.log('4. View Blockchain');
    console.log('5. Exit');
    rl.question('Choose option: ', choice => {
      switch (choice.trim()) {
        case '1':
          const { public, private } = generateKeyPair();
          keys[public] = private;
          savePrivateKeys(keys);
          console.log('Public Key (Login):', public);
          console.log('Private Key (Password):', private);
          showMenu();
          break;
        case '2':
          rl.question('Enter public key: ', pub => {
            rl.question('Enter private key: ', priv => {
              if (keys[pub.trim()] === priv.trim()) {
                currentUser = pub.trim();
                console.log('Login success.');
              } else {
                console.log('Invalid keys.');
              }
              showMenu();
            });
          });
          break;
        case '3':
          if (!currentUser) {
            console.log('Login required!');
            return showMenu();
          }
          rl.question('Enter transaction data: ', data => {
            blockchain.addBlock({ user: currentUser, data });
            saveBlockchain();
            console.log('Transaction added.');
            showMenu();
          });
          break;
        case '4':
          console.log(JSON.stringify(blockchain.chain, null, 2));
          showMenu();
          break;
        case '5':
          rl.close();
          break;
        default:
          showMenu();
      }
    });
  }

  showMenu();
}

menu();