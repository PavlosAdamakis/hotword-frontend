import random
from nltk.corpus import wordnet

def get_dynamic_hints(word, hint_index):
    """
    Returns up to 3 progressively revealing hints for a given word:
      0) definition + part of speech,
      1) synonym or antonym,
      2) example sentence (with the word blanked) or letter‐set fallback.
    """
    synsets = wordnet.synsets(word)
    hints = []

    # 0) Definition + POS
    if synsets:
        primary = synsets[0]
        pos = primary.pos()
        definition = primary.definition().capitalize()
        hints.append(f"💡 [{pos}] {definition}")
    else:
        hints.append(f"💡 It's a {len(word)}-letter word")

    # 1) Antonym or synonym
    if synsets:
        lemmas = primary.lemmas()
        # try antonyms first
        antonyms = [l.antonyms()[0].name() for l in lemmas if l.antonyms()]
        if antonyms:
            hints.append(f"💡 Opposite of “{antonyms[0]}”")
        else:
            synonyms = [l.name() for l in lemmas if l.name().lower() != word]
            if synonyms:
                hints.append(f"💡 Synonym: “{synonyms[0]}”")
    if len(hints) < 2:
        # fallback if no synsets or no synonyms/antonyms
        hints.append(f"💡 It starts with “{word[0].upper()}”")

    # 2) Example sentence or letter‐set
    if synsets and primary.examples():
        example = primary.examples()[0]
        # mask the word in the example
        masked = example.replace(word, '_' * len(word))
        hints.append(f"🔤 “{masked}”")
    else:
        letters = ', '.join(sorted(set(word)))
        hints.append(f"💡 Letters: {letters}")

    # return the requested hint (clamped to available indices)
    return hints[min(hint_index, len(hints) - 1)]
