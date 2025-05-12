import fs from 'fs';

fs.readFile('test-folder/info.txt', 'utf-8', (err, data) => {
  if (err) throw err;
  console.log(data);
});
