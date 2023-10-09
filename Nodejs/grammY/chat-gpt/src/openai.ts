import * as dotenv from 'dotenv';
dotenv.config();
import { Configuration, OpenAIApi } from 'openai';
import { BotConfig } from './db';

export class Request {
  instance: OpenAIApi;
  constructor(token?: string) {
    if (token) {
      const configuration = new Configuration({
        apiKey: token,
      });
      this.instance = new OpenAIApi(configuration);
    } else {
      const configuration = new Configuration({
        apiKey: process.env.OPENAI_TOKEN,
      });
      this.instance = new OpenAIApi(configuration);
    }
  }

  async complete(input: string, config: BotConfig) {
    const c = TIPOS[config.type];
    let results: string | undefined = undefined;
    if (c.model != 'gpt-3.5-turbo') {
      const complete = await this.instance.createCompletion({
        model: c.model,
        prompt: `${input}`,
        max_tokens: c.max_value,
        temperature: c.temperature,
        top_p: 1,
        n: 1,
        stream: false,
        logprobs: null,
        stop: '',
      });
      results = complete.data.choices[0].text;
    } else {
      const { data } = await this.instance.createChatCompletion({
        model: 'gpt-3.5-turbo',
        messages: [{ role: 'user', content: `${input}` }],
        temperature: 0,
        top_p: 0.1,
        max_tokens: c.max_value,
      });
      results = data.choices[0].message?.content;
    }
    if (!results) {
      results = "I can't answer this, sorry and try something else :c";
    }
    return results;
  }
}

interface Model {
  model: string;
  temperature: number;
  max_value: number;
}

export const TIPOS: Record<string, Model> = {
  downdown: {
    model: 'text-ada-001',
    temperature: 0,
    max_value: 100,
  },
  down: {
    model: 'text-curie-001',
    temperature: 0.1,
    max_value: 120,
  },
  medium: {
    model: 'text-curie-001',
    temperature: 0.75,
    max_value: 400,
  },
  high: {
    model: 'text-davinci-003',
    temperature: 0.78,
    max_value: 356,
  },
  highhigh: {
    model: 'gpt-3.5-turbo',
    temperature: 0,
    max_value: 200,
  },
};
