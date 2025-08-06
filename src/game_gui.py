"""
Interfaccia grafica per il videogioco Deutschland.

Questa versione utilizza la libreria ``pygame`` per mostrare domande a video
e consente di riprodurre l'audio delle parole tramite la libreria
``pyttsx3`` (sintesi vocale offline).  È una versione semplificata
rispetto alla CLI ma fornisce un'esperienza più immersiva con pulsanti,
testo formattato e supporto alla pronuncia.

Requisiti:

* Python 3.8 o superiore.
* Libreria ``pygame`` (installabile con ``pip install pygame``).
* Libreria ``pyttsx3`` per la sintesi vocale (installabile con ``pip install pyttsx3``).

Il gioco mantiene la stessa logica di base della versione CLI: l'utente
affronta livelli progressivi e può effettuare un ripasso quotidiano.

Nota: se ``pygame`` o ``pyttsx3`` non sono installati, il programma
uscirà con un messaggio di errore.

"""

import sys
import os
import json
import random
import datetime
from typing import List, Dict, Any, Tuple

# Importa le strutture dati dal modulo esistente
from data import (
    VocabularyItem,
    GrammarTopic,
    get_vocabulary_by_level,
    get_grammar_by_level,
    VOCABULARY,
    GRAMMAR_TOPICS,
)



def check_dependencies() -> None:
    """Verifica che pygame e pyttsx3 siano installati; esce con errore in caso contrario."""
    try:
        import pygame  # noqa: F401
    except ImportError as e:
        print("Errore: la libreria pygame non è installata. Installa con 'pip install pygame'.")
        raise e
    try:
        import pyttsx3  # noqa: F401
    except ImportError as e:
        print("Errore: la libreria pyttsx3 non è installata. Installa con 'pip install pyttsx3'.")
        raise e



