# secrets.bradsaund.com

Google-login auth wall test, live at https://secrets.bradsaund.com. Shows a secret
number only to allowlisted Google accounts. Template for future private pages
(the recipe IAP couldn't provide, since the GCP project has no organization).

## How it works

- Flask + Authlib app (`main.py`) runs the Google OAuth flow itself.
- Only emails in the `ALLOWED_EMAILS` env var (comma-separated) get past
  `/auth/callback`; everyone else gets 403.
- Runs on Cloud Run service `secrets` (project `streamlit-prototype-465722`,
  us-central1), which is publicly invokable — the app enforces auth.
- OAuth client secret lives in Secret Manager (`oauth-client-secret`) and is
  mounted as env var `GOOGLE_CLIENT_SECRET`. Rotating the secret needs no
  redeploy (service reads `:latest`).
- Domain: Cloud Run domain mapping + Cloudflare CNAME `secrets` →
  `ghs.googlehosted.com` (DNS only / gray cloud).

## Deploy an update

```bash
gcloud run deploy secrets --source . --region us-central1 \
  --project streamlit-prototype-465722
```

Env vars and the secret mount persist across deploys — no need to re-set them.

## Add another allowed account

```bash
gcloud run services update secrets --region us-central1 \
  --project streamlit-prototype-465722 \
  --update-env-vars ALLOWED_EMAILS=brad.saund@gmail.com,other@example.com
```

## Reuse for a new private page

1. Copy this app (or add routes behind the same session check).
2. Deploy as a new Cloud Run service; map `<name>.bradsaund.com` to it
   (`gcloud beta run domain-mappings create`).
3. Add `https://<name>.bradsaund.com/auth/callback` to the OAuth client's
   authorized redirect URIs in the Google console.
4. Add Cloudflare CNAME `<name>` → `ghs.googlehosted.com` (gray cloud).
