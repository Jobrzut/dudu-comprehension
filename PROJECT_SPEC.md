## 1. Overview
**DuDu 读度** is a lightweight, zero-config Anki desktop add-on for Mandarin and Cantonese learners. Users paste any real-world text (news articles, video transcripts, short stories) into an analysis window, select which Anki deck(s) and note field(s) represent their known vocabulary, and immediately see:
1. How much of the text they can already read (coverage percentages + readability rating).
2. A color-coded reading view highlighting known words in green and unknown words in red (with an optional toggle to split Mature vs. Learning cards).
3. One-click flashcard creation (with automatic source-sentence capture) for unknown words.

---

## 2. User Workflow
1. User opens **Tools → DuDu 读度: Analyze Text** in Anki.
2. User selects:
   - **Language Mode:** `Mandarin` (default), `Cantonese`, or `Space-Separated` (basic fallback).
   - **Vocabulary Source:** Specific deck(s) or entire collection, plus the target field name (e.g., `Hanzi`, `Simplified`, `Front`).
3. User pastes text and clicks **Analyze**.
4. The UI renders summary charts, a ranked list of top unknown words, and the full annotated passage.
5. While reading:
   - Clicking an **unknown (red)** word opens Anki's native **Add Cards** dialog pre-filled with the word and the full sentence it appeared in.
   - Clicking a **known (green)** word opens Anki's **Card Browser** filtered to that existing note.

---

## 3. Core Features

### MVP (Checkpoint 1 & 2)
- **Vocabulary Indexing:** Query `mw.col` using Anki search filters to build fast lookup sets of known words:
  - **Default Mode (Binary Known / Unknown):**
    - **Known (Green):** Any studied card (`-is:new`), combining both Mature and Learning states.
    - **Unknown (Red):** Absent from selected deck/field (or still `is:new`).
  - **Optional Toggle ("Split Mature vs. Learning"):** Off by default. When enabled in the UI/config, splits Known into:
    - **Mature (Green):** `prop:ivl>=21`
    - **Learning / Young (Amber):** `-is:new prop:ivl<21`
- **Tokenization:**
  - **Mandarin:** Pure-Python `jieba` tokenizer.
  - **Cantonese:** Separate `jieba.Tokenizer()` instance loaded with a CC-Canto custom user dictionary.
  - **Space-Separated:** Regex word-boundary fallback (`\b\w+\b`).
  - Strip whitespace, numbers, and CJK/ASCII punctuation from statistical counts while preserving original formatting and line breaks in the rendered reading view.
- **Comprehension Metrics & Readability Tier:**
  - **Total Text Coverage %:** `(known word occurrences / total word occurrences) * 100`.
  - **Unique Words Known %:** `(unique known words in text / total unique words in text) * 100`.
  - **Readability Badge:** `98%+` = Smooth Read, `95–97%` = Good Study Challenge, `90–94%` = Intensive Reading, `<90%` = Heavy Lookup.
- **Annotated Reading View:**
  - Display words as soft tinted pill badges (`border-radius: 4px`) with generous CJK line height (`2.1`) and font sizing (`18px`).
  - **"Focus Unknowns" Toggle:** Hides green (and amber) highlights so advanced learners only see red unknown words.

### Polish & V2 Enhancements (Checkpoint 3)
- **Inline SVG Charts:** Two side-by-side bento cards at the top with lightweight SVG donut/bar gauges (no `matplotlib` or external plotting dependencies).
- **High-Impact Unknowns Bar:** Ranked list of the top 5–10 unknown words sorted by frequency in the pasted text (e.g., `经济 ×7`).
- **One-Click Sentence Mining:** Clicking a red word extracts the surrounding sentence (split on `。！？!?`) and calls `aqt.dialogs.open("AddCards", mw)` with both the target word and sentence fields pre-populated.
- **Known-Character Hint:** Give unknown multi-character words a dashed red border if 100% of their individual characters already exist in the user's known character set.
- **Optional Simplified ↔ Traditional Matching:** Checkbox using a bundled character conversion map so Traditional cards match Simplified text (and vice versa).
- **Theme Sync:** Automatically adapt CSS variables to Anki's light or dark mode (`aqt.theme.theme_manager.night_mode`).
- Add **CC-CEDICT** (Mandarin) and **CC-Canto** (Cantonese) for words translations - while creating cards but also for inspecting in reading view.

---

## 4. Technical Architecture & Constraints (For AI Assistants)
- **Target Environment:** Modern Anki (`23.10+` / `24.x` / `25.x`, Qt6, Python 3.10+).
- **UI Framework:** Build the main dialog using `aqt.webview.AnkiWebView` with a self-contained HTML/CSS/JS template and `pycmd` message bridge for Python ↔ JS actions. Keep Qt boilerplate minimal.
- **Anki API Rules:**
  - Import all Qt classes from `aqt.qt`, never directly from `PyQt5` or `PyQt6`.
  - Register menu actions via `aqt.gui_hooks.main_window_did_init`.
  - Never access `mw.col` at module import time; read collection data only inside user-triggered callbacks.
  - Never execute raw SQL against `mw.col.db`.
- **Dependencies:** Pure Python only. Vendor third-party packages like `jieba` inside `vendor/` and append to `sys.path` safely so the add-on works cross-platform (Windows, macOS, Linux) with zero `pip` steps for end users.

---

## 5. Planned Folder Structure
```text
dudu_comprehension/
├── __init__.py          # Entry point: registers Tools menu item via gui_hooks
├── manifest.json        # Anki add-on metadata ("name": "DuDu 读度 - Mandarin & Cantonese Comprehension Analyzer")
├── config.json          # Default settings (deck, target field, sentence field, mode, split_mature_learning: false)
├── analyzer.py          # Collection querying, jieba tokenization, coverage math
├── gui.py               # QDialog + AnkiWebView wrapper & pycmd handler
├── web/
│   └── template.html    # Self-contained UI (CSS variables, SVG charts, reading view)
├── data/
│   └── cantonese_words.txt
└── vendor/
    └── jieba/           # Vendored pure-Python segmenter
```