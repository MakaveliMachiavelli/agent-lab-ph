## Pillar 3: The Free-Tier Loophole Roundup

### Long-form script (10 min, Taglish, conversational)

[SHOW: Title card with glitch/synthwave aesthetic: "₱0 TECH STACK: Paano magpatakbo ng Production Server nang Walang Binabayaran Kahit Piso"]

[SHOW: Host speaking directly to camera. May split-screen sa tabi: AWS pricing calculator na nagpapakita ng $150/month bill vs. Oracle Cloud bill showing $0.00]

Kamusta mga ka-Agent! Ako si Allen, at welcome back sa Agent Lab PH.

Aminin natin: ang pinakamalaking barrier para sa ating mga Pinoy freelancers, devs, at aspiring agency owners kapag gusto nating mag-deploy ng sarili nating automations o AI bots ay yung **infrastructure cost**. 

Mag-deploy ka ng VPS sa AWS o DigitalOcean? Minimum $6 to $20 a month. Gusto mo ng automated workflows sa Zapier o Make.com? Paglampas mo ng 1,000 tasks, sisingilin ka ng $30 to $100 monthly. Magdagdag ka pa ng OpenAI API credits, S3 storage fees, domain, SSL... bago ka pa makakuha ng unang paying client mo, butas na ang bulsa mo ng ₱5,000 hanggang ₱10,000 kada buwan.

Pero what if sabihin ko sa inyo na pwede kang mag-host ng enterprise-grade automation stack—may 24 Gigabytes ng RAM, 4 vCPUs, unmetered automations, zero-latency transcription, Taglish text-to-speech, custom domain na may SSL, at bypass sa CGNAT ng PLDT o Converge—nang **₱0 kada buwan, habangbuhay**?

Hindi ito trial na mage-expire after 30 days. Hindi ito pirated. Ito ang tinatawag nating **The Free-Tier Loophole Stack**. 

Sa video na 'to, iisa-isahin natin at pagdudugtungin ang bawat piyesa ng ₱0 production engine natin. Buksan ang terminal niyo, at tara, i-build natin 'to step-by-step.

---

[SHOW: Full Screen Architecture Diagram showing:
1. Oracle Cloud Infrastructure (Always Free ARM VM: 4 OCPU, 24GB RAM, 200GB SSD)
2. Cloudflare Zero Trust (Cloudflared Tunnel + R2 Storage 10GB + Free DNS/SSL)
3. Docker Host: n8n Workflow Engine + PostgreSQL + edge-tts microservice
4. External Free APIs: Groq Cloud (Whisper-large-v3) + Telegram Bot API
5. GitHub: Pages (Landing Page) + Actions (CI/CD)]

[SHOW: Screen recording of browser entering Oracle Cloud Console]

Simulan natin sa pinaka-foundation: **The Compute Layer**.

Karamihan sa atin akala ang free tier ng cloud providers ay puro 1 vCPU at 512MB RAM lang na nagka-crash kapag nag-run ka ng npm build. Pero si **Oracle Cloud Infrastructure (OCI)** may tinatawag na **Always Free Tier**. 

Bibigyan ka ni Oracle ng:
- **Ampere A1 ARM Compute**: Up to 4 OCPUs at **24 GB ng RAM** (pwede mong i-allocate sa isang giant VM o hatiin sa 2-4 instances).
- **200 GB Block Volume Storage**.
- **10 TB of outbound data transfer per month**.

[SHOW: Terminal running SSH connection to Oracle VM instance]

```bash
# SSH sa ating Always Free Oracle Ubuntu ARM instance
ssh -i ~/.ssh/oracle_arm_key ubuntu@129.150.x.x

# Check natin ang specs gamit ang htop at fastfetch
lscpu | grep "Model name\|CPU(s):"
free -h
```

[SHOW: Terminal screen highlighting 4 Cores and 24GB RAM available]

Kita niyo yan? 24 Gigabytes ng RAM. Libre. Forever. Dito tatakbo ang buong backend operating system natin.

---

[SHOW: Screen switch to Cloudflare Dashboard]

Pangalawa: **The Ingress and Storage Layer: Cloudflare**.

Kapag nagho-host ka sa bahay o kahit sa cloud VM, kadalasan problema ng mga Pinoy devs ang **CGNAT** (Carrier-Grade NAT) ng Converge, PLDT, o Globe. Hindi ka makapag-port forward nang direkta, o kaya naman exposed ang public IP mo sa DDoS attacks.

Ang solution? **Cloudflare Tunnels (cloudflared)**.

[SHOW: Code editor with `docker-compose.yml` for Cloudflare Tunnel and n8n]

Hindi natin kailangang mag-open ng port 80 o 443 sa firewall. Magpapatakbo lang tayo ng lightweight daemon sa loob ng Oracle box natin. Si Cloudflare na ang bahala sa:
1. Libreng SSL/TLS encryption.
2. DDoS protection.
3. Automatic DNS routing papunta sa subdomain mo like `automation.yourdomain.com`.

At para sa file storage—kung magse-save ka ng audio messages, generated PDFs, o client backups—huwag kang mag-AWS S3. Gamitin mo ang **Cloudflare R2**. 
May **10 GB of free storage per month** si R2, and best of all: **ZERO egress fees**. Kahit mag-download ang client mo ng 1,000 files araw-araw, walang hidden bandwidth bill.

---

[SHOW: Browser showing n8n workflow canvas]

Pangatlo: **The Brain — Self-Hosted n8n**.

