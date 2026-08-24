## Pillar 2: Hardened Server — Fail-First Security

### Long-form script (10 min, Taglish, conversational)

[COLD OPEN — SCREEN RECORDING: terminal showing auth.log scrolling fast, red text overlay "UNDER ATTACK"]

Mga boss, ito yung server ko. Brand new. Kakalagay ko lang kagabi — free Oracle Cloud instance, yung ginawa natin sa Pillar 1. Wala pa akong ni-deploy na kahit ano. Wala pang website, wala pang app, literally blangkong server.

Tapos pag check ko ng logs ngayong umaga…

[SHOW: terminal command]
```
sudo cat /var/log/auth.log | grep "Failed password" | tail -50
```

[SHOW: fake auth.log output scrolling, dramatic pause habang naglo-load]
```
Aug 24 02:13:07 srv sshd[4821]: Failed password for root from 218.92.0.107 (China) port 43521 ssh2
Aug 24 02:13:09 srv sshd[4821]: Failed password for root from 218.92.0.107 (China) port 43521 ssh2
Aug 24 02:13:14 srv sshd[4823]: Failed password for admin from 185.224.128.43 (Russia) port 52190 ssh2
Aug 24 02:13:18 srv sshd[4825]: Failed password for root from 45.227.254.20 (Brazil) port 38891 ssh2
Aug 24 02:13:21 srv sshd[4827]: Failed password for ubuntu from 103.145.13.98 (Vietnam) port 44012 ssh2
Aug 24 02:13:24 srv sshd[4829]: Failed password for test from 61.177.172.55 (China) port 51823 ssh2
Aug 24 02:13:27 srv sshd[4831]: Failed password for root from 92.255.85.135 (Russia) port 39201 ssh2
Aug 24 02:13:29 srv sshd[4833]: Failed password for admin from 177.54.148.218 (Brazil) port 47833 ssh2
Aug 24 02:13:33 srv sshd[4835]: Failed password for root from 218.92.0.107 (China) port 43525 ssh2
Aug 24 02:13:36 srv sshd[4837]: Failed password for postgres from 43.154.19.227 (Hong Kong) port 60122 ssh2
Aug 24 02:13:38 srv sshd[4839]: Failed password for root from 112.85.42.88 (China) port 28441 ssh2
Aug 24 02:13:41 srv sshd[4841]: Failed password for oracle from 185.224.128.43 (Russia) port 52201 ssh2
```

Nakita niyo yan? China, Russia, Brazil, Vietnam, Hong Kong — parang United Nations ng hackers ang nagta-try mag-login sa server ko. At hindi lang bente o trenta — pag binilang ko lahat…

[SHOW: command]
```
sudo cat /var/log/auth.log | grep "Failed password" | wc -l
```

[SHOW: output]
```
1,847
```

One thousand, eight hundred forty-seven failed login attempts. Sa loob lang ng isang gabi. Hindi pa yan targeted attack ha — yan ay mga bots. Automated scripts na nagsa-scan ng buong internet, hinahanap nila kung sinong server ang bukas ang pinto.

At kung ang password mo ay "password123" o "admin" o kahit ano na madaling hulaan — congratulations, may bagong roommate ka sa server mo. At hindi siya magbabayad ng renta.

[BEAT — straight face to camera]

So ngayon, aayusin natin 'to. Hindi tayo magpapa-hack. Libre lang 'tong server natin, pero hindi ibig sabihin libre na rin para sa kanila. I-lock down natin 'to, step by step, habang ginagawa ko — kayo naman, sundan niyo.

---

[TITLE CARD: "STEP 1: SSH KEYS ONLY — Patay ang Password"]

[SHOW: camera/screen split — face cam + terminal]

Okay, Step 1. Ito yung pinaka-importante. Yung mga bots na nakita natin sa log, ano bang ginagawa nila? Gumuguess sila ng password. Root, admin, test, ubuntu — tina-try nila lahat. So ano ang pinaka-simple na fix?

