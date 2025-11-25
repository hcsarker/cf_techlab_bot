# 🚀 Deploy CF TechLab Chatbot to Railway.app

## For Vercel Website: cftechlab.vercel.app

---

## ✨ Why Railway.app?

- ✅ **Free Tier:** $5 credit/month (enough for chatbot)
- ✅ **Auto Deploy:** GitHub integration
- ✅ **Custom Domain:** Free SSL
- ✅ **No Cold Start:** Unlike serverless
- ✅ **Easy Setup:** 5 minutes deploy

---

## 🚀 Quick Deploy Steps

### Step 1: Push to GitHub

```bash
cd /home/hridoy/Documents/Project/cf_techlab_bot

# Add all files
git add .
git commit -m "Add Railway deployment config"
git push origin HCS
```

### Step 2: Deploy on Railway

1. **Visit:** https://railway.app/
2. **Sign in** with GitHub
3. **Click:** "New Project"
4. **Select:** "Deploy from GitHub repo"
5. **Choose:** `hcsarker/cf_techlab_bot`
6. **Branch:** HCS
7. **Click:** Deploy

Railway will automatically:

- Detect Python project
- Install dependencies from `requirements.txt`
- Run `Procfile` command
- Generate a public URL

### Step 3: Get Your Railway URL

After deployment (2-3 minutes):

- You'll get a URL like: `https://cf-techlab-bot-production.up.railway.app`
- Or set custom domain: `chatbot.cftechlab.com`

### Step 4: Add to Vercel Website

Go to your Vercel project and add this code:

**In your HTML/React component (before `</body>` or in layout):**

```html
<!-- CF TechLab AI Chatbot -->
<iframe
  src="https://cf-techlab-bot-production.up.railway.app/widget"
  style="position: fixed; bottom: 0; right: 0; width: 100%; height: 100%; border: none; z-index: 999999; pointer-events: none;"
  id="cf-chatbot-iframe"
>
</iframe>

<style>
  #cf-chatbot-iframe {
    pointer-events: none;
  }
</style>

<script>
  const iframe = document.getElementById("cf-chatbot-iframe");

  document.addEventListener("mousemove", function (e) {
    if (
      e.clientX > window.innerWidth - 150 &&
      e.clientY > window.innerHeight - 150
    ) {
      iframe.style.pointerEvents = "auto";
    } else {
      iframe.style.pointerEvents = "none";
    }
  });
</script>
```

---

## 🎨 For Next.js/React (Vercel)

### Option A: Add to `app/layout.js` or `pages/_app.js`

```jsx
export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}

        {/* CF TechLab Chatbot */}
        <iframe
          src="https://cf-techlab-bot-production.up.railway.app/widget"
          style={{
            position: "fixed",
            bottom: 0,
            right: 0,
            width: "100%",
            height: "100%",
            border: "none",
            zIndex: 999999,
            pointerEvents: "none",
          }}
          id="cf-chatbot-iframe"
        />

        <script
          dangerouslySetInnerHTML={{
            __html: `
            const iframe = document.getElementById('cf-chatbot-iframe');
            document.addEventListener('mousemove', function(e) {
              if (e.clientX > window.innerWidth - 150 && e.clientY > window.innerHeight - 150) {
                iframe.style.pointerEvents = 'auto';
              } else {
                iframe.style.pointerEvents = 'none';
              }
            });
          `,
          }}
        />
      </body>
    </html>
  );
}
```

### Option B: Create a Component

```jsx
// components/Chatbot.jsx
"use client"; // For Next.js 13+

import { useEffect } from "react";

export default function Chatbot() {
  useEffect(() => {
    const iframe = document.getElementById("cf-chatbot-iframe");
    if (!iframe) return;

    const handleMouseMove = (e) => {
      if (
        e.clientX > window.innerWidth - 150 &&
        e.clientY > window.innerHeight - 150
      ) {
        iframe.style.pointerEvents = "auto";
      } else {
        iframe.style.pointerEvents = "none";
      }
    };

    document.addEventListener("mousemove", handleMouseMove);
    return () => document.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return (
    <iframe
      id="cf-chatbot-iframe"
      src="https://cf-techlab-bot-production.up.railway.app/widget"
      style={{
        position: "fixed",
        bottom: 0,
        right: 0,
        width: "100%",
        height: "100%",
        border: "none",
        zIndex: 999999,
        pointerEvents: "none",
      }}
    />
  );
}
```

Then import in your layout:

```jsx
import Chatbot from "@/components/Chatbot";

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Chatbot />
      </body>
    </html>
  );
}
```

---

## 🔧 Alternative: Render.com

If Railway doesn't work, try Render.com:

1. Visit: https://render.com/
2. Sign in with GitHub
3. Click "New +" → "Web Service"
4. Connect `hcsarker/cf_techlab_bot`
5. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Environment:** Python 3

Same embed code, just change URL to Render URL.

---

## 🧪 Test Your Deployment

### 1. Check Health

```bash
curl https://your-railway-url.up.railway.app/health
```

Should return:

```json
{ "status": "healthy", "model_loaded": true }
```

### 2. Test Widget

Visit: `https://your-railway-url.up.railway.app/widget`

### 3. Test on Vercel Site

Visit: `https://cftechlab.vercel.app`

You should see chat button in bottom-right! 🎉

---

## 📊 Admin Dashboard

Access admin panel:

```
https://your-railway-url.up.railway.app/admin
```

Monitor:

- Total users
- All conversations
- User info (name, mobile, email)
- Feedback data

---

## 🔄 Update & Redeploy

```bash
# Make changes
git add .
git commit -m "Update chatbot"
git push origin HCS
```

Railway will auto-deploy! ✨

---

## 💰 Cost Estimate

**Railway Free Tier:**

- $5 credit/month
- ~500 hours runtime
- Good for: 1000-2000 conversations/month

**If you need more:**

- Railway Hobby: $5/month
- Render Free: 750 hours/month
- DigitalOcean: $6/month

---

## ⚡ Quick Summary

```bash
# 1. Push to GitHub
git add .
git commit -m "Add Railway config"
git push

# 2. Deploy on Railway.app
# → Connect GitHub → Select repo → Deploy

# 3. Copy Railway URL
# → Like: https://cf-techlab-bot-production.up.railway.app

# 4. Add to Vercel website
# → Paste iframe code with Railway URL

# 5. Deploy Vercel
git add .
git commit -m "Add chatbot"
git push
# → Vercel auto-deploys
```

---

## ✅ Checklist

- [ ] Push chatbot to GitHub
- [ ] Deploy on Railway.app
- [ ] Get Railway public URL
- [ ] Update iframe src with Railway URL
- [ ] Add iframe code to Vercel project
- [ ] Test on local (`vercel dev`)
- [ ] Deploy to Vercel production
- [ ] Test chatbot on live site
- [ ] Check admin dashboard
- [ ] Monitor Railway logs

---

## 🎉 Done!

Your chatbot will be live at:

- **Website:** https://cftechlab.vercel.app
- **Chatbot API:** https://your-railway-url.up.railway.app
- **Admin:** https://your-railway-url.up.railway.app/admin

Users can chat, register with name/mobile/email, and all data saves to database! 🚀
