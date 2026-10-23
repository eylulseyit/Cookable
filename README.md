# Cookable

[![CI](https://github.com/eylulseyit/Cookable/actions/workflows/ci.yml/badge.svg?branch=dev)](https://github.com/eylulseyit/Cookable/actions/workflows/ci.yml)
[![License: AGPL-3.0](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](LICENSE)

Cookable helps you cook with what you already have. Tell it what's in your kitchen and it suggests a recipe, along with a shopping list for anything missing.

The goal is a meal planner that knows your pantry: snap a photo of your fridge, keep track of your ingredients, and get a weekly plan that fits your diet and nutrition goals.

> **Work in progress.** Cookable is in active development, so things change often.

## Running locally

You need Docker or Podman with Compose, and a free [Gemini API key](https://aistudio.google.com/apikey).

```bash
cp backend/.env.example backend/.env   # then set GOOGLE_API_KEY
docker compose up --build              # or: podman compose up --build
```

Open http://localhost:3000.

## License

Cookable is licensed under the [GNU Affero General Public License v3.0 or later](LICENSE).
