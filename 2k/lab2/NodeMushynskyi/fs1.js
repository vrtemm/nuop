import fs from 'fs';

fs.mkdir('test-folder', err => {
  if (err) throw err;
  console.log('Каталог створено');
});
