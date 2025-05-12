import os from 'os';

console.log('ОС:', os.platform());
console.log('Архітектура:', os.arch());
console.log('Користувач:', os.userInfo().username);