Si Zapier at Make.com, kada execution ng step, binibilang. Sa n8n, dahil self-hosted natin ito sa ating 24GB Oracle instance via Docker Compose, **UNLIMITED ang workflow executions**. 100,000 executions a day? Go lang.

Tignan natin ang ating `docker-compose.yml` setup:

[SHOW: VS Code showing full Docker Compose file]

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    restart: always
    environment:
      - POSTGRES_USER=n8n_admin
      - POSTGRES_PASSWORD=SuperSecretPinoyPassword2026
      - POSTGRES_DB=n8n_db
    volumes:
      - postgres_data:/var/lib/postgresql/data

  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    restart: always
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=n8n_db
      - DB_POSTGRESDB_USER=n8n_admin
      - DB_POSTGRESDB_PASSWORD=SuperSecretPinoyPassword2026
      - N8N_HOST=automation.agentlab.ph
      - WEBHOOK_URL=https://automation.agentlab.ph/
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - postgres

  edge-tts:
    image: ghcr.io/travisvn/edge-tts-api:latest
    restart: always
    ports:
      - "5050:5050"

volumes:
  postgres_data:
  n8n_data:
```

[SHOW: Terminal running `docker compose up -d` with all green checks]

Isang `docker compose up -d` lang, running na ang automation powerhouse natin.

---

[SHOW: Graphic highlighting Telegram logo and Smartphone mockup]

Pang-apat: **The Free UI / Frontend — Telegram Bot API**.

Bakit ka pa gagawa ng custom mobile app o magbabayad ng WhatsApp Business API (na may bayad per conversation window) kung pwede mong gamitin ang **Telegram**?

Ang Telegram Bot API ay:
- 100% Free.
- Walang conversation limit.
- Supports voice notes, images, interactive buttons, custom keyboards, and documents.
- May instant webhook support diretso sa n8n.

Ito ang magiging instant CRM at command center ng business mo at ng mga clients mo.

---

[SHOW: Terminal and Browser testing Groq and edge-tts]

Panglima: **Free Multimodal AI Stack — Groq Whisper + edge-tts**.

Paano kung magpadala ng Taglish voice message si client?
*"Kuya Allen, paki-follow up naman yung quotation para kay Doc Santos kahapon."*

Kapag pinadaan mo yan sa normal na paid APIs, gagastos ka. Pero dito sa stack natin:
1. **Groq Cloud Free Tier**: Ginagamit natin ang `whisper-large-v3` running on LPU (Language Processing Units). 0.3 seconds transcription time para sa 30-second voice note, perfectly accurate sa Taglish, at may generous free daily tier na libo-libong requests bawat araw.
2. **edge-tts**: Ito ang pinaka-underrated open-source gem. Ginagamit nito ang natural neural voices ng Microsoft Edge. Libreng text-to-speech na may Tagalog voice (`fil-PH-AngeloNeural` o `fil-PH-BlessicaNeural`). Walang API key, self-hosted sa container natin!

[SHOW: Playing an audio sample from edge-tts: "Magandang araw po! Na-save na po ang inyong inquiry sa ating database."]

Solid, di ba? Natural pakinggan, walang bayad sa ElevenLabs.

---

[SHOW: GitHub Repo and GitHub Pages site]

Pang-anim: **The Public Presence — GitHub Pages + Actions**.

Saan nakalagay ang landing page mo para kumuha ng leads? Sa **GitHub Pages**. Libreng static hosting na naka-link sa custom domain mo via Cloudflare.

Saan nakalagay ang backup ng mga n8n workflows at Docker scripts mo? Sa private GitHub repository na may automated GitHub Actions workflow para mag-CI/CD sync sa Oracle server mo tuwing mag-git push ka.

---

[SHOW: Summary Diagram with all tools connected]

Pagsama-samahin natin:
- **Oracle Cloud**: 24GB Server (₱0)
- **Cloudflare**: Ingress Tunnel + R2 Storage + SSL (₱0)
- **n8n + Postgres**: Unlimited Workflows (₱0)
- **Telegram**: Client & Admin Frontend (₱0)
- **Groq Whisper + edge-tts**: Voice AI Engine (₱0)
- **GitHub Pages**: High-speed Landing Page (₱0)

**Total Monthly Operating Cost: ₱0.00.**

Ito ang blueprint. Walang dahilan para sabihing *"Wala akong budget mag-start."* Ang kailangan mo lang ay ang diskarte at tamang architectural knowledge para pagtagpi-tagpiin ang mga tools na ito.

Kung gusto niyo ng full copy-paste `docker-compose.yml` and setup scripts, i-check niyo ang open-source GitHub repo sa description sa ibaba. I-star niyo na rin para updated kayo!

Sa susunod nating video sa Pillar 4, gagamitin natin itong eksaktong stack para mag-build ng isang fully functional AI Automation Agency product na pwede ninyong ibenta sa local business owners bukas na bukas din.

Kita-kits sa next video! Like, subscribe, and happy building, mga ka-Agent!

---

### 5 Short-form hooks

#### Hook 1: The AWS Killer
- **Hook Title:** Paano magka-24GB Cloud Server nang ₱0?
- **30-sec Taglish Script:**
  [SHOW: Hold up phone with AWS $200 bill, then shake head]
  "Nagbabayad ka pa rin ba sa AWS o DigitalOcean ng ₱1,500 buwan-buwan para lang sa 1GB RAM na VPS? Stop it, bossing! Alam mo bang may Always Free Tier si Oracle Cloud na nagbibigay ng 4 Cores at 24GB ng RAM nang walang expiration? Yes, 24GB! Kasya ang 20 Docker containers, database, at n8n automation mo nang zero pesos forever. Link in bio para sa step-by-step setup guide!"
- **Caption Line:** Itigil na ang paglustay sa cloud bills! Setup your 24GB free cloud server today. 🚀

#### Hook 2: Bypassing CGNAT
- **Hook Title:** No Port Forwarding? No Problem!
- **30-sec Taglish Script:**
  [SHOW: Quick diagram of PLDT/Converge router blocking incoming traffic]
  "Naka-Converge o PLDT ka ba at hindi makapag-host ng server sa bahay dahil sa CGNAT? Huwag ka nang magmakaawa sa ISP mo para sa Static IP. Gamitin mo ang Cloudflare Tunnels! Isang line of command lang sa terminal, may secure https connection ka na diretso sa local machine mo nang walang binubuksan na ports sa router. Libre pa ang SSL at DDoS protection!"
- **Caption Line:** Paano i-bypass ang CGNAT ng telco gamit ang Cloudflare Tunnels para sa ₱0 hosting! 🌐

#### Hook 3: Zero-Cost Voice AI
- **Hook Title:** Libreng Tagalog AI Voice & Audio Transcriber
- **30-sec Taglish Script:**
  [SHOW: Playing voice message on Telegram -> Instant Tagalog voice response]
  "Gusto mong gumawa ng AI customer service bot na marunong mag-Tagalog pero namamahalan ka sa ElevenLabs at OpenAI? Gamitin mo ang combination na 'to: Groq Whisper para sa 0.3-second Taglish transcription, plus edge-tts para sa natural Pinoy AI voice. Parehong ₱0 API cost! I-connect mo sa Telegram bot mo via n8n, tapos ang laban."
- **Caption Line:** Tagalog Voice AI nang walang API bill? Groq + edge-tts ang secret sauce! 🎙️

#### Hook 4: The Zapier Alternative
- **Hook Title:** Unlimited Automations without Zapier Bills
- **30-sec Taglish Script:**
  [SHOW: Zapier pricing page highlighting the $299 plan -> cut to n8n workflow canvas]
  "1,000 tasks lang sa Zapier, sisingilin ka na agad ng mahigit ₱1,500? Bakit ka magpapa-holdap kung pwede kang mag-self-host ng n8n? Dahil open-source ito, wala kang task limits. 100k tasks, 1 million webhooks, magdamagang data scraping—walang dagdag bayad. I-deploy mo sa libreng Oracle VM, may enterprise automation suite ka na!"
- **Caption Line:** Bye-bye Zapier subscription! Unlimited free automation with self-hosted n8n. ⚡

#### Hook 5: The Complete ₱0 Tech Stack
- **Hook Title:** The Ultimate ₱0 Pinoy Dev Tech Stack
- **30-sec Taglish Script:**
  [SHOW: Fast-paced montage of Oracle, Cloudflare, n8n, Telegram, and GitHub logos]
  "Eto ang pinaka-malupit na ₱0 tech stack para sa Pinoy freelancers ngayong 2026: Compute galing kay Oracle, Ingress at DNS galing kay Cloudflare, Automations via n8n, Database sa PostgreSQL, Voice AI via Groq at edge-tts, at Chat UI gamit ang Telegram Bot API. Buong production tech stack para sa business mo: Zero pesos. Watch full tutorial sa channel!"
- **Caption Line:** Ang kumpletong ₱0 cloud infrastructure para sa automation business mo. 💻

---

### Caption

Gusto mo bang magpatakbo ng production-grade automation server nang hindi nagbabayad ng kahit isang piso buwan-buwan? Sa video na ito, i-chain natin ang pinakamalulupit na Always-Free cloud tiers para makabuo ng isang ₱0 tech stack: 24GB Oracle ARM Compute, Cloudflare Zero Trust Tunnels, unlimited self-hosted n8n, Groq Whisper transcription, at Tagalog edge-tts! 

#FreeTierCloud #PinoyDev #n8nAutomation

---
---

## Pillar 4: Build an AI Agency for ₱0 with n8n

### Long-form script (10 min, Taglish, conversational)

[SHOW: Host sitting at desk with laptop. Background neon light says "AGENT LAB PH".]

[SHOW: Screen recording of a local business Facebook Page / Telegram with a customer asking questions in Tagalog at 2:30 AM, instantly receiving an accurate voice note reply with an invoice PDF attached.]

Alas-dos y medya ng madaling araw. May nag-inquire sa isang aesthetic clinic sa QC o dental clinic sa Cebu. 

*"Hi doc, magkano po ang dental implants and pwede ba installment? Tsaka pwede ba mag-book this Saturday 3pm?"*

Karamihan sa mga small businesses sa Pilipinas—mga clinics, real estate brokers, accounting firms, car rental services, pati high-volume online sellers—walang 24/7 staff na sasagot diyan. Pag gising ng receptionist ng 8:00 AM, lumipat na sa ibang clinic yung customer. Lost revenue.

Ngayon, kung lalapitan mo sila at sasabihin mo: *"Sir/Ma'am, gawan ko kayo ng custom AI system gamit ang $300/month custom software subscription,"* tatanggihan ka nila. Masyadong mahal, masyadong complex.

Pero what if ikaw ang mag-offer ng **Done-For-You 24/7 AI Receptionist and Operations Agent** na tumatakbo sa ₱0 infrastructure na binuild natin sa Pillar 3? 

Walang overhead cost sa server mo, pero pwede mong singilin si client ng **₱15,000 to ₱35,000 setup fee**, plus **₱3,000 to ₱8,000 monthly retainer** para sa maintenance at continuous improvements.

Ako si Allen ng Agent Lab PH, at sa video na 'to, bubuuin natin ang core product ng iyong AI Automation Agency gamit ang n8n, Telegram, Groq, at Google Sheets. Tara!

---

[SHOW: n8n Canvas Architecture Overview diagram showing 4 core nodes:
1. Telegram Trigger (Text & Voice Note Ingestion)
2. Groq Whisper / Audio Parser Sub-workflow
3. AI Agent Node (LLM System Prompt tailored for PH B2B + Tool Calling)
4. Operations Sub-flows: Google Sheets CRM + Calendar Booker + edge-tts Voice Reply + Admin Alert]

[SHOW: n8n interface on browser]

I-breakdown natin ang architecture ng ating B2B AI Agent product. May apat itong major components:

1. **The Ingestion Layer**: Tumatanggap ng text o voice messages mula sa customer.
2. **The Intelligence Layer**: Isang AI Agent na may memory at business context na nakakaintindi ng Taglish at local nuance.
3. **The Action Tools**: Kayang mag-check ng available slots sa Google Calendar, mag-save ng lead data sa Google Sheets, at mag-compute ng presyo.
4. **The Response Synthesizer**: Sasagot pabalik via text o voice note gamit ang Pinoy voice.

---

[SHOW: Screen zoom into n8n Telegram Trigger Node & Groq Transcription Node]

**Step 1: Ingestion & Voice Transcription**

Una, magse-set up tayo ng Telegram Trigger node sa n8n. 

Kapag text ang pinadala, diretso agad sa AI Agent. Pero kapag boses (voice note) ang pinadala ni customer:
1. Kukunin ng n8n ang `file_id` mula sa Telegram.
2. Ida-download ang `.oga` voice file via HTTP Request node.
3. Ipapadala natin ito sa **Groq Whisper API**.

[SHOW: HTTP Request node configuration in n8n for Groq Whisper]

```json
{
  "method": "POST",
  "url": "https://api.groq.com/openai/v1/audio/transcriptions",
  "headers": {
    "Authorization": "Bearer ={{ $env.GROQ_API_KEY }}",
    "Content-Type": "multipart/form-data"
  },
  "body": {
    "file": "={{ $binary.data }}",
    "model": "whisper-large-v3",
    "temperature": 0.0,
    "response_format": "json",
    "language": "tl"
  }
}
```

In less than 500 milliseconds, yung Taglish voice note ni customer, converted na into clean text.

---

[SHOW: Screen zoom into n8n AI Agent Node and System Prompt]

**Step 2: The Pinoy Business Context Prompt**

Dito nagkakamali ang karamihan ng mga AI beginners: gumagamit sila ng generic English prompts na tunog robot o customer service sa US.

Sa local PH market, kailangan **natural, magalang pero authoritative, at may tamang Taglish tone**.

Tignan natin ang system prompt na ilalagay natin sa AI Agent node:

[SHOW: Code block of the System Prompt]

```markdown
Ikaw si "Maria", ang friendly at professional digital assistant ng SmileCare Dental Clinic BGC.
Tungkulin mong sagutin ang inquiries ng mga pasyente, magbigay ng price estimates, at mag-schedule ng appointments.

