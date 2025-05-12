import fs from 'fs';

fs.writeFile('test-folder/info.txt', 'Привіт, НУВГП!', err => {
  if (err) throw err;
  console.log('Файл створено');
});
