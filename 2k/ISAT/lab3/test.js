const { Block, Blockchain } = require('./blockchain');

const myChain = new Blockchain();

console.log("Додаємо блоки...");
myChain.addBlock(new Block(1, new Date().toISOString(), { amount: 100 }));
myChain.addBlock(new Block(2, new Date().toISOString(), { amount: 50 }));

console.log("Блокчейн:");
console.log(JSON.stringify(myChain, null, 2));

console.log("Перевірка цілісності:", myChain.isChainValid() ? "Ланцюг дійсний" : "Ланцюг порушено");

// Псування даних (перевірка)
myChain.blockchain[1].data = { amount: 999 };
console.log(" Після зміни блоку:", myChain.isChainValid() ? "Ланцюг дійсний" : "Ланцюг порушено");
