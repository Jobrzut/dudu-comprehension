# Copilot Instructions – DuDu 读度 (`dudu_comprehension`)

Read `PROJECT_SPEC.md` in the repository root for full feature requirements, UI design, and folder layout before generating code.

## Anki API & Qt6 Rules
- Target modern Anki (`23.10+` / `24.x` / `25.x`, Qt6, Python 3.10+).
- Always import Qt widgets from `aqt.qt` (e.g., `from aqt.qt import QDialog, QVBoxLayout`), NEVER directly from `PyQt5` or `PyQt6`.
- Register menu items and lifecycle hooks using modern `aqt.gui_hooks` (e.g., `gui_hooks.main_window_did_init`), NEVER legacy `anki.hooks.addHook`.
- Access `mw.col` only inside user-triggered callbacks or after `profile_did_open`, NEVER at module import time.
- Keep `__init__.py` minimal; separate logic (`analyzer.py`), dialog/bridge (`gui.py`), and frontend (`web/template.html`).

## Database & File Safety
- NEVER execute raw SQL (`mw.col.db.execute`) to modify notes, cards, or decks; always use official Anki APIs (`mw.col.find_notes`, `mw.col.get_note`, `aqt.dialogs.open`).
- Never write, move, or delete files outside the add-on's own `user_files` directory.

## Architecture & Dependencies
- Build the UI inside `aqt.webview.AnkiWebView` using a self-contained HTML/CSS/JS template and `pycmd` for Python ↔ JavaScript communication.
- Use pure-Python dependencies only; load vendored libraries from `vendor/` (such as `jieba`) by inserting `vendor/` into `sys.path`.
- Do not add `matplotlib`, `plotly`, or external chart libraries—render charts as lightweight inline SVGs.