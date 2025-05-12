import EventEmitter from 'events';

const emitter = new EventEmitter();

emitter.on('start', () => {
  console.log('Процес запущено...');
  setTimeout(() => {
    console.log('Минуло 3 секунди');
  }, 3000);
});

emitter.emit('start');
