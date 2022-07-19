import re

SEP = '@#*'

def read_paragraphs(it):
    doc = []
    for line in it:
        line = line.strip()
        line = re.sub(r'\s+', ' ', line)
        if not line and doc:
            yield "\n".join(doc)
            doc.clear()
        else:
            if line:
                doc.append(line)
    if doc:
        yield "\n".join(doc)

def annotate_and_print(it_par, nlp):
    for par in nlp.pipe(it_par, batch_size=5):
        print(par)
        print('\n')
        for token in par:
            if token.text == '\n':
                print()
            else:
                new_string = token.text + ' [' + token.lemma_ + '] ' + token.pos_
                if token._.offset:
                    # new_string += token._.offset
                    new_string += " ==>" + token._.synset.definition() + f" {token._.synset.lemma_names()}"
                print(new_string, end=' ')
                print()
        print()
        print()


def test_run():
    # -d cuda - c / home / danmincu / ewiser / res / downloaded / ewiser.semcor + wngt.pt / home / danmincu / ewiser / test.txt
    from argparse import ArgumentParser
    import fileinput

    from ewiser.spacy.disambiguate import Disambiguator
    from spacy import load

    checkpoint = "/home/danmincu/ewiser/res/downloaded/ewiser.semcor+wngt.pt"
    device = 'cuda'
    spacy = 'en_core_web_sm'
    language = 'en'
    input = '/home/danmincu/ewiser/test.txt'
    wsd = Disambiguator(checkpoint, lang=language, batch_size=5, save_wsd_details=False).eval()
    wsd = wsd.to(device)
    nlp = load(spacy, disable=['ner', 'parser'])
    wsd.enable(nlp, 'wsd')

    if input == '-':
        lines = fileinput.input(['-'])
        pars = read_paragraphs(lines)
        annotate_and_print(pars, nlp)
    else:
        with open(input) as lines:
            pars = read_paragraphs(lines)
            annotate_and_print(pars, nlp)

if __name__ == '__main__':

    from argparse import ArgumentParser
    import fileinput

    from ewiser.spacy.disambiguate import Disambiguator
    from spacy import load

    parser = ArgumentParser(description='Script to annotate raw text.')
    parser.add_argument(
        'input', type=str,
        help='Input lines. Raw text file or stdin (if arg == "-").')
    parser.add_argument(
        '-c', '--checkpoint', type=str,
        help='Trained EWISER checkpoint.')
    parser.add_argument(
        '-d', '--device', default='cpu',
        help='Device to use. (cpu, cuda, cuda:0 etc.)')
    parser.add_argument(
        '-l', '--language', default='en')
    parser.add_argument(
        '-s', '--spacy', default='en_core_web_sm')
    args = parser.parse_args()

    wsd = Disambiguator(args.checkpoint, lang=args.language, batch_size=5, save_wsd_details=False).eval()
    wsd = wsd.to(args.device)
    nlp = load(args.spacy, disable=['ner', 'parser'])
    wsd.enable(nlp, 'wsd')

    if args.input == '-':
        lines = fileinput.input(['-'])
        pars = read_paragraphs(lines)
        annotate_and_print(pars, nlp)
    else:
        with open(args.input) as lines:
            pars = read_paragraphs(lines)
            annotate_and_print(pars, nlp)