Tanggalin natin ang password. Completely. Wala nang password login. SSH keys lang ang papasok.

Kung wala ka pang SSH key sa local machine mo, gawa tayo:

[SHOW: local terminal]
```
ssh-keygen -t ed25519 -C "agentlabph@email.com"
```

Pindutin mo lang Enter sa lahat ng tanong niya. Tapos i-copy natin yung public key papunta sa server:

[SHOW: local terminal]
```
ssh-copy-id ubuntu@your-server-ip
```

Pag nag-login ka ulit, hindi ka na tinanong ng password — ibig sabihin, gumagana na yung key. Perfect. Ngayon, pataying natin ang password authentication sa mismong server:

[SHOW: server terminal]
```
sudo nano /etc/ssh/sshd_config
```

[SHOW: highlight the lines being changed in the config file]

Hanapin niyo 'tong mga linya, at palitan:

```
PasswordAuthentication no
PubkeyAuthentication yes
PermitRootLogin no
```

Tatlo lang yan. `PasswordAuthentication no` — wala nang password. `PubkeyAuthentication yes` — SSH key lang ang pasok. `PermitRootLogin no` — kahit may key ka, hindi ka pwedeng mag-login bilang root. Use your own user, tapos `sudo` na lang.

I-save niyo — `Ctrl+O, Enter, Ctrl+X` — tapos i-restart yung SSH service:

[SHOW: server terminal]
```
sudo systemctl restart sshd
```

[FACE CAM — confident nod]

Boom. Yung 1,847 bots na yan? Wala na silang magagawa. Kahit isang milyon pang password ang i-try nila — walang password na tatanggapin ng server. Parang pinalitan mo yung lock ng bahay mo from regular na susi to fingerprint — wala silang daliri mo, hindi sila papasok.

---

[TITLE CARD: "STEP 2: UFW Firewall — Sarado Lahat, Bukas Lang ang Kailangan"]

[SHOW: server terminal]

Next, firewall. Pag bagong server, lahat ng port bukas by default — port 1 hanggang port 65535. Parang bahay na lahat ng bintana at pinto nakabukas. Hindi natin kailangan yan.

Ang kailangan lang natin: port 22 para sa SSH, port 80 para sa HTTP, at port 443 para sa HTTPS. Tatlo lang. Sarado lahat ng iba.

UFW — Uncomplicated Firewall — ang pinakamadaling paraan para gawin to. Pre-installed na sa Ubuntu:

[SHOW: commands one by one with brief pause between each]
```
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

Dahan-dahan lang tayo. `default deny incoming` — lahat ng papasok, bawal muna. `default allow outgoing` — lahat ng palabas, okay lang, kasi kailangan ng server mag-download ng updates. Tapos isa-isa, binubuksan natin yung tatlong port lang na kailangan.

At ngayon, i-enable na natin:

[SHOW: terminal]
```
sudo ufw enable
```

[SHOW: prompt "Command may disrupt existing SSH connections. Proceed with operation (y|n)?"]

Huwag kayong kabahan dito. Tatanungin ka niya kung sure ka — type `y`. Hindi madi-disconnect ang SSH mo kasi in-allow na natin yung port 22.

[SHOW: confirmation message]
```
Firewall is active and enabled on system startup
```

Check natin:

[SHOW: terminal]
```
sudo ufw status verbose
```

[SHOW: output showing the three allowed ports, everything else denied]

Ayan. Tatlong port lang ang bukas. Yung mga bots na nagsa-scan ng random ports — port 3306 MySQL, port 5432 PostgreSQL, port 8080 — wala na, sarado lahat, walang reply, parang hindi ka nag-e-exist.

---

[TITLE CARD: "STEP 3: Fail2Ban — Auto-Ban ang Mga Pasaway"]

[FACE CAM — medyo mischievous smile]

Okay, pini-prevent na natin yung password login. Sarado na lahat ng port maliban sa tatlo. Pero yung port 22 — bukas pa rin, kailangan natin yun para sa SSH. So may mga bots pa rin na mag-a-attempt mag-connect kahit laging ma-fail. Nakakairita, at nag-co-consume pa ng resources ng server mo.

Pasok si Fail2Ban. Ito yung bouncer ng server mo. Pag may nag-try mag-login at nag-fail ng tatlong beses? Banned. Blocked ang IP niya. Automatic.

[SHOW: terminal]
```
sudo apt update && sudo apt install fail2ban -y
```

Tapos gawa tayo ng config file:

[SHOW: terminal]
```
sudo nano /etc/fail2ban/jail.local
```

[SHOW: typing the config, line by line]
```
[DEFAULT]
bantime  = 3600
findtime = 600
maxretry = 3
banaction = ufw

