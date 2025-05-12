const crypto = require('crypto');

class Block {
  constructor(index, timestamp, data, precedingHash = '') {
    this.index = index;
    this.timestamp = timestamp;
    this.data = data;
    this.precedingHash = precedingHash;
    this.nonce = 0;
    this.hash = this.calculateHash();
  }

  calculateHash() {
    return crypto
      .createHash('sha256')
      .update(this.index + this.timestamp + JSON.stringify(this.data) + this.precedingHash + this.nonce)
      .digest('hex');
  }

  proofOfWork(difficulty) {
    while (this.hash.substring(0, difficulty) !== Array(difficulty + 1).join("0")) {
      this.nonce++;
      this.hash = this.calculateHash();
    }
  }
}

class Blockchain {
  constructor() {
    this.blockchain = [this.createGenesisBlock()];
    this.difficulty = 3;
  }

  createGenesisBlock() {
    return new Block(0, new Date().toISOString(), "Genesis Block", "0");
  }

  getLatestBlock() {
    return this.blockchain[this.blockchain.length - 1];
  }

  addBlock(newBlock) {
    newBlock.precedingHash = this.getLatestBlock().hash;
    newBlock.proofOfWork(this.difficulty);
    this.blockchain.push(newBlock);
  }

  isChainValid() {
    for (let i = 1; i < this.blockchain.length; i++) {
      const current = this.blockchain[i];
      const previous = this.blockchain[i - 1];

      if (current.hash !== current.calculateHash()) {
        return false;
      }

      if (current.precedingHash !== previous.hash) {
        return false;
      }
    }
    return true;
  }
}

module.exports = { Block, Blockchain };
