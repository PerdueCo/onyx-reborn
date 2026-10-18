# Deploying Onyx Reborn to Render (free plan)

## Prerequisites
- A [GitHub](https://github.com) account with this repo pushed to it (`PerdueCo/onyx-reborn`).
- Python 3.12 installed locally (to generate the key in step 4).

---

## Steps

### 1 — Sign up for Render (free, no credit card required)
1. Go to <https://render.com>.
2. Click **Get Started for Free**.
3. Choose **Continue with GitHub** and authorise Render to read your repositories.

### 2 — Create a new Blueprint deployment
1. In the Render dashboard, click **New +** in the top-right corner.
2. Select **Blueprint**.
3. Render will ask you to connect a Git repository — choose **PerdueCo/onyx-reborn**.
4. Render detects `render.yaml` automatically and shows a service called **onyx-reborn**.
5. Click **Apply** (you do not need to change anything yet — you will paste the key next).

### 3 — Wait for the initial build to start
Render will begin a Docker build. It will **fail** on the first boot because `MFA_ENC_KEY`
has not been set yet. That is expected — you will fix it in the next step.

### 4 — Generate MFA_ENC_KEY on your local machine
Open a terminal and run:

```
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Copy the output — it looks like: `ABC123...=` (44 URL-safe base64 characters).

> **Important:** keep this key safe. If you lose it, all TOTP secrets stored in the
> database become unreadable and demo users will not be able to sign in with 2-FA.

### 5 — Paste MFA_ENC_KEY into the Render dashboard
1. In the Render dashboard, click the **onyx-reborn** service.
2. Go to **Environment** in the left sidebar.
3. Find the `MFA_ENC_KEY` variable (it was created by the Blueprint with no value).
4. Click the pencil icon, paste the key you generated in step 4, and click **Save**.
5. Render will automatically trigger a new deploy.

### 6 — Watch the deploy logs
1. Click **Logs** in the left sidebar of the **onyx-reborn** service.
2. You should see lines like:
   ```
   ==> DEMO_MODE: seeding fresh database...
   ...
   INFO:     Application startup complete.
   ```
3. When you see `Application startup complete`, the service is live.

### 7 — Open the app
Click the URL shown at the top of the service page
(e.g. `https://onyx-reborn.onrender.com`).

Demo logins are printed in the build logs by `reset_db.py`:
| Account | Email | Password | TOTP secret |
|---------|-------|----------|-------------|
| Admin | admin@onyx.demo | OnyxAdmin2026! | JBSWY3DPEHPK3PXP |
| Staff | staff@onyx.demo | OnyxStaff2026! | JBSWY3DPEHPK3PXQ |

Use any TOTP app (Google Authenticator, Authy) or run:
```
python -c "import pyotp; print(pyotp.TOTP('JBSWY3DPEHPK3PXP').now())"
```

---

## Free-plan notes

- **Cold starts:** Render's free plan spins the container down after ~15 minutes of
  inactivity. The first visit after a sleep period can take **~1 minute** to respond.
  This is normal — just wait for the page to load.
- **Ephemeral disk:** The SQLite database is rebuilt on every deploy because the
  container's filesystem is not persistent. Demo data is always fresh.
- **No custom domain** on the free plan unless you add one manually in the dashboard.