MGA PANUNTUNAN SA PAKIKIPAG-USAP:
1. Tone: Natural Taglish (conversational Pinoy professional). Gumamit ng "po" at "opo" nang natural pero huwag OA.
2. Knowledge Base & Pricing:
   - Consultation: ₱500 (Free if proceed with procedure)
   - Teeth Cleaning (Prophylaxis): ₱1,500 - ₱2,500
   - Dental Implants: Starts at ₱45,000 (Available via 0% installment up to 12 months)
3. Action Guidelines:
   - Bago mag-book, laging kunin ang: Buong Pangalan, Contact Number, at Preferred Date/Time.
   - Kapag kumpleto na ang details, tawagin ang tool na `book_appointment` at `save_lead_to_sheets`.
   - Kung emergency (e.g., severe toothache o bleeding), payuhan silang pumunta agad sa clinic emergency hotline: 0917-XXX-XXXX.
```

[SHOW: Adding Tools to the AI Agent Node in n8n: Google Sheets Tool and Google Calendar Tool]

Ikinabit natin sa AI Agent ang dalawang tools:
- **Google Sheets Tool**: Nag-a-append ng Name, Phone, Inquiry Type, at Lead Score sa CRM spreadsheet ng clinic owner.
- **Calendar Check Tool**: Nagbabasa kung available ang specific time slot sa Google Calendar ng doktor para maiwasan ang double booking.

---

[SHOW: Live demo testing on Telegram]

Subukan natin live!

[SHOW: Host typing in Telegram on phone: "Hi doc! Magkano po magpa-cleaning and available ba kayo bukas ng 2pm? Ako nga pala si Mark Ramos, 09181234567."]

[SHOW: Fast forward 2 seconds. Telegram receives response]

Tignan niyo ang sagot:
> *"Hello Mark! Salamat sa pag-inquire sa SmileCare Dental BGC. 😊 Ang ating Basic to Deep Prophylaxis (Cleaning) ay nagre-range mula ₱1,500 hanggang ₱2,500 depende sa condition ng teeth.*
> 
> *Chineck ko ang calendar ni Doc, and YES, available po ang 2:00 PM slot bukas, Tuesday! Na-reserve ko na po provisional slot para sa'yo under 09181234567. May confirmation text din pong ipapadala ang clinic staff. May iba ka pa bang gustong itanong, Mark?"*

[SHOW: Screen switch to Google Sheets: Instant new row created with Mark Ramos's details, inquiry summary, and status 'Booked']

Sabay pasok ng bagong row sa Google Sheets ng clinic owner nang real time!

---

[SHOW: Voice Generation Node workflow in n8n]

**Step 3: Taglish Voice Message Reply (Optional Up-sell Feature)**

Kung gusto mo talagang mapabilib ang client mo, i-enable natin ang Voice Reply feature.

Kapag nagpadala ng voice note ang pasyente, imbes na text lang ang ibalik, ipapasa ng n8n ang text response ng AI kay `edge-tts` (na tumatakbo sa Oracle container natin), at ibabalik sa Telegram as an actual audio voice message na nagsasalita ng Tagalog!

[SHOW: Audio playing from Telegram bot with smooth Filipina AI voice confirming the appointment]

Isipin mo ang reaksyon ng dental clinic owner o real estate broker kapag pinakita mo 'to sa sales pitch mo. Sasabihin nila: *"Pang-enterprise to ah! Magkano aabutin nito?"*

---

[SHOW: Business model slide / Pricing Breakdown]

**Step 4: Ang B2B2B Business Model — Paano Ito Pagkakakitaan?**

Pag-usapan natin ang negosyo. Paano mo 'to ibebenta sa local Philippine businesses?

Huwag mong ibenta bilang *"n8n workflow with LLM chain"*. Walang pakialam ang business owner sa tech stack. 
Ibenta mo ito bilang **"24/7 Inbound Lead & Booking Automation System"**.

Narito ang recommended pricing framework para sa PH market:

1. **Setup Fee (One-Time)**: **₱15,000 – ₱30,000**
   - Kasama ang custom workflow setup, prompt tailoring sa business nila, integration sa Google Sheets/Calendar/Telegram, at 2 rounds of revisions.
2. **Monthly Maintenance Retainer**: **₱3,000 – ₱7,500 / month**
   - Kasama ang hosting sa iyong server infrastructure, server monitoring, prompt optimization base sa customer logs, at basic support.

Kung mayroon ka lang **10 active small business clients** sa retainer mo:
`10 clients × ₱5,000/mo = ₱50,000 / month passive recurring revenue`.

Magkano ang server costs mo? **₱0.00** sa Oracle Always Free Tier. Ang tanging babayaran mo lang ay minimal API tokens kung lumagpas ka sa free tier ng Groq o Gemini (na madalas less than $2 a month total).

---

[SHOW: Host speaking to camera with step-by-step action plan on screen]

Ito ang kapangyarihan ng pagiging isang **AI Automation Agency (AAA)** sa Pilipinas. Hindi mo kailangang mag-code ng sarili mong neural network mula sa simula. Ang value mo ay nasa pagiging arkitekto: kukunin mo ang free open-source tools at pagdudugtungin mo para lutasin ang totoong problema ng mga negosyo sa paligid mo.

Nasa description ang export ng buong n8n workflow JSON template na ito. I-import niyo lang sa inyong n8n instance, lagay ang credentials niyo, at ready to deploy na kayo!

Kung may tanong kayo sa pag-configure, drop a comment sa baba. Sa susunod na Pillar 5, ituturo ko kung paano gamitin ang "Building in Public" para makakuha ng paying clients nang hindi nagbabayad ng ads.

Subscribe to Agent Lab PH, i-share sa fellow Pinoy devs, and let's automate the Philippines!

---

### 5 Short-form hooks

#### Hook 1: Local Clinic Automation Pitch
- **Hook Title:** Paano kumita ng ₱25k sa pag-automate ng Dental Clinics
- **30-sec Taglish Script:**
  [SHOW: Dentist clinic facade -> Split screen with smartphone receiving appointments automatically]
  "Alam mo ba kung bakit laging stressed ang mga clinic owners sa Pilipinas? Kasi 50% ng inquiries sa Facebook at Viber, pumapasok sa gabi kung kailan tulog na ang staff. I-pitch mo sa kanila 'to: Isang 24/7 AI Receptionist sa Telegram na marunong mag-Taglish, sumasagot sa pricing, at nagbu-book sa Google Calendar. ₱20,000 setup fee per clinic. Panoorin ang full n8n blueprint sa aming YouTube channel!"
- **Caption Line:** Paano mag-benta ng AI Receptionist sa local clinics para sa ₱25,000 setup fee! 🦷🤖

#### Hook 2: The Voice Note Customer
- **Hook Title:** AI Bot na sumasagot ng Voice Note sa Taglish!
- **30-sec Taglish Script:**
  [SHOW: Screen recording: Sending voice message "Doc, available ba bukas?" -> Bot replies with voice note instantly]
  "Mga Pinoy, tamad mag-type, mahilig mag-voice note! Kung ang customer bot mo puro text lang ang kaya, maiiwan ka. Sa video na 'to, ginawa nating multimodal ang n8n automation natin: Pinapakinggan ang voice message via Groq Whisper, tapos sasagot pabalik gamit ang Tagalog AI voice via edge-tts. Production ready, ₱0 host cost. Full tutorial out now!"
- **Caption Line:** Ang Pinoy AI bot na marunong makinig at sumagot ng voice notes! 🎧🇵🇭

#### Hook 3: Stop Selling Hours, Sell Retainers
- **Hook Title:** Freelancer ka pa rin ba per hour? Switch to AI Retainers!
- **30-sec Taglish Script:**
  [SHOW: Clock ticking vs Monthly recurring invoice notification]
  "Kung freelancer ka at sumisingil ka per hour, may ceiling ang kita mo. Pero kapag nag-build ka ng AI workflow sa n8n para sa isang small business—tulad ng automated lead qualification—pwede kang sumingil ng ₱5,000 monthly retainer kada client para lang panatilihing running ang bot. 10 clients lang, may ₱50k/month ka na habang natutulog. Panoorin kung paano!"
- **Caption Line:** Shift from hourly freelancing to monthly AI automation retainers! 📈

#### Hook 4: Google Sheets as a Free CRM
- **Hook Title:** Huwag mag-bayad ng mamahaling CRM, gamitin ang n8n + Sheets!
- **30-sec Taglish Script:**
  [SHOW: HubSpot $500 pricing -> Cut to auto-updating Google Sheets via n8n]
  "Karamihan sa mga local businesses dito sa atin, nalulula sa HubSpot o Salesforce. Ayaw nila ng complicated dashboard. Ang gusto nila: Google Sheets na nag-a-update mag-isa tuwing may bagong buyer o pasyente. Gamit ang libreng n8n workflow na 'to, automated na ang lead scoring at booking diretso sa spreadsheet ni bossing nang walang binabayarang CRM subscription!"
- **Caption Line:** Libreng CRM automation para sa micro-businesses gamit ang n8n at Google Sheets. 📊

#### Hook 5: The B2B Agency Blueprint
- **Hook Title:** Magtayo ng sariling AI Agency ngayong 2026
- **30-sec Taglish Script:**
  [SHOW: Step 1: Oracle VM -> Step 2: n8n Workflow -> Step 3: Local Client Contract]
  "Paano magsimula ng AI Agency sa Pilipinas nang walang puhunan? Step 1: Kunin ang Always Free Oracle Cloud Server. Step 2: I-install ang pre-built n8n templates namin for Telegram lead bots. Step 3: I-alok sa mga sari-sari wholesale stores, real estate agents, at private clinics sa city mo. Zero overhead, pure profit. Panoorin ang step-by-step masterclass sa channel!"
- **Caption Line:** Step-by-step blueprint para magtayo ng sarili mong AI Automation Agency sa Pinas! 🚀

---

### Caption

Gusto mong magtayo ng sarili mong AI Automation Agency (AAA) dito sa Pilipinas pero wala kang malaking capital? Sa tutorial na ito, bubuuin natin ang isang production-grade AI Receptionist at Lead Qualification workflow gamit ang self-hosted n8n, Groq Whisper (Taglish voice transcription), at Google Sheets CRM na tumatakbo sa ating ₱0 Oracle server. Kasama na rin ang B2B pricing strategy kung paano ito ibenta sa local business owners!

#AIAgency #n8nPH #PinoyFreelancer

---
---

## Pillar 5: Ship in Public / The Funnel

### Long-form script (10 min, Taglish, conversational)

[SHOW: Host looking directly at camera. Sa background, dashboard ng YouTube Studio, GitHub Traffic graph na may spike sa Clones/Stars, at Telegram notification inbox na may client inquiries.]

Isang malaking misconception ng mga developers at tech freelancers: *"Bumuo ka lang ng magandang software, kusa nang darating ang mga customer."*

Newsflash: **Hindi totoo yan.** 

Kahit ikaw pa ang pinakamagaling mag-setup ng n8n workflows sa buong Luzon, Visayas, at Mindanao, kung walang nakakaalam na nage-exist ka, zero ang benta mo. 

Pero paano ka makakakuha ng clients kung:
- Wala kang budget mag-Facebook o Google Ads?
- Ayaw mong mag-cold message o mag-spam sa LinkedIn at Upwork kung saan 500 kayong nag-aagawan sa isang $5/hour job post?
- At nagsisimula ka sa **zero audience** at zero followers?

Ang sagot ay isang proven strategy: **Build in Public, Open Source the Template, and Turn Your Content into a Client Acquisition Funnel.**

Sa video na 'to, ibubunyag ko sa inyo ang eksaktong funnel kung bakit ang **Agent Lab PH channel mismo ang aming pinaka-epektibong sales machine**—at paano niyo kokopyahin ang eksaktong playbook na ito para sa sarili ninyong freelance career o agency.

---

[SHOW: Full Screen Graphic: The 4-Stage Developer Flywheel
1. TOP OF FUNNEL (Awareness): Free YouTube & Short-Form Tutorials solving specific pain points
2. MIDDLE OF FUNNEL (Trust & Proof): Open Source GitHub Repositories (Stars, Code, Dockerfiles)
3. BOTTOM OF FUNNEL (Conversion): Free Community & Inbound Discovery Form
4. MONETIZATION (Retainer/Consulting): Custom Deployment for Non-Technical Business Owners]

[SHOW: Host explaining the Flywheel on a digital whiteboard]

I-analyze natin ang mechanics ng **Developer Flywheel**. Bakit ito gumagana nang 10x mas mabilis kaysa sa traditional cold outreach?

Kapag nag-cold call ka sa isang business owner, ikaw ang nagmamakaawa. Low leverage.
Pero kapag nakita ng business owner ang YouTube tutorial mo kung saan dine-demo mo kung paano lutasin ang eksaktong problema nila gamit ang n8n at Cloudflare, ang tingin nila sa'yo ay **Subject Matter Expert**. Inbound sila lalapit sa'yo.

Tignan natin ang bawat step ng funnel:

---

[SHOW: Screen recording ng GitHub repo ng Agent Lab PH na may malinis na README.md, architecture diagram, at green "Deploy" instructions]

**Stage 1: The Open Source Social Proof Engine (GitHub)**

Huwag mong itago ang code mo. Ibigay mo ang workflow templates nang libre sa GitHub. 

Bakit?
1. **GitHub Stars and Forks are Public Social Proof**: Kapag may 100 stars o 50 forks ang repository mo, instant validation ito sa technical skills mo. Pwede mong ilagay sa portfolio o proposal mo.
2. **The "Do-It-Yourself vs. Do-It-For-Me" Split**: 
   - 80% ng manonood sa'yo ay mga kapwa devs o technical students na gustong matuto. I-star nila ang repo mo at magiging advocates mo sa social media.
   - 20% ng manonood sa'yo ay **mga business owners, clinic managers, o busy freelancers**. Titignan nila ang 40-minute tutorial mo at ang sasabihin nila: *"Naintindihan ko yung value, pero wala akong 10 oras para mag-aral ng Docker at terminal commands. Babayaran ko na lang si Allen para i-setup 'to sa server ko."*

Yun ang magic! Ang tutorial ang nagpapatunay na kaya mong gawin. Ang service mo ang nagtitipid ng oras nila.

---

[SHOW: Screen showing YouTube Studio Analytics & Traffic Sources]

**Stage 2: Metrics That Actually Matter (Ignore the Vanity)**

Kapag nagsisimula ka, huwag kang ma-depress kung ang video mo ay may 300 views lang. 

Sa agency funnel, **hindi views ang sukatan ng tagumpay; CONVERSION INTENT ang sukatan.**

[SHOW: Comparison Table on Screen:
- Lifestyle Influencer: 100,000 views = $50 AdSense revenue = 0 client leads
- Tech B2B Channel: 350 views = 3 qualified business owners = 2 booked discovery calls = ₱50,000 agency setup project]

Ang 300 views mula sa mga target na negosyante sa Pilipinas na naghahanap ng *"clinic automation"* o *"free server hosting"* ay 100x mas valuable kaysa sa 1,000,000 views ng viral dance video.

Ano ang mga metrics na dapat mong bantayan?
1. **GitHub Clones & Template Downloads**: Sinasabi nito kung gaano ka-actionable ang tinuro mo.
2. **Click-Through Rate sa Description Link**: Ilan ang nagki-click papunta sa Telegram Group o Contact Form mo.
3. **Inbound Inquiries**: Ilan ang nagtatanong ng *"Boss, tumatanggap ka ba ng custom setup para sa trucking/clinic/store namin?"*

---

[SHOW: Step-by-step screen recording on setting up an automated Inbound Discovery Form using GitHub Pages + n8n + Telegram Alert]

**Stage 3: Setting Up Your Frictionless Intake Funnel**

Paano mo tatanggapin ang leads nang hindi nagbabayad ng CRM tool?

[SHOW: Workflow diagram in n8n]

1. **The Free Landing Page**: Isang single-page static site sa GitHub Pages (e.g., `agency.yourname.dev`) na may simpleng form:
   - Pangalan & Business Name
   - Anong manual process ang gustong i-automate?
   - Estimated monthly budget (₱15k-₱30k, ₱30k-₱50k, ₱50k+)
2. **The n8n Webhook**: Kapag nag-submit si lead sa form:
   - Sinasala ng n8n ang budget at readiness.
   - Nagpapadala ng instant notification sa private Telegram account mo:
     *"🚨 BAGONG LEAD: Doc Santos Dental Clinic (Budget: ₱30k). Click here to call."*
3. **The 15-Minute Discovery Call**: Makikipag-meet ka sa Google Meet hindi para magbenta nang agresibo, kundi para magtanong tungkol sa bottlenecks ng operasyon nila.

---

[SHOW: Checklist on screen: "How to Start Today with 0 Audience"]

**Stage 4: Paano Magsimula Ngayong Linggo (The 7-Day Sprint)**

Kung wala ka pang audience ngayon, eto ang 4-step execution plan mo para sa darating na weekend:

- **Day 1-2**: Pumili ng isang specific problem (Halimbawa: *"Auto-reply and Google Sheets lead capture para sa mga real estate agents sa Facebook"*). I-build ang workflow sa n8n.
- **Day 3**: I-upload ang code at clean setup instructions sa isang public GitHub repository.
- **Day 4-5**: I-record ang screen mo habang tinuturo kung paano ito i-deploy step-by-step. Maging tapat, natural na Taglish, at ipakita pati ang mga errors at paano ito i-fix.
- **Day 6**: I-post ang video sa YouTube, at i-cut ang 30-second highlight clips para sa TikTok, Facebook Reels, at YouTube Shorts na may call-to-action: *"Full tutorial and free code in bio."*
- **Day 7**: I-share ang GitHub repo link sa mga relevant Pinoy tech communities (tulad ng Reddit r/PinoyProgrammer o local developer Facebook groups) nang may kasamang helpful explanation—huwag mag-spam.

---

[SHOW: Host speaking with inspiring, grounded tone]

Mga ka-Agent, tapos na ang panahon kung saan kailangan mong maghintay ng approval mula sa mga corporate employers para mapatunayan ang galing mo. 

Hawak mo na ang free cloud tools. Hawak mo na ang automation engine. At hawak mo na ang distribution platforms tulad ng YouTube at GitHub para ipakita ang kakayahan mo sa buong mundo.

Ang channel na 'to, ang Agent Lab PH, ay patunay na sa pamamagitan ng pagbibigay ng value at pagtuturo nang libre, kusa mong maa-attract ang tamang opportunities at paying clients.

Lahat ng templates, scripts, at intake funnels na pinag-usapan natin sa video na 'to ay nasa description sa ibaba. I-clone niyo, i-tweak niyo, at i-deploy niyo para sa sarili ninyong business.

Huwag kalimutang mag-subscribe, i-hit ang notification bell, at mag-iwan ng comment kung anong industry ang gusto ninyong i-automate natin sa next episode.

Muli, ako si Allen. Mag-build tayo sa publiko, magtulungan tayo, at tara, i-level up natin ang Pinoy tech community! Maraming salamat!

---

### 5 Short-form hooks

#### Hook 1: Stop Applying on Upwork
- **Hook Title:** Wag ka nang makipagsiksikan sa Upwork!
- **30-sec Taglish Script:**
  [SHOW: Upwork screen with "50+ proposals sent" -> Swipe left to YouTube & GitHub analytics]
  "Pagod ka na bang mag-send ng 50 proposals sa Upwork para lang baratin ng $3 per hour? Subukan mo ang 'Ship in Public' method. Gumawa ka ng 10-minute video na nagpapakita kung paano ayusin ang automation ng isang clinic o retail store gamit ang n8n. I-share mo ang code sa GitHub. Yung mga business owners na manonood, sila mismo ang mag-i-inbox sa'yo para magpa-hire. Panoorin ang full breakdown!"
- **Caption Line:** Paano kumuha ng high-paying automation clients nang hindi nag-a-Upwork! 🎯

#### Hook 2: The Open Source Secret
- **Hook Title:** Bakit ko pinamimigay ang code ko nang Libre?
- **30-sec Taglish Script:**
  [SHOW: Code on screen -> Download counter going up -> Invoice notification]
  "Sinasabihan ako ng ibang devs: 'Bakit mo pinamimigay ng libre yung n8n templates mo sa YouTube? Baka nakawin lang ng iba!' Ang hindi nila alam, ang open-source content ang pinakamalakas kong sales funnel. Ang mga kapwa devs, gagamitin ang code. Pero ang mga business owners na walang time mag-code, ako ang babayaran ng ₱30k para mag-deploy nito sa kanila. Free code = Paid clients!"
- **Caption Line:** Bakit ang pagbibigay ng libreng code ang pinakamabilis na paraan para makakuha ng agency clients! 💡

#### Hook 3: Zero Views to Paying Client
- **Hook Title:** 200 Views lang pero kumita ng ₱40,000?
- **30-sec Taglish Script:**
  [SHOW: YouTube analytics showing 214 views -> Zoom in to 2 contract signatures]
  "Hindi mo kailangan ng 1 milyong subscribers para kumita sa YouTube. Sa B2B tech niche, kailangan mo lang ng tamang 200 views. Kung ang 200 views na yan ay mga local real estate brokers at accounting firm owners na naghahanap ng solusyon sa tambak nilang paperworks, 2 clients lang ang mag-convert, may ₱40,000 ka na. Stop chasing vanity views, start building targeted funnels!"
- **Caption Line:** Bakit mas mahalaga ang qualified B2B views kaysa sa viral content! 📊💰

#### Hook 4: The 7-Day Freelancer Challenge
- **Hook Title:** 7-Day Sprint para magka-Client sa Automation
- **30-sec Taglish Script:**
  [SHOW: Calendar sprint overlay: Mon build -> Wed publish -> Fri leads]
  "Hamunin natin ang sarili natin ngayong linggo: 7-Day Build in Public Challenge! Lunes: Mag-build ng isang Telegram bot sa n8n. Miyerkules: I-record ang screen mo habang tinuturo ito sa Taglish. Biyernes: I-upload sa YouTube at i-post ang GitHub link sa Pinoy dev groups. Linggo: Check your inbound inbox. Panoorin ang step-by-step roadmap sa channel namin!"
- **Caption Line:** Ang 7-Day challenge para simulan ang iyong tech funnel mula zero audience! ⏱️🔥

#### Hook 5: The Funnel That Works While You Sleep
- **Hook Title:** Ang Automation Funnel na kumukuha ng Leads para sa'yo
- **30-sec Taglish Script:**
  [SHOW: Static website form -> Telegram bot pinging phone: "New Discovery Call Booked"]
  "Paano ako kumukuha ng qualified client leads nang hindi nagbabayad ng ads? GitHub Pages landing page + n8n webhook + Telegram instant notification. Tuwing may business owner na magpapadala ng inquiry mula sa YouTube video ko, n8n will score the lead at magpapadala ng alert sa phone ko. Automated portfolio, automated intake. Ituturo ko sa'yo paano i-setup nang ₱0!"
- **Caption Line:** Build your automated lead generation funnel using GitHub Pages at n8n. 🚀

---

### Caption

Paano ka makakakuha ng high-paying automation clients kung nagsisimula ka sa zero audience at walang budget sa ads? Sa video na ito, ibinubunyag namin ang aming "Ship in Public" Flywheel: Paano ginagamit ang mga libreng YouTube tutorials at open-source GitHub repositories para maging magnetic client acquisition funnel na nagdadala ng inbound agency retainers.

#ShipInPublic #BuildInPublicPH #FreelanceDevPH