[sshd]
enabled  = true
port     = ssh
filter   = sshd
logpath  = /var/log/auth.log
maxretry = 3
```

I-explain ko. `bantime = 3600` — one hour ang ban. Pag na-ban ka, balik ka sa isang oras. Pero sa totoo lang, yung mga bots, nag-mo-move on na sila. `findtime = 600` — sa loob ng 10 minutes, pag nag-fail ka ng `maxretry = 3` — tatlong beses — ban agad. `banaction = ufw` — gamit natin yung UFW na firewall natin para i-block yung IP. Hindi na siya makakapasok sa kahit anong port.

Tapos yung `[sshd]` section — specifically sa SSH natin i-a-apply. I-save at i-start:

[SHOW: terminal]
```
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

Check natin kung gumagana:

[SHOW: terminal]
```
sudo fail2ban-client status sshd
```

[SHOW: output]
```
Status for the jail: sshd
|- Filter
|  |- Currently failed: 2
|  |- Total failed:     14
|  `- File list:        /var/log/auth.log
`- Actions
   |- Currently banned: 3
   |- Total banned:     5
   `- Banned IP list:   218.92.0.107 185.224.128.43 61.177.172.55
```

[FACE CAM — pointing at screen]

Ayan! Tatlo nang naka-ban! Yung China at Russia IPs na nakita natin kanina — blocked na. Automatic. Hindi ka kailangan mag-monitor 24/7. Si Fail2Ban ang nagbabantay para sa'yo habang tulog ka.

---

[TITLE CARD: "STEP 4: Cloudflare Tunnel — Stealth Mode"]

[FACE CAM — leans in, mas seryoso]

Okay mga boss, dito na yung boss level. Steps 1 to 3, solid na yan — enough na para sa karamihan ng use cases. Pero kung gusto mo ng ultimate protection, ito yung pinakamalupet: Cloudflare Tunnel.

Ano ang problema sa current setup natin? Port 22 bukas pa rin sa internet. Oo, SSH keys lang ang tanggap, oo, naka-ban agad ang mga pasaway — pero kita pa rin ng mga scanner na may bukas kang port 22. Parang kahit may guard sa gate mo, nakikita pa rin ng mga tao na may gate ka.

Ang Cloudflare Tunnel? Wala nang gate. Tinatago mo yung buong bahay. Literally, sarado lahat ng port sa server mo — walang 22, walang bukas, wala. Pero nag-co-connect ka pa rin sa server mo through Cloudflare.

Paano gumagana? Yung server mo ang nagko-connect papunta sa Cloudflare — outbound connection. Walang inbound port na kailangan buksan. Parang VPN pero libre at walang setup na nakakalito.

[SHOW: terminal]

Una, install natin ang `cloudflared`:

```
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o cloudflared.deb
sudo dpkg -i cloudflared.deb
```

Tapos i-login natin sa Cloudflare account mo — libre lang ang account ha:

```
cloudflared tunnel login
```

[SHOW: browser opening Cloudflare auth page]

Pumili ka ng domain mo dito. Kahit libre lang na domain, okay. Tapos gawa ng tunnel:

```
cloudflared tunnel create hardened-server
```

[SHOW: output showing tunnel ID and credentials file created]

I-configure natin:

[SHOW: terminal]
```
sudo nano ~/.cloudflared/config.yml
```

```yaml
tunnel: hardened-server
credentials-file: /home/ubuntu/.cloudflared/<tunnel-id>.json

