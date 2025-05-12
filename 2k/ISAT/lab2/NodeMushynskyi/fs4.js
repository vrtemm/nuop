import fs from 'fs/promises';

const data = await fs.readFile('test-folder/info.txt', 'utf-8');
console.log(data);
