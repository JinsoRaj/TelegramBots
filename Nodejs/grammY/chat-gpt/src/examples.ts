const GRAMMAR = `Please correct this in Spanish:

Ella no comer papas.`;

const SUMMARY = `Summarize this for a second grader.:

Jupiter is the fifth planet from the Sun and the largest in the Solar System. Is
a gas giant with a mass one thousandth that of the Sun, but two
one and a half times that of all the other planets in the Solar System combined. Jupiter
It is one of the brightest objects visible to the naked eye in the sky
nocturnal, and ancient civilizations have known it since before history
registered. It is named after the Roman god Jupiter.[19] When seen from the
Earth, Jupiter may be bright enough that its light
reflection casts visible shadows, [20] and is, on average, the third largest object
brightest natural in the night sky after the Moon and Venus.`;

const QUESTION = `I am a very intelligent question answering bot.
If you ask me a question that is rooted in truth, I will give you the
answer. If you ask me a question that is stupid, deceitful, or not
has a clear answer, I will respond with "Unknown".

P: What is the human life expectancy in the United States?
R: The human life expectancy in the United States is 78 years.

P: Who was president of the United States in 1955?
R: Dwight D. Eisenhower was president of the United States in 1955.

P: What party did he belong to?
R: He belonged to the Republican Party.

P: What is the square root of banana?
R: Unknown

P: How does a telescope work?
R: Telescopes use lenses or mirrors to focus light and make objects appear closer.

P: Where were the 1992 Olympic Games held?
R: The 1992 Olympic Games were held in Barcelona, Spain.

P: How many squigs are in a bonk?
R: Unknown

P:`;

const TRANSLATE = `Translate this to 1. French, 2. Spanish and 3. Japanese:

What rooms do you have available?

1.`;

const PYTHON = `
"""
1. Create a list of names
2. Create a list of surnames
3. Combine them randomly into a list of 100 full names
"""
`;

const EXPLAIN = `class Log:
    def __init__(self, path):
        dirname = os.path.dirname(path)
        os.makedirs(dirname, exist_ok=True)
        f = open(path, "a+")

        # Check that the file is newline-terminated
        size = os.path.getsize(path)
        if size > 0:
            f.seek(size - 1)
            end = f.read(1)
            if end != "\n":
                f.write("\n")
        self.f = f
        self.path = path

    def log(self, event):
        event["_event_id"] = str(uuid.uuid4())
        json.dump(event, self.f)
        self.f.write("\n")

    def state(self):
        state = {"complete": set(), "last": None}
        for line in open(self.path):
            event = json.loads(line)
            if event["type"] == "submit" and event["success"]:
                state["complete"].add(event["id"])
                state["last"] = event
        return state

"""
Explica que esta haciendo la anterior clase:
1.`;

const ASSISTANT = `The following is a conversation with an AI assistant. The assistant is helpful, creative, intelligent and very friendly.

Human: Hello who are you?
AI: I am an AI created by someone. How can I help you today?
Human:`;

const HELP = `Your option is not correct, here is the list of the correct options:

- grammar
- summary
- question
- translation
- explain
- python
- assistant`;

export const EXAMPLES: Record<string, string> = {
  gramatica: GRAMMAR,
  resumen: SUMMARY,
  pregunta: QUESTION,
  traduccion: TRANSLATE,
  python: PYTHON,
  asistente: ASSISTANT,
  ayuda: HELP,
  explicar: EXPLAIN,
};
