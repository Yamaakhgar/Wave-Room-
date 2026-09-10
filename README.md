# WaveRoom Web App

A simple WaveRoom demo built with:
- HTML
- CSS
- JavaScript
- Python + Flask
- Included images/assets

## Supabase setup

1. Create a Supabase project.
2. Open **SQL Editor** and run `supabase_schema.sql`.
3. Copy `.env.example` to `.env`.
4. Fill in `SUPABASE_URL` and the server-only `SUPABASE_SERVICE_ROLE_KEY`.

Never put the service role key in browser JavaScript or commit `.env` to GitHub.

## How to run on Windows

1. Install Python from https://www.python.org/
2. Open this folder in VS Code.
3. Open Terminal in VS Code.
4. Run:

```powershell
python -m pip install -r requirements.txt
python app.py
```

5. Open your browser and go to:

http://127.0.0.1:5000

## Current functionality

- WaveRoom home page
- Live room cards
- Join room button
- Create a new room
- Persistent rooms and messages through Supabase
- Dark/light theme
- Responsive mobile layout

## Deploy with Render

Create a Render Web Service from this repository. Render can use `render.yaml`
automatically. Add the two Supabase environment variables when prompted, then
deploy with the generated public URL.

## Important

Real voice calls, accounts, payments, notifications, and moderation still need
additional services and product work before accepting customers or payments.
