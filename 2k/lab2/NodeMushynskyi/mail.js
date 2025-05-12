import nodemailer from 'nodemailer';

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: '3986185@stud.op.edu.ua',
    pass: 'gqgrxcyjziglyian'
  },
  tls: {
    rejectUnauthorized: false
  }
});

const mailOptions = {
  from: '3986185@stud.op.edu.ua',
  to: '3986185@stud.op.edu.ua',
  subject: 'Test from Node.js',
  text: 'Це тестовий лист з лабораторної роботи №2.'
};

transporter.sendMail(mailOptions, (error, info) => {
  if (error) {
    return console.error('Помилка надсилання:', error);
  }
  console.log('Лист успішно надіслано:', info.response);
});

