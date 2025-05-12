const crypto = require('crypto');

class Block {
  constructor(index, timestamp, data, precedingHash = '', difficulty = 3) {
    this.index = index;
    this.timestamp = timestamp;
    this.data = data;
    this.precedingHash = precedingHash;
    this.nonce = 0;
    this.hash = this.computeHash();
    this.difficulty = difficulty;
  }

  computeHash() {
    return crypto.createHash('sha256')
      .update(this.index + this.timestamp + JSON.stringify(this.data) + this.precedingHash + this.nonce)
      .digest('hex');
  }

  proofOfWork() {
    while (!this.hash.startsWith('0'.repeat(this.difficulty))) {
      this.nonce++;
      this.hash = this.computeHash();
    }
  }
}

class Blockchain {
  constructor() {
    this.chain = [this.createGenesisBlock()];
    this.difficulty = 3;
  }

  createGenesisBlock() {
    const genesis = new Block(0, new Date().toISOString(), "Genesis Block", "0");
    genesis.proofOfWork();
    return genesis;
  }

  getLatestBlock() {
    return this.chain[this.chain.length - 1];
  }

  addBlock(data) {
    const newBlock = new Block(
      this.chain.length,
      new Date().toISOString(),
      data,
      this.getLatestBlock().hash,
      this.difficulty
    );
    newBlock.proofOfWork();
    this.chain.push(newBlock);
    return newBlock;
  }

  isChainValid() {
    for (let i = 1; i < this.chain.length; i++) {
      const current = this.chain[i];
      const previous = this.chain[i - 1];

      if (current.hash !== current.computeHash()) return false;
      if (current.precedingHash !== previous.hash) return false;
    }
    return true;
  }
}

module.exports = { Blockchain };