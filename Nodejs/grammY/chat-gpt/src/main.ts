import { Bot } from 'grammy';
import * as dotenv from 'dotenv';
dotenv.config();
import { BotConfig, BotAnswer, Users } from './db';
import { Request } from './openai';
import { EXAMPLES } from './examples';

// Configuracion de los tokens
let botToken = process.env.BOT_TOKEN;
if (!botToken) {
  botToken = '';
}
const bot = new Bot(botToken);
const db = new Users();
const now = new Date();
let memorize = false;
let context =
  'The following is a conversation with an AI assistant. The assistant is helpful, creative, intelligent and very friendly.\nHuman: ';

bot.command('start', (ctx) => {
  ctx.reply('Hello!');
  let name = ctx.from?.first_name;
  if (!name) {
    name = '';
  }
  const bot_configuration: BotConfig = {
    id: ctx.chat.id,
    name: name,
    type: 'medium',
  };
  db.add_conf(bot_configuration);
});

bot.command('config', async (ctx) => {
  let newConfig = ctx.message?.text.split(' ')[1];
  let config = await db.obtener_conf(ctx.chat.id);
  let name = ctx.from?.first_name;
  if (!newConfig) {
    newConfig = 'medium';
  }
  if (!name) {
    name = '';
  }
  config = {
    id: ctx.chat.id,
    name: name,
    type: newConfig,
  };
  db.add_conf(config);
  ctx.reply('Putting it in: ' + newConfig);
});

bot.command('example', (ctx) => {
  let name = ctx.message?.text.split(' ')[1];
  if (!name || name === '') {
    name = 'help';
  }
  ctx.reply(EXAMPLES[name.toLowerCase()]);
});

bot.command('memorize', (ctx) => {
  let cmd = ctx.message?.text.split(' ')[1];
  if (!cmd || cmd === '' || cmd != 'active') {
    memorize = false;
    context =
      'The following is a conversation with an AI assistant. The assistant is helpful, creative, intelligent and very friendly.\nHuman: ';
  } else {
    memorize = true;
  }
  ctx.reply(
    memorize ? 'Memorization is activated' : 'Memorization was disabled',
  );
});

bot.on('message:text', async (ctx) => {
  if (memorize) {
    context += ctx.update.message.text + '\nAI: ';
  }
  const hora: string =
    now.getDay() +
    '/' +
    now.getDate().toString() +
    '/' +
    now.getMonth() +
    '/' +
    now.getFullYear().toString() +
    ':' +
    now.getHours().toString() +
    ':' +
    now.getMinutes().toString() +
    ':' +
    now.getSeconds().toString();

  const author = ctx.update.message.from;
  const request = new Request();
  const config = await db.obtener_conf(author.id);
  let response = '';
  if (memorize) {
    response = await request.complete(context, config);
  } else {
    response = await request.complete(ctx.update.message.text, config);
  }
  const answer: BotAnswer = {
    id: author.id,
    name: author.first_name,
    hour: hora,
    answer: response,
    input: ctx.update.message.text,
  };
  ctx.reply(response);
  db.add_response(answer);
  if (memorize) {
    context += response + '\nHuman: ';
  }
});

console.log('The bot will start running 😸');
bot.start();
