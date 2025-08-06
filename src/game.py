"""
Videogioco interattivo per imparare il tedesco (versione da terminale).

Questo programma guida l’utente attraverso livelli progressivi che introducono
vocabolario e nozioni grammaticali.  Al termine di ogni livello viene
calcolato un punteggio: se l’utente raggiunge almeno l’80 % di risposte
corrette, sblocca il livello successivo.  Il gioco salva automaticamente
l’avanzamento in un file `progress.json`.

Per avviare il gioco eseguire:

```
python3 game.py
```

Il gioco richiede solo la libreria standard di Python.
"""

import json
import os
import random
import datetime
from typing import List, Dict, Any

from data import (
    VocabularyItem,
    GrammarTopic,
    get_vocabulary_by_level,
    get_grammar_by_level,
    VOCABULARY,
    GRAMMAR_TOPICS,
)

PROGRESS_FILE = os.path.join(os.path.dirname(__file__), "progress.json")


def load_progress() -> Dict[str, Any]:
    """Carica il progresso dal file se esiste, altrimenti restituisce valori iniziali."""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "current_level": 1,
        "learned_words": [],
        "last_review_date": None,
        "scores": {},
    }


def save_progress(progress: Dict[str, Any]) -> None:
    """Salva il progresso su disco."""
    try:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Errore nel salvataggio del progresso: {e}")


def print_menu(current_level: int):
    print("\n=== Deutschland – Impara il tedesco ===")
    print(f"Livello attuale: {current_level}")
    print("1. Inizia livello")
    print("2. Ripasso giornaliero")
    print("3. Esci")


def ask_choice(num_options: int) -> int:
    """Richiede all’utente di inserire un numero di opzione valido."""
    while True:
        choice = input("Seleziona un’opzione: ")
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= num_options:
                return idx
        print(f"Inserisci un numero compreso tra 1 e {num_options}.")


def generate_level_questions(level: int) -> List[Dict[str, Any]]:
    """Crea la lista delle domande per un dato livello."""
    questions: List[Dict[str, Any]] = []
    vocab_items = get_vocabulary_by_level(level)
    grammar_topics = get_grammar_by_level(level)
    # Vocabolario
    for item in vocab_items:
        # Traduzione
        correct_option = f"{item.article} {item.singular}"
        distractors = [f"{other.article} {other.singular}" for other in vocab_items if other.singular != item.singular]
        random.shuffle(distractors)
        opts = [correct_option] + distractors[:2]
        random.shuffle(opts)
        questions.append(
            {
                "prompt": f"Scegli il termine tedesco corretto per '{item.translation}':",
                "options": opts,
                "answer": correct_option,
                "explanation": item.explanation,
            }
        )
        # Plurale
        correct_plural = f"die {item.plural}"
        distract_plurals = [f"die {other.plural}" for other in vocab_items if other.singular != item.singular]
        random.shuffle(distract_plurals)
        opts2 = [correct_plural] + distract_plurals[:2]
        random.shuffle(opts2)
        questions.append(
            {
                "prompt": f"Qual è il plurale corretto di '{item.article} {item.singular}'?",
                "options": opts2,
                "answer": correct_plural,
                "explanation": item.explanation,
            }
        )
    # Grammatica
    for topic in grammar_topics:
        for q in topic.questions:
            questions.append(
                {
                    "prompt": q.prompt,
                    "options": q.options,
                    "answer": q.answer,
                    "explanation": q.explanation,
                }
            )
    random.shuffle(questions)
    return questions


def run_questionnaire(questions: List[Dict[str, Any]]) -> int:
    """Esegue una serie di domande e restituisce il numero di risposte corrette."""
    correct = 0
    for idx, q in enumerate(questions, start=1):
        print(f"\nDomanda {idx}/{len(questions)}")
        print(q["prompt"])
        for i, opt in enumerate(q["options"], start=1):
            print(f"  {i}. {opt}")
        choice = ask_choice(len(q["options"]))
        selected = q["options"][choice - 1]
        if selected == q["answer"]:
            correct += 1
            print("✔️  Corretto!")
        else:
            print(f"❌  Sbagliato. La risposta corretta era: {q['answer']}")
        # Mostra spiegazione
        print(f"Spiegazione: {q['explanation']}")
    return correct


