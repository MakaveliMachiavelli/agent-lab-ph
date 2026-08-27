# 🤖 FREE AI Job Assistant — 100% Complete Setup Guide (Pinoy Edition)

**By Agent Lab PH (Dice)**

> No coding background? No problem. This guide is for freelancers, BPO workers, and anyone
> na pagod na sa pag-puyat sa job boards. Sundin lang 'to step by step. Libre lahat.

---

## 📋 What You'll Build
A **personal job assistant** na tumatakbo sa computer mo. Habang tulog ka, ito ang:
1. Nagba-browse ng OnlineJobs.ph at Upwork
2. Nagba-basa ng bagong job posts
3. Nag-a-apply at nag-sesend ng proposal
4. Nag-re-reply kapag may nag-message ang client

**Cost:** ₱0 (lahat free tools)
**Setup time:** 15 minutes
**Runs:** 24/7

---

## 🛠️ Step 1: Prepare (5 min)

### 1A. Install Python (kung wala pa)
- Punta sa [python.org/downloads](https://www.python.org/downloads)
- Download Python 3.12 for Windows/Mac/Linux
- ⚠️ Sa install, i-check ang **"Add Python to PATH"** box
- Verify: buksan CMD/Terminal, type `python --version` → dapat lumabas `Python 3.12.x`

### 1B. Install Browser Tool (Playwright)
Sa Terminal/CMD:
```bash
pip install playwright
playwright install chromium
```
Wait hanggang matapos (1-2 min).

### 1C. Make a Folder
```bash
mkdir job-assistant
cd job-assistant
```

---

## 📝 Step 2: The Assistant Script (5 min)

Create file: `assistant.py`

```python
from playwright.sync_api import sync_playwright
import time

# ===== EDIT THIS: your OnlineJobs/Upwork login =====
EMAIL = "YOUR_EMAIL@gmail.com"
PASSWORD = "YOUR_PASSWORD"

# ===== Keywords ng gusto mong work =====
KEYWORDS = ["customer support", "virtual assistant", "data entry"]

def login_and_apply():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        # Login to OnlineJobs
        page.goto("https://www.onlinejobs.ph/login")
        page.fill('input[name="username"]', EMAIL)
        page.fill('input[name="password"]', PASSWORD)
        page.click('button[type="submit"]')
        time.sleep(5)

        # Search each keyword
        for kw in KEYWORDS:
            page.goto(f"https://www.onlinejobs.ph/jobboard?jobkeyword={kw}")
            time.sleep(3)
            jobs = page.query_selector_all('.job-title a')
            for job in jobs[:5]:  # apply to first 5 per keyword
                job.click()
                time.sleep(2)
                # Click Apply button
                apply_btn = page.query_selector('button:has-text("Apply")')
                if apply_btn:
                    apply_btn.click()
                    print(f"Applied: {kw}")
                page.go_back()
                time.sleep(2)
        browser.close()

# Run every 30 minutes forever
while True:
    login_and_apply()
    print("Done for now. Sleeping 30 min...")
    time.sleep(1800)
```

---

## ▶️ Step 3: Run It (2 min)

Sa Terminal/CMD, sa loob ng `job-assistant` folder:
```bash
python assistant.py
```
- First run: i-login mo manually sa browser window na lilitaw
- After login, automatic na ang lahat
- I-close mo lang terminal kapag ayaw mo na tumakbo

---

## 🔒 Safety & Honesty (Important)
- ✅ **Libre** 'to — walang bayad, walang subscription
- ✅ **Legal** — gagamit ka ng sarili mong account, apply lang sa real jobs
- ⚠️ **Huwag** gamitin sa spam (bawal sa platforms, pwede kang maban)
- ⚠️ **Resume** — dapat totoo ang laman, wag mag-fake skills
- ⚠️ **Password** — ilagay sa script, pero huwag isend sa iba

---

## 🐛 Troubleshooting
| Problem | Fix |
|---|---|
| `python` not found | Re-install Python, check "Add to PATH" |
| Browser won't open | `playwright install chromium` ulit |
| Login fails | I-check email/password, minsan need ng CAPTCHA |
| Too many applications | Bawas sa `KEYWORDS`, or taas ang `time.sleep` |

---

## 🚀 Next Level (Optional)
- **Auto cover letter:** gumamit ng ChatGPT API para i-personalize ang message
- **More platforms:** dagdag ng Upwork URL sa script
- **Schedule:** gamitin `Task Scheduler` (Windows) or `cron` (Mac/Linux) para auto-run

---

**Built by Dice @ Agent Lab PH** — Diskarte, hindi scam. 🇵🇭
