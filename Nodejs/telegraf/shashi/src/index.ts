import {
  annotate,
  argsCmd,
  checkIdUser,
  logger,
  loggerMeta,
  msgRandom,
  getDate,
  getTime,
  getNote,
  setIdUser,
} from './funcionesBasicas';
import {
  AskDate,
  AskTime,
  ConfusingMsg,
  GreetingMessage,
  TimeMsg,
  DateMsg,
} from './constantes';
import { Context } from 'vm';

const Telegraf: any = require('telegraf').Telegraf;
const weather: any = require('weather-js');
const Bot = new Telegraf(''); //Ingresa el token de Telegram

//Inicio del logger
Bot.use((ctx: Context, next: any) => {
  const start = Date.now();
  return next().then(() => {
    const ms = Date.now() - start;
    let clog: string =
      ctx.message.text +
      '\n' +
      'Mensaje enviado a: ' +
      ctx.from.first_name +
      '\n' +
      'Tiempo de respuesta: ' +
      ms +
      'ms';
    console.log(clog);
    loggerMeta(clog);
  });
});

Bot.start((ctx: Context) => {
  var argumentos = argsCmd(ctx, 1);
  if (argumentos[0] == 'ClaveParaIniciar') {
    var mensaje = msgRandom(GreetingMessage);
    ctx.reply(mensaje);
    logger(mensaje);
    setIdUser(ctx.from.id);
  } else {
    ctx.reply('Bienvenido ' + ctx.from.first_name);
    logger('Bienvenido ' + ctx.from.first_name);
  }
});

Bot.hears(AskTime, (ctx: Context) => {
  var random = msgRandom(TimeMsg);
  var mensaje = getTime();
  ctx.reply(mensaje);
  mensaje = mensaje + '\n' + random;
  ctx.reply(random);
  logger(mensaje);
});

Bot.command('hora', (ctx: Context) => {
  var random = msgRandom(TimeMsg);
  var mensaje = getTime();
  ctx.reply(mensaje);
  mensaje = mensaje + '\n' + random;
  ctx.reply(random);
  logger(mensaje);
});

Bot.command('fecha', (ctx: Context) => {
  var random = msgRandom(DateMsg);
  var mensaje = getDate();
  ctx.reply(mensaje);
  mensaje = mensaje + '\n' + random;
  ctx.reply(random);
  logger(mensaje);
});

Bot.hears(AskDate, (ctx: Context) => {
  var mensaje = getDate();
  ctx.reply(mensaje);
  logger(mensaje);
});

Bot.command('depurar', (ctx: Context) => {
  ctx.reply('Iniciando depuracion por parte del servidor');
  console.log('Alguien a pedido depurar...');
  logger('Iniciando depuracion por parte del servidor');
});

Bot.command('nota', (ctx: Context) => {
  let argumentos: string[] = argsCmd(ctx);
  let titulo = argumentos[0];
  let cuerpo: string = '';
  for (let i = 0; i < argumentos.length; i++) {
    const element = argumentos[i];
    if (i != 0) {
      cuerpo = cuerpo + element + ' ';
    }
  }
  if (checkIdUser(ctx.from.id)) {
    annotate(ctx.from.id, titulo, cuerpo);
    const respuesta: string = 'Tu nota fue agregada exitosamente ;D';
    ctx.reply(respuesta);
    logger(respuesta);
  } else {
    const respuesta: string =
      'Tu nota no fue guardada ya que no tienes permiso :(';
    ctx.reply(respuesta);
    logger(respuesta);
  }
});

Bot.command('ver', (ctx: Context) => {
  const notas = getNote();
  const argumentos: string[] = argsCmd(ctx, 1);
  for (let i = 0; i < notas.length; i++) {
    const element = notas[i];
    if (element.id == ctx.from.id && element.title == argumentos[0]) {
      ctx.reply(element.title + '\n' + element.contents);
      logger(element.title + '\n' + element.contents);
    }
  }
});

Bot.command('clima', (ctx: Context) => {
  if (checkIdUser(ctx.from.id) == true) {
    weather.find(
      { search: 'Mexico City', degreeType: 'C' },
      (err: any, result: any) => {
        if (err) console.log(err);
        const clima: any = result[0].current;
        let mensaje: string =
          'El dia de hoy estamos a ' +
          clima.temperature +
          'ºc con ' +
          clima.skytext +
          ', humedad del ' +
          clima.humidity +
          '% asi como vientos de hasta ' +
          clima.windspeed +
          ' en la Ciudad de Mexico';
        ctx.reply(mensaje);
        logger(mensaje);
      }
    );
  } else {
    ctx.reply('No tienes permisos de acceder a esta funcion :(');
    logger('No tienes permiso de acceder a esta funcion :(');
  }
});

Bot.on('text', (ctx: Context) => {
  let mensaje = msgRandom(ConfusingMsg);
  logger(mensaje);
  ctx.reply(mensaje);
});

//Iniciamos aqui
Bot.launch();
console.log('El bot esta en funcionamiento');