def start_level(progress: Dict[str, Any]):
    level = progress.get("current_level", 1)
    max_level = max(item.level for item in VOCABULARY)
    if level > max_level:
        print("\nHai completato tutti i livelli disponibili! Usa la modalità di ripasso per continuare a esercitarti.")
        return
    print(f"\n*** Inizio del livello {level} ***")
    # Mostra i vocaboli nuovi
    vocab_items = get_vocabulary_by_level(level)
    if vocab_items:
        print("Vocaboli introdotti in questo livello:")
        for item in vocab_items:
            print(f"- {item.article} {item.singular} (plurale: {item.plural}) – {item.translation}")
    # Mostra spiegazioni grammaticali
    grammar_topics = get_grammar_by_level(level)
    for topic in grammar_topics:
        print(f"\nRegola: {topic.name}")
        print(topic.explanation)
    input("\nPremi INVIO per iniziare gli esercizi...")
    questions = generate_level_questions(level)
    correct = run_questionnaire(questions)
    score_percent = int((correct / len(questions)) * 100) if questions else 0
    print(f"\nHai risposto correttamente al {score_percent}% delle domande.")
    progress["scores"][str(level)] = score_percent
    if correct / len(questions) >= 0.8:
        print("Complimenti! Hai superato il livello.")
        # Aggiungi i vocaboli alle parole imparate
        for item in vocab_items:
            if item.singular not in progress["learned_words"]:
                progress["learned_words"].append(item.singular)
        # Avanza al livello successivo se non già oltre
        if progress["current_level"] == level:
            progress["current_level"] += 1
    else:
        print("Non hai raggiunto l'80% di risposte corrette. Prova di nuovo il livello per superarlo.")
    save_progress(progress)


def daily_review(progress: Dict[str, Any]):
    learned = progress.get("learned_words", [])
    if not learned:
        print("\nNon hai ancora vocaboli da ripassare. Completa prima almeno un livello.")
        return
    # Verifica la data
    last_date = progress.get("last_review_date")
    today = datetime.date.today().isoformat()
    if last_date == today:
        ans = input("\nHai già eseguito il ripasso oggi. Vuoi ripassare di nuovo? (s/n): ")
        if ans.strip().lower() != "s":
            return
    # Costruisci domande miste dai vocaboli e dalla grammatica già sbloccata
    max_level_done = progress.get("current_level", 1) - 1
    vocab_items = [item for item in VOCABULARY if item.singular in learned]
    grammar_topics: List[GrammarTopic] = [topic for topic in GRAMMAR_TOPICS if topic.level <= progress.get("current_level", 1)]
    questions: List[Dict[str, Any]] = []
    # Domande vocabolario
    for item in vocab_items:
        if random.choice([True, False]):
            # Traduzione
            correct_option = f"{item.article} {item.singular}"
            distractors = [f"{other.article} {other.singular}" for other in vocab_items if other.singular != item.singular]
            random.shuffle(distractors)
            opts = [correct_option] + distractors[:2]
            random.shuffle(opts)
            questions.append(
                {
                    "prompt": f"Scegli il termine tedesco corretto per '{item.translation}':",
                    "options": opts,
                    "answer": correct_option,
                    "explanation": item.explanation,
                }
            )
        else:
            # Plurale
            correct_plural = f"die {item.plural}"
            distract_plurals = [f"die {other.plural}" for other in vocab_items if other.singular != item.singular]
            random.shuffle(distract_plurals)
            opts2 = [correct_plural] + distract_plurals[:2]
            random.shuffle(opts2)
            questions.append(
                {
                    "prompt": f"Qual è il plurale corretto di '{item.article} {item.singular}'?",
                    "options": opts2,
                    "answer": correct_plural,
                    "explanation": item.explanation,
                }
            )
    # Domande grammatica
    for topic in grammar_topics:
        for q in topic.questions:
            questions.append(
                {
                    "prompt": q.prompt,
                    "options": q.options,
                    "answer": q.answer,
                    "explanation": q.explanation,
                }
            )
    random.shuffle(questions)
    print("\n*** Ripasso ***")
    correct = run_questionnaire(questions)
    score_percent = int((correct / len(questions)) * 100) if questions else 0
    print(f"\nRipasso completato: {score_percent}% di risposte corrette.")
    # Aggiorna data
    progress["last_review_date"] = today
    save_progress(progress)


def main():
    progress = load_progress()
    while True:
        print_menu(progress.get("current_level", 1))
        choice = ask_choice(3)
        if choice == 1:
            start_level(progress)
        elif choice == 2:
            daily_review(progress)
        elif choice == 3:
            print("Auf Wiedersehen! Arrivederci!")
            break


if __name__ == "__main__":
    main()
