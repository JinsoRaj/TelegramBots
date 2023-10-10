import { Database } from 'sqlite3';
import { ensureFile } from 'fs-extra';
import { existsSync } from 'fs';

export interface BotConfig {
  id: number;
  name: string;
  type: string;
}

export interface BotAnswer {
  id: number;
  name: string;
  hour: string;
  answer: string;
  input: string;
}

export function get_conn(file: string) {
  return new Database(file);
}

function query(q: string, db: Database) {
  db.exec(q);
}

export class Users {
  db: Database;
  constructor(db_path?: string, configuration?: BotConfig, input?: BotAnswer) {
    const config = `
     CREATE TABLE config (
     id INTEGER PRIMARY KEY,
     name TEXT NOT NULL,
     type TEXT NOT NULL
    );`;
    const answers = `
     CREATE TABLE answer (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     id_chat INTEGER,
     name TEXT NOT NULL,
     hour TEXT NOT NULL,
     answer TEXT NOT NULL,
     input TEXT NOT NULL
    );`;

    if (!db_path) {
      db_path = 'users.db';
    }

    if (existsSync(db_path)) {
      const db = new Database(db_path);
      this.db = db;
      return this;
    }
    ensureFile(db_path);
    const db = new Database(db_path);
    this.db = db;
    query(config, db);
    query(answers, db);

    if (configuration) {
      this.add_conf(configuration);
    }
    if (input) {
      this.add_response(input);
    }

    return this;
  }

  add_conf(c: BotConfig) {
    this.db.get('SELECT * FROM config WHERE id = ?', c.id, (_, row) => {
      let sql_query: string;
      if (row) {
        sql_query = `
     UPDATE config
     SET type = '${c.type}'
     WHERE id = ${c.id}
   `;
      } else {
        sql_query = `
     INSERT INTO config (id, name, type)
     VALUES ('${c.id}', '${c.name}', '${c.type}')
   `;
      }
      query(sql_query, this.db);
    });
  }

  add_response(r: BotAnswer) {
    const sql_query = `
      INSERT INTO respuestas (id_chat, name, hour, answer, input)
      VALUES ('${r.id}', '${r.name}', '${r.hour}', '${r.answer}', '${r.input}')
    `;
    query(sql_query, this.db);
  }

  obtener_conf(id: number): Promise<BotConfig> {
    return new Promise((resolve, reject) => {
      this.db.serialize(() => {
        this.db.get('SELECT * FROM config WHERE id = ?', id, (err, row) => {
          if (err) reject(err);
          const sql_query: BotConfig = {
            id: row.id,
            name: row.nombre,
            type: row.tipo,
          };
          resolve(sql_query);
        });
      });
    });
  }
}
