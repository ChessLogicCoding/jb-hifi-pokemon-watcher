# JB Hi-Fi Pokémon TCG Watcher

A small Python script that checks JB Hi-Fi’s Pokémon TCG listings and shows a desktop notification when certain keywords (e.g. **“Prismatic”**, **“151”**, **“Bundle”**, **“Elite”**) appear.

- Randomised check interval (10–30 s) to avoid hammering the site
- Headless Chrome via Selenium
- Desktop notifications via `plyer`

## Requirements

- Python 3.9+
- Google Chrome installed
- Python packages:
pip install selenium plyer