ingress:
  - hostname: ssh.yourdomain.com
    service: ssh://localhost:22
  - service: http_status:404
```

Start the tunnel:

```
cloudflared tunnel run hardened-server
```

At ngayon, sa UFW, tanggalin na natin yung port 22:

```
sudo ufw delete allow 22/tcp
sudo ufw status verbose
```

[SHOW: UFW status — only 80 and 443 remain, or even those removed if pure tunnel]

[FACE CAM — dramatic pause]

Port 22? Sarado na. Wala nang SSH port na nakikita sa internet. Pag mag-na-nmap ang kahit sino sa IP mo — walang makikita. Ghost ka. Invisible.

Tapos paano ka maglo-login? Sa local machine mo:

```
cloudflared access ssh --hostname ssh.yourdomain.com
```

O i-configure mo yung SSH config mo:

[SHOW: local terminal]
```
nano ~/.ssh/config
```

```
Host hardened-server
    HostName ssh.yourdomain.com
    ProxyCommand cloudflared access ssh --hostname %h
    User ubuntu
```

Tapos `ssh hardened-server` na lang. Parang normal na SSH, pero dumadaan sa Cloudflare Tunnel. Walang exposed port. Zero attack surface.

---

[OUTRO — FACE CAM, relaxed but proud]

So ayan mga boss. Tayo nagsimula sa server na may halos 2,000 brute-force attempts sa isang gabi. Ngayon?

[SHOW: recap graphic/checklist, check marks appearing one by one]

✅ Password authentication — PATAY. SSH keys only.
✅ Firewall — SARADO lahat maliban sa kailangan.
✅ Fail2Ban — Auto-ban sa mga pasaway. Tatlong tries, tapos ban.
✅ Cloudflare Tunnel — Wala nang bukas na port. Invisible sa internet.

Libreng server, enterprise-level security. Walang binayaran. Walang excuse.

Sa susunod na pillar, ide-deploy na natin ang actual na apps dito — containers, websites, automation tools — lahat libre. Kaya i-subscribe na, para kasama kayo.

[END CARD: Subscribe + Bell + "Pillar 3: Deploy mo na yan"]

Kung gusto niyong makita yung auth.log niyo mismo, try niyo yung command sa pinned comment. Baka magulat kayo kung ilan na ang nag-try pumasok. See you sa next one, mga boss.

---

### 5 Short-form hooks

**Hook 1: "1,847 Hackers in One Night"**

[SHOW: terminal scrolling auth.log rapidly, dramatic music]

Alam niyo ba na pag gumawa ka ng server — kahit libre, kahit walang laman — within hours, ina-attack ka na?

[SHOW: command + output]
```
sudo cat /var/log/auth.log | grep "Failed password" | wc -l
```
Output: `1,847`

One thousand eight hundred forty-seven login attempts. Isang gabi. China, Russia, Brazil — parang UN meeting sa server ko. Mga bots yan — automatic na nagsa-scan ng buong internet.

Fix? Isang linya lang:

```
PasswordAuthentication no
```

Sa `/etc/ssh/sshd_config`. Wala nang password, wala nang problema. SSH keys lang. Full tutorial sa main video — link sa bio.

**Caption:** Isang gabi lang, 1,847 na ang nag-try pumasok sa server ko. Nakakatakot? Hindi — kung alam mo ang fix. 🔒 #PinoyDev #FreeTier #ServerSecurity

---

**Hook 2: "Tatlong Port Lang ang Kailangan Mo"**

[SHOW: terminal]

Bagong server mo? Lahat ng port bukas — 65,535 ports, bukas lahat. Parang bahay na lahat ng bintana walang screen.

Ilan lang ba talaga ang kailangan mo?

```
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

