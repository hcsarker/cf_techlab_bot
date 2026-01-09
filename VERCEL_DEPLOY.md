# 🚀 Deploy CF TechLab Chatbot to Render.com

## For Vercel Website: cftechlab.vercel.app

---

## ✨ Why Render.com?

- Free tier suitable for small Flask apps
- One-click Blueprint with `render.yaml`
- Health checks and auto-redeploy on commit
- No "serverless cold start" delays

---

## 🚀 Quick Deploy Steps (Blueprint)

1. Push repo to GitHub (branch `HCS` if applicable).
2. In Render: New → Blueprint → select this repo.
3. Confirm service settings from `render.yaml`:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app --workers 1 --bind 0.0.0.0:$PORT --timeout 120`
   - Health check: `/health`
4. Click Create Resources → wait for build and deploy.
5. Copy your URL: `https://your-service.onrender.com`.

---

## 🛠️ Manual Web Service (Alternative)

1. New → Web Service → connect GitHub repo.
2. Runtime: Python
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app --workers 1 --bind 0.0.0.0:$PORT --timeout 120`
5. Health Check Path: `/health`
6. Create Web Service → copy URL.

---

## 🌐 Add to Vercel

Place this before `</body>` in your site or add as a component:

```html
<!-- CF TechLab AI Chatbot (Render) -->
<iframe
  src="https://your-service.onrender.com/widget"
  style="position: fixed; bottom: 0; right: 0; width: 100%; height: 100%; border: none; z-index: 999999; pointer-events: none;"
  id="cf-chatbot-iframe"
>
</iframe>

<style>
  #cf-chatbot-iframe { pointer-events: none; }
</style>

<script>
  const iframe = document.getElementById('cf-chatbot-iframe');
  document.addEventListener('mousemove', (e) => {
    const nearCorner = e.clientX > window.innerWidth - 150 && e.clientY > window.innerHeight - 150;
    iframe.style.pointerEvents = nearCorner ? 'auto' : 'none';
  });
</script>
```

### Next.js/React snippet

```jsx
<iframe
  id="cf-chatbot-iframe"
  src="https://your-service.onrender.com/widget"
  style={{ position: 'fixed', bottom: 0, right: 0, width: '100%', height: '100%', border: 'none', zIndex: 999999, pointerEvents: 'none' }}
/>
```

---

## 🧪 Test Your Deployment

```bash
# Health check
curl https://your-service.onrender.com/health
```

- Widget: `https://your-service.onrender.com/widget`
- Admin: `https://your-service.onrender.com/admin`

---

## ⚠️ Troubleshooting

- Error: `bash: line 1: web:: command not found`
  - Cause: Start Command included `web:` from Procfile.
  - Fix: Use only `gunicorn app:app --workers 1 --bind 0.0.0.0:$PORT --timeout 120`.

---

## ✅ Checklist

- [ ] Push chatbot to GitHub
- [ ] Deploy on Render (Blueprint or Web Service)
- [ ] Copy Render URL (`your-service.onrender.com`)
- [ ] Update iframe `src` in your Vercel project
- [ ] Test locally and on Vercel site
- [ ] Verify `/health` and `/admin` work
