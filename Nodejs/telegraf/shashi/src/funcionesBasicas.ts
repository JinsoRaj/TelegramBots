import * as fs from 'fs';
import { Context } from 'vm';

export function loggerMeta(log: string) {
  let mensaje: string = '=========';
  const ahora = new Date();
  //dia, fecha, mes, año, hora, minutos, segundo
  const tiempo: string =
    dia(ahora.getDay()) +
    ' ' +
    ahora.getDate().toString() +
    ' ' +
    mes(ahora.getMonth()) +
    ' ' +
    ahora.getFullYear().toString() +
    ' ' +
    ahora.getHours().toString() +
    ' ' +
    ahora.getMinutes().toString() +
    ' ' +
    ahora.getSeconds().toString();
  mensaje = tiempo + '\n' + log + '\n' + mensaje + '\n';

  if (fs.existsSync('shashi.log')) {
    fs.appendFileSync('shashi.log', mensaje);
  } else {
    fs.writeFileSync('shashi.log', mensaje);
  }
}

export function logger(log: string) {
  if (fs.existsSync('shashi.log')) {
    log = log + '\n';
    fs.appendFileSync('shashi.log', log);
  } else {
    log = log + '\n';
    fs.writeFileSync('shashi.log', log);
  }
}

export function setIdUser(id: number) {
  if (fs.existsSync('users_shashi.txt')) {
    var iden = id.toString() + '\n';
    const file: string = fs.readFileSync('users_shashi.txt', 'utf-8');
    const fileSplit: String[] = file.split('\n');
    var existe: boolean = false;

    for (let i = 0; i < fileSplit.length; i++) {
      if (fileSplit[i] == id.toString()) {
        console.log('Existo');
        existe = true;
      }
    }

    if (existe == false) {
      fs.appendFileSync('users_shashi.txt', iden);
    }
  } else {
    var iden = id.toString() + '\n';
    fs.writeFileSync('users_shashi.txt', iden);
  }
}

export function checkIdUser(id: number): boolean {
  var existe: boolean = false;
  if (fs.existsSync('users_shashi.txt') == false) {
    existe = false;
  } else {
    const file: string = fs.readFileSync('users_shashi.txt', 'utf-8');
    const fileSplit: String[] = file.split('\n');
    for (let i = 0; i < fileSplit.length; i++) {
      const element = fileSplit[i];
      if (element == id.toString()) {
        existe = true;
      }
    }
  }
  return existe;
}

export function anotar(id: number, titulo: string, contenido: string) {
  const iden = id.toString() + '\n';
  const texto: string = iden + titulo + '\n' + contenido + '\n----\n';
  if (fs.existsSync('notas.txt')) {
    fs.appendFileSync('notas.txt', texto);
  } else {
    fs.writeFileSync('notas.txt', texto);
  }
}

export function obtenerNota(): {
  id: number;
  titulo: string;
  contenido: string;
}[] {
  if (fs.existsSync('notas.txt') == false) {
    return [
      {
        id: 0,
        titulo: '',
        contenido: '',
      },
    ];
  }
  const archivo: string = fs.readFileSync('notas.txt', 'utf-8');
  const notas: string[] = archivo.split('\n----\n');
  let notasArg = [];
  for (let i = 0; i < notas.length; i++) {
    const nota = notas[i];
    const estructura: string[] = nota.split('\n');
    const id: string = estructura[0];
    const titulo: string = estructura[1];
    let contenido: string = '';
    for (let i = 0; i < estructura.length; i++) {
      const element = estructura[i];
      if (i > 1) {
        contenido = contenido + element + '\n';
      }
    }
    notasArg.push({
      id: parseInt(id),
      titulo: titulo,
      contenido: contenido,
    });
  }
  return notasArg;
}

export function obtenerHora(): string {
  const ahora = new Date();
  let enunciado: string;
  const hora = ahora.getUTCHours() - 6;
  if (hora == 1 || hora == 13) {
    enunciado = 'Son la ';
  } else {
    enunciado = 'Son las ';
  }

  if (hora < 12) {
    enunciado = enunciado + hora.toString() + ' a.m. ';
  } else {
    let horaDoce = hora - 12;
    enunciado = enunciado + horaDoce + ' p.m. ';
  }

  enunciado =
    enunciado +
    'con ' +
    ahora.getMinutes() +
    ' y ' +
    ahora.getSeconds() +
    ' segundos';

  return enunciado;
}

export function obtenerFecha(): string {
  const ahora = new Date();
  let enunciado: string =
    'Hoy es ' +
    dia(ahora.getDay()) +
    ' ' +
    ahora.getDate() +
    ' de ' +
    mes(ahora.getMonth()) +
    ' del ' +
    ahora.getFullYear();

  return enunciado;
}

export function argumentosCmd(
  ctx: Context,
  numeroArgs?: number
): Array<string> {
  var mensaje: any = ctx.message.text;
  if (numeroArgs) {
    mensaje = mensaje.split(' ', numeroArgs + 1);
  } else {
    mensaje = mensaje.split(' ');
  }

  var argumentos: Array<string> = [];
  for (let index = 0; index < mensaje.length; index++) {
    if (index != 0) {
      argumentos.push(mensaje[index]);
    }
  }

  return argumentos;
}

export function numeroRandom(menor: number, mayor: number): number {
  let numero = Math.floor(Math.random() * (mayor + 1 - menor) + menor);
  return numero;
}

export function mensajeRandom(mensajes: Array<string>): string {
  let numero = numeroRandom(1, mensajes.length);
  return mensajes[numero - 1];
}

function dia(numero: number): string {
  switch (numero) {
    case 1:
      return 'dom';

    case 2:
      return 'lun';

    case 3:
      return 'mar';

    case 4:
      return 'mie';

    case 5:
      return 'jue';

    case 6:
      return 'vie';

    case 7:
      return 'sab';

    default:
      return 'lun';
  }
}

function mes(numero: number): string {
  switch (numero) {
    case 1:
      return 'ene';

    case 2:
      return 'feb';

    case 3:
      return 'mar';

    case 4:
      return 'abr';

    case 5:
      return 'may';

    case 6:
      return 'jun';

    case 7:
      return 'jul';

    case 8:
      return 'ago';

    case 9:
      return 'sep';

    case 10:
      return 'oct';

    case 11:
      return 'nov';

    case 12:
      return 'dic';

    default:
      return 'ene';
  }
}