def speak(text: str) -> None:
    """Riproduce audio tramite pyttsx3. Se il motore non è disponibile, stampa il testo."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
    except Exception:
        # Fallback: stampa invece di pronunciare
        print(f"[PRONUNCIA] {text}")


class Button:
    """Classe semplice per rappresentare un pulsante in pygame."""

    def __init__(self, rect: Tuple[int, int, int, int], text: str, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback

    def draw(self, surface, font, color_bg=(200, 200, 200), color_text=(0, 0, 0)):
        pygame.draw.rect(surface, color_bg, self.rect)
        label = font.render(self.text, True, color_text)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()


class DeutschlandGUI:
    """Classe principale per gestire il gioco grafico."""

    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        check_dependencies()
        import pygame  # import locale dopo verifica
        pygame.init()
        pygame.display.set_caption("Deutschland – Impara il tedesco")
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)
        self.large_font = pygame.font.SysFont(None, 36)
        # caricamento/salvataggio
        self.progress_file = os.path.join(os.path.dirname(__file__), "progress.json")
        self.progress: Dict[str, Any] = self.load_progress()
        self.questions: List[Dict[str, Any]] = []
        self.current_question_index: int = 0
        self.correct_count: int = 0
        self.state: str = "menu"  # stati: menu, level, review, result
        self.buttons: List[Button] = []

    def load_progress(self) -> Dict[str, Any]:
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "current_level": 1,
            "learned_words": [],
            "last_review_date": None,
            "scores": {},
        }

    def save_progress(self) -> None:
        try:
            with open(self.progress_file, "w", encoding="utf-8") as f:
                json.dump(self.progress, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Errore nel salvataggio del progresso: {e}")

    def reset_questions(self, level: int, review: bool = False) -> None:
        """Prepara le domande per un livello o ripasso."""
        if review:
            # Domande miste dai vocaboli imparati e dalla grammatica sbloccata
            learned = self.progress.get("learned_words", [])
            vocab_items = [item for item in VOCABULARY if item.singular in learned]
            grammar_topics = [topic for topic in GRAMMAR_TOPICS if topic.level <= self.progress.get("current_level", 1)]
            questions: List[Dict[str, Any]] = []
            for item in vocab_items:
                if random.choice([True, False]):
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
            self.questions = questions
        else:
            self.questions = generate_level_questions(level)
        self.current_question_index = 0
        self.correct_count = 0

    def draw_menu(self) -> None:
        self.screen.fill((255, 255, 255))
        title = self.large_font.render("Deutschland – Impara il tedesco", True, (0, 0, 0))
        self.screen.blit(title, (self.WIDTH // 2 - title.get_width() // 2, 50))
        level = self.progress.get("current_level", 1)
        sub = self.font.render(f"Livello attuale: {level}", True, (0, 0, 0))
        self.screen.blit(sub, (self.WIDTH // 2 - sub.get_width() // 2, 100))
        # Definisce pulsanti
        self.buttons = []
        def start_level_cb():
            self.state = "level"
            self.reset_questions(level)
        def start_review_cb():
            self.state = "review"
            self.reset_questions(level, review=True)
        def exit_cb():
            pygame.quit()
            sys.exit(0)
        self.buttons.append(Button((self.WIDTH//2 - 100, 200, 200, 40), "Inizia livello", start_level_cb))
        self.buttons.append(Button((self.WIDTH//2 - 100, 260, 200, 40), "Ripasso giornaliero", start_review_cb))
        self.buttons.append(Button((self.WIDTH//2 - 100, 320, 200, 40), "Esci", exit_cb))
        for btn in self.buttons:
            btn.draw(self.screen, self.font, color_bg=(220, 220, 220))

    def draw_question(self) -> None:
        self.screen.fill((255, 255, 255))
        if self.current_question_index >= len(self.questions):
            # Fine questionario
            percent = int((self.correct_count / len(self.questions)) * 100) if self.questions else 0
            msg = f"Hai risposto correttamente al {percent}% delle domande."
            result = self.large_font.render(msg, True, (0, 0, 0))
            self.screen.blit(result, (self.WIDTH//2 - result.get_width()//2, 200))
            # Aggiorna progresso se livello
            if self.state == "level":
                level = self.progress.get("current_level", 1)
                self.progress["scores"][str(level)] = percent
                if self.correct_count / len(self.questions) >= 0.8:
                    # Avanza livello
                    # aggiorna parole imparate
                    for item in get_vocabulary_by_level(level):
                        if item.singular not in self.progress["learned_words"]:
                            self.progress["learned_words"].append(item.singular)
                    max_level = max(item.level for item in VOCABULARY)
                    if level < max_level:
                        self.progress["current_level"] = level + 1
                self.save_progress()
            elif self.state == "review":
                # aggiorna data ripasso
                today = datetime.date.today().isoformat()
                self.progress["last_review_date"] = today
                self.save_progress()
            # Pulsante per tornare al menu
            def back_cb():
                self.state = "menu"
            self.buttons = [Button((self.WIDTH//2 - 100, 300, 200, 40), "Torna al menu", back_cb)]
            for btn in self.buttons:
                btn.draw(self.screen, self.font, color_bg=(200, 230, 200))
            return
        # Mostra domanda corrente
        q = self.questions[self.current_question_index]
        prompt_lines = self.wrap_text(q["prompt"], self.WIDTH - 40, self.font)
        y = 40
        for line in prompt_lines:
            label = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(label, (20, y))
            y += label.get_height() + 2
        # Mostra opzioni come pulsanti
        self.buttons = []
        base_y = y + 20
        for idx, opt in enumerate(q["options"]):
            def make_callback(opt=opt):
                def cb():
                    # registra scelta, controlla correttezza e mostra spiegazione
                    is_correct = opt == q["answer"]
                    if is_correct:
                        self.correct_count += 1
                    # parlato: pronuncia l'opzione scelta per rinforzo
                    speak(opt)
                    # mostra spiegazione breve in console e continua
                    # nella GUI potremmo mostrare un messaggio temporaneo
                    self.current_question_index += 1
                return cb
            btn = Button((40, base_y + idx*60, 500, 40), opt, make_callback())
            self.buttons.append(btn)
            # Pulsante audio per l'opzione
            def audio_cb(word=opt):
                return lambda: speak(word)
            audio_button = Button((560, base_y + idx*60, 40, 40), "🔊", audio_cb(opt))
            self.buttons.append(audio_button)
        # Non disegna spiegazione qui; spiegazione sarà stampata in console
        for btn in self.buttons:
            # colore diverso per audio
            if btn.text == "🔊":
                btn.draw(self.screen, self.font, color_bg=(230, 230, 250))
            else:
                btn.draw(self.screen, self.font, color_bg=(210, 210, 210))

    def wrap_text(self, text: str, max_width: int, font) -> List[str]:
        """Divide il testo in righe che non superano la larghezza indicata."""
        words = text.split()
        lines: List[str] = []
        current = ""
        for word in words:
            test = f"{current} {word}" if current else word
            if font.size(test)[0] <= max_width:
                current = test
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def run(self) -> None:
        import pygame  # reinizializza alias
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    # Gestione pulsanti
                    for btn in self.buttons:
                        btn.handle_event(event)
            if self.state == "menu":
                self.draw_menu()
            elif self.state in ("level", "review"):
                self.draw_question()
            pygame.display.flip()
            self.clock.tick(30)
        pygame.quit()


def generate_level_questions(level: int) -> List[Dict[str, Any]]:
    """Funzione di utilità condivisa con la versione CLI per generare domande per un livello."""
    questions: List[Dict[str, Any]] = []
    vocab_items = get_vocabulary_by_level(level)
    grammar_topics = get_grammar_by_level(level)
    for item in vocab_items:
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


if __name__ == "__main__":
    gui = DeutschlandGUI()
    gui.run()
