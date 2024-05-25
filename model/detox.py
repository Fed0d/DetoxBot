from ufal.udpipe import Model, Pipeline

from config import MODEL


def detox(message: str, words: set[str]) -> str:
    model = Model.load(MODEL)

    pipeline = Pipeline(model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')

    processed = pipeline.process(message)

    sentences = processed.split('\n\n')
    for sentence in sentences:
        lines = sentence.split('\n')
        for line in lines:
            columns = line.split('\t')
            if len(columns) > 2:
                if columns[2].lower() in words or columns[1].lower() in words:
                    masked_word = columns[1][0] + '*' * (len(columns[1]) - 1)
                    message = message.replace(columns[1], masked_word)

    return message