Tatlo lang. SSH, HTTP, HTTPS. Sarado lahat ng iba. Pag may nag-scan sa port 3306 mo — MySQL — wala, walang reply. Parang wala kang server.

Limang commands, five minutes, 65,532 ports sarado na. Walang excuse.

**Caption:** 65,535 ports na bukas — tatlo lang pala ang kailangan mo. Limang commands = locked down. 🔥 #UFW #CloudSecurity #AgentLabPH

---

**Hook 3: "Tatlong Tries Ka Lang, Ban Ka Na"**

[SHOW: terminal with fail2ban status output]

May bouncer ang server ko. Hindi tao — software. Pangalan niya? Fail2Ban.

Pag may nag-try mag-login sa server ko at nag-fail ng tatlong beses sa loob ng 10 minutes?

[SHOW: fail2ban-client status output]
```
Currently banned: 3
Banned IP list: 218.92.0.107 185.224.128.43 61.177.172.55
```

Automatic ban. Isang oras, blocked sa lahat ng port. Hindi mo kailangan mag-monitor — si Fail2Ban ang gising habang tulog ka.

Install? Dalawang commands lang:
```
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
```

Libre. Automatic. Walang tulog.

**Caption:** Tatlong failed login = auto-ban. Si Fail2Ban ang nagbabantay ng server mo 24/7. Libre lang. 🚫 #Fail2Ban #AutoSecurity #FreelancerTech

---

**Hook 4: "Invisible Server — Walang Port na Bukas"**

[SHOW: nmap scan of server IP, all ports showing "filtered" or "closed"]

Pag ni-scan mo yung server ko — walang makikita. Zero open ports. Parang walang server. Ghost.

Pero nag-ru-run ang website ko, nag-ru-run ang apps ko, naglo-login pa rin ako sa SSH. Paano?

Cloudflare Tunnel. Yung server ko ang nagko-connect palabas — papunta sa Cloudflare. Walang port na bukas papasok. Walang 22, walang 80, kahit ano — wala.

```
cloudflared tunnel create my-tunnel
cloudflared tunnel run my-tunnel
```

Libre. Zero attack surface. Pag wala silang makitang pinto, paano sila papasok?

**Caption:** Nag-nmap sila sa server ko — wala silang nakita. Zero open ports pero live ang lahat. Cloudflare Tunnel magic. 👻 #CloudflareTunnel #ZeroTrust #InvisibleServer

---

**Hook 5: "Free Server, Enterprise Security"**

[SHOW: quick montage — auth.log attack → SSH key setup → UFW → Fail2Ban → Cloudflare Tunnel, each with a ✅ check mark]

Free Oracle Cloud server — libre.
SSH keys — libre.
UFW Firewall — libre.
Fail2Ban — libre.
Cloudflare Tunnel — libre.

Lahat libre, pero yung security level? Same level ng mga naka-AWS na nagbabayad ng thousands per month.

Hindi excuse ang "wala akong budget for security." Lahat ng tools na kailangan mo, nandyan na sa server mo. I-setup mo lang.

Apat na steps, walang bayad, enterprise-grade protection. Full walkthrough sa main video.

**Caption:** Walang budget for security? Hindi excuse yan. Apat na FREE tools = enterprise-level protection sa free server mo. 💪 #ZeroBudgetSecurity #PinoyFreelancer #AgentLabPH

---

### Caption

Bagong server mo, walang laman, tapos kinagabihan — halos 2,000 brute-force login attempts na galing sa buong mundo. 😱 Sa video na 'to, pinapakita ko kung paano i-lock down ang FREE Oracle Cloud server mo in 4 steps — SSH keys, UFW firewall, Fail2Ban, at Cloudflare Tunnel — para enterprise-level ang security kahit zero ang gastos. Sundan niyo habang ginagawa ko, real commands, real setup.

#AgentLabPH #FreeCloudSecurity #PinoyDevSecurity
