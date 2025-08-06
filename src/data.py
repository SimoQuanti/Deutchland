"""
Questo modulo contiene i dati lessicali e grammaticali utilizzati nel videogioco
Deutschland.  Ogni voce del vocabolario include il livello in cui viene
introdotta, il singolare, il plurale, l’articolo determinativo, la
traduzione italiana e una breve spiegazione.  Le regole grammaticali sono
organizzate in temi con spiegazioni e domande.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class VocabularyItem:
    """Rappresenta un singolo vocabolo tedesco con articolo e plurale."""
    level: int
    singular: str
    article: str
    plural: str
    translation: str
    explanation: str


@dataclass
class GrammarQuestion:
    """Domanda relativa a un argomento grammaticale."""
    prompt: str
    options: List[str]
    answer: str
    explanation: str


@dataclass
class GrammarTopic:
    """Argomento grammaticale con spiegazione generale e domande."""
    level: int
    name: str
    explanation: str
    questions: List[GrammarQuestion]


# Elenco dei vocaboli introdotti nei livelli del gioco
VOCABULARY: List[VocabularyItem] = [
    VocabularyItem(
        level=1,
        singular="Gabelstapler",
        article="der",
        plural="Gabelstapler",
        translation="carrello elevatore / muletto",
        explanation=(
            "Il sostantivo Gabelstapler significa ‘carrello elevatore’. È di genere "
            "maschile (article der) e il suo plurale è identico al singolare: "
            "die Gabelstapler【59630982256329†L128-L184】."
        ),
    ),
    VocabularyItem(
        level=1,
        singular="Lager",
        article="das",
        plural="Lager",
        translation="magazzino",
        explanation=(
            "Lager significa ‘magazzino’ o ‘deposito’. È un sostantivo neutro (das) e "
            "al plurale rimane invariato: die Lager o con umlaut die Läger【79702443002764†L129-L184】."
        ),
    ),
    VocabularyItem(
        level=1,
        singular="Palette",
        article="die",
        plural="Paletten",
        translation="pallet / bancale",
        explanation=(
            "Palette è un sostantivo femminile che significa ‘pallet’ o ‘bancale’. "
            "Il plurale si forma aggiungendo -n: die Paletten【18485698920483†L128-L186】."
        ),
    ),
    VocabularyItem(
        level=1,
        singular="Lagerarbeiter",
        article="der",
        plural="Lagerarbeiter",
        translation="magazziniere",
        explanation=(
            "Lagerarbeiter indica l’‘operatore di magazzino’. È di genere maschile e "
            "al plurale rimane invariato: die Lagerarbeiter【144059179125449†L128-L180】."
        ),
    ),
    VocabularyItem(
        level=1,
        singular="Regal",
        article="das",
        plural="Regale",
        translation="scaffale",
        explanation=(
            "Regal significa ‘scaffale’. È neutro (das) e al plurale diventa die "
            "Regale【933059004205608†L18-L23】."
        ),
    ),
    # Livello 2 – nuovi vocaboli
    VocabularyItem(
        level=2,
        singular="Kiste",
        article="die",
        plural="Kisten",
        translation="cassetta / scatola",
        explanation=(
            "Kiste è una ‘cassetta’ o ‘scatola’. È femminile (die) e al plurale prende -n: "
            "die Kisten【912261064037591†L14-L22】."
        ),
    ),
    VocabularyItem(
        level=2,
        singular="Paket",
        article="das",
        plural="Pakete",
        translation="pacco",
        explanation=(
            "Paket significa ‘pacco’. È neutro (das) e al plurale diventa die Pakete"
            "【724579430065651†L18-L22】."
        ),
    ),
    VocabularyItem(
        level=2,
        singular="Waage",
        article="die",
        plural="Waagen",
        translation="bilancia",
        explanation=(
            "Waage significa ‘bilancia’ o ‘bilance’. È un sostantivo femminile; al plurale "
            "si aggiunge -n: die Waagen【8612395697889†L127-L134】."
        ),
    ),
    VocabularyItem(
        level=2,
        singular="Verpackung",
        article="die",
        plural="Verpackungen",
        translation="imballaggio",
        explanation=(
            "Verpackung è il termine per ‘imballaggio’. È femminile e al plurale "
            "diventa die Verpackungen【725387443235402†L128-L134】."
        ),
    ),
]

# Argomenti grammaticali introdotti nei vari livelli
GRAMMAR_TOPICS: List[GrammarTopic] = []

# Livello 2 – Articoli indeterminativi
GRAMMAR_TOPICS.append(
    GrammarTopic(
        level=2,
        name="Articoli indeterminativi",
        explanation=(
            "In tedesco l’articolo indeterminativo (‘un/una’) si esprime con **ein** "
            "per i sostantivi maschili e neutri e con **eine** per quelli femminili. "
            "Non esiste un articolo indeterminativo al plurale: in quel caso si omette "
            "l’articolo o si usa un quantificatore. Ad esempio: der Gabelstapler – "
            "ein Gabelstapler; die Palette – eine Palette【756518071371949†L116-L123】."),
        questions=[
            GrammarQuestion(
                prompt="Quale articolo indeterminativo (ein/eine) usi con ‘Gabelstapler’ (carrello elevatore)?",
                options=["ein", "eine", "(nessuno)"],
                answer="ein",
                explanation="Gabelstapler è maschile, quindi si usa 'ein'.",
            ),
            GrammarQuestion(
                prompt="Quale articolo indeterminativo usi con ‘Palette’ (pallet)?",
                options=["ein", "eine", "(nessuno)"],
                answer="eine",
                explanation="Palette è un sostantivo femminile; l’articolo indeterminativo è 'eine'.",
            ),
            GrammarQuestion(
                prompt="Quale articolo indeterminativo usi con ‘Lager’ (magazzino)?",
                options=["ein", "eine", "(nessuno)"],
                answer="ein",
                explanation="Lager è neutro; in nominativo singolare l’articolo indeterminativo è 'ein'.",
            ),
            GrammarQuestion(
                prompt="Esiste un articolo indeterminativo al plurale in tedesco?",
                options=["Sì, 'einige'", "No, non esiste", "Sì, 'ein' per tutti i generi"],
                answer="No, non esiste",
                explanation="In tedesco non esiste un vero e proprio articolo indeterminativo al plurale; si usano altre parole come 'einige' (alcuni)【756518071371949†L116-L123】.",
            ),
        ],
    )
)

# Livello 3 – Verbo sein al presente
GRAMMAR_TOPICS.append(
    GrammarTopic(
        level=3,
        name="Verbo sein – presente indicativo",
        explanation=(
            "Il verbo **sein** (essere) è irregolare e molto importante. Nella forma "
            "presente indicativo si coniuga così: ich bin (io sono), du bist (tu sei), "
            "er/sie/es ist (egli/ella/esso è), wir sind (noi siamo), ihr seid (voi siete), "
            "sie sind (essi sono), Sie sind (Lei è)【583649228292794†L158-L174】."),
        questions=[
            GrammarQuestion(
                prompt="Completa: ich ___ (essere)",
                options=["bin", "bist", "ist"],
                answer="bin",
                explanation="La forma per la prima persona singolare è 'ich bin'【583649228292794†L158-L174】.",
            ),
            GrammarQuestion(
                prompt="Completa: wir ___ (essere)",
                options=["ist", "sind", "seid"],
                answer="sind",
                explanation="Per la prima persona plurale si usa 'wir sind'【583649228292794†L158-L174】.",
            ),
            GrammarQuestion(
                prompt="Completa: du ___ (essere)",
                options=["bist", "bin", "seid"],
                answer="bist",
                explanation="La seconda persona singolare è 'du bist'【583649228292794†L158-L174】.",
            ),
            GrammarQuestion(
                prompt="Completa: ihr ___ (essere)",
                options=["seid", "sind", "ist"],
                answer="seid",
                explanation="Per la seconda persona plurale si usa 'ihr seid'【583649228292794†L158-L174】.",
            ),
        ],
    )
)


def get_vocabulary_by_level(level: int) -> List[VocabularyItem]:
    """Restituisce la lista dei vocaboli per un dato livello."""
    return [item for item in VOCABULARY if item.level == level]


def get_grammar_by_level(level: int) -> List[GrammarTopic]:
    """Restituisce la lista degli argomenti grammaticali per un dato livello."""
    return [topic for topic in GRAMMAR_TOPICS if topic.level == level]
