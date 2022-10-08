import fs from 'fs';
import { Context } from 'vm';

export function loggerMeta(log: string) {
  let msg: string = '=========';
  const now = new Date();
  //dia, fecha, mes, año, hora, minutos, segundo
  const time: string =
    day(now.getDay()) +
    ' ' +
    now.getDate().toString() +
    ' ' +
    month(now.getMonth()) +
    ' ' +
    now.getFullYear().toString() +
    ' ' +
    now.getHours().toString() +
    ' ' +
    now.getMinutes().toString() +
    ' ' +
    now.getSeconds().toString();
  msg = time + '\n' + log + '\n' + msg + '\n';

  if (fs.existsSync('shashi.log')) {
    fs.appendFileSync('shashi.log', msg);
  } else {
    fs.writeFileSync('shashi.log', msg);
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
    var exists: boolean = false;

    for (let i = 0; i < fileSplit.length; i++) {
      if (fileSplit[i] == id.toString()) {
        console.log('i_exist');
        exists = true;
      }
    }

    if (exists == false) {
      fs.appendFileSync('users_shashi.txt', iden);
    }
  } else {
    var iden = id.toString() + '\n';
    fs.writeFileSync('users_shashi.txt', iden);
  }
}

export function checkIdUser(id: number): boolean {
  var exists: boolean = false;
  if (fs.existsSync('users_shashi.txt') == false) {
    exists = false;
  } else {
    const file: string = fs.readFileSync('users_shashi.txt', 'utf-8');
    const fileSplit: String[] = file.split('\n');
    for (let i = 0; i < fileSplit.length; i++) {
      const element = fileSplit[i];
      if (element == id.toString()) {
        exists = true;
      }
    }
  }
  return exists;
}

export function annotate(id: number, title: string, contents: string) {
  const iden = id.toString() + '\n';
  const text: string = iden + title + '\n' + contents + '\n----\n';
  if (fs.existsSync('notes.txt')) {
    fs.appendFileSync('notes.txt', text);
  } else {
    fs.writeFileSync('notes.txt', text);
  }
}

export function getNote(): {
  id: number;
  title: string;
  contents: string;
}[] {
  if (fs.existsSync('notas.txt') == false) {
    return [
      {
        id: 0,
        title: '',
        contents: '',
      },
    ];
  }
  const file: string = fs.readFileSync('notas.txt', 'utf-8');
  const notes: string[] = file.split('\n----\n');
  let notesArg = [];
  for (let i = 0; i < notes.length; i++) {
    const note = notes[i];
    const struct: string[] = note.split('\n');
    const id: string = struct[0];
    const title: string = struct[1];
    let contents: string = '';
    for (let i = 0; i < struct.length; i++) {
      const element = struct[i];
      if (i > 1) {
        contents = contents + element + '\n';
      }
    }
    notesArg.push({
      id: parseInt(id),
      title: title,
      contents: contents,
    });
  }
  return notesArg;
}

export function getTime(): string {
  const now = new Date();
  let statement: string;
  const time = now.getUTCHours() - 6;
  if (time == 1 || time == 13) {
    statement = 'Son la ';
  } else {
    statement = 'Son las ';
  }

  if (time < 12) {
    statement = statement + time.toString() + ' a.m. ';
  } else {
    let horaDoce = time - 12;
    statement = statement + horaDoce + ' p.m. ';
  }

  statement =
    statement +
    'with ' +
    now.getMinutes() +
    ' and ' +
    now.getSeconds() +
    ' seconds';

  return statement;
}

export function getDate(): string {
  const now = new Date();
  let statement: string =
    'Hoy es ' +
    day(now.getDay()) +
    ' ' +
    now.getDate() +
    ' de ' +
    month(now.getMonth()) +
    ' del ' +
    now.getFullYear();

  return statement;
}

export function argsCmd(
  ctx: Context,
  numArgs?: number
): Array<string> {
  var msg: any = ctx.message.text;
  if (numArgs) {
    msg = msg.split(' ', numArgs + 1);
  } else {
    msg = msg.split(' ');
  }

  var args: Array<string> = [];
  for (let index = 0; index < msg.length; index++) {
    if (index != 0) {
      args.push(msg[index]);
    }
  }

  return args;
}

export function numberRandom(minor: number, elderly: number): number {
  let number = Math.floor(Math.random() * (elderly + 1 - minor) + minor);
  return number;
}

export function msgRandom(msgs: Array<string>): string {
  let number = numberRandom(1, msgs.length);
  return msgs[number - 1];
}

function day(number: number): string {
  switch (number) {
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

function month(number: number): string {
  switch (number) {
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
