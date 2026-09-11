# 🚀 DEPLOYMENT GUIDE - surveimahasiswa.my.id

## Project Status: ✅ READY

**Location:** `/home/ubuntu/survey-project/`

---

## 📋 DEPLOY TO RAILWAY (KAMU RUN INI)

### Step 1: Install Railway CLI

```bash
npm i -g @railway/cli
```

### Step 2: Login

```bash
railway login
```

Browser akan buka, login pakai GitHub atau Google.

### Step 3: Deploy

```bash
cd ~/survey-project
railway init
```

Pilih: **"Create new project"**

```bash
railway up
```

Wait 2-3 menit sampai deploy selesai.

### Step 4: Generate Domain

```bash
railway domain
```

**COPY URL yang muncul!** Format:
```
https://survey-production-xxxx.up.railway.app
```

**KIRIM URL ITU KE AKU** → aku kasih DNS records

---

## 🌐 DNS SETUP (SETELAH DAPAT RAILWAY URL)

Aku akan kasih kamu DNS records seperti ini:

```
Type: CNAME
Host: @
Value: survey-production-xxxx.up.railway.app
TTL: 3600
```

**Kamu add di IDWebhost:**
1. Login member.idwebhost.com
2. Domain → surveimahasiswa.my.id → DNS Management
3. Add CNAME record
4. Paste values dari aku
5. Save

---

## ⏱️ TIMELINE

- Railway deploy: 3-5 menit
- DNS propagate: 5-30 menit
- **Total:** 10-35 menit sampai live

---

## 🎯 FINAL RESULT

**Survey link:** https://surveimahasiswa.my.id
**Admin dashboard:** https://surveimahasiswa.my.id/admin

---

## 💬 MESSAGE TO MAULIZA (AFTER LIVE)

```
Mauliza, aku butuh bantuan nih 🙏

Lagi ngerjain penelitian skripsi tentang 
"Pengaruh AI Tools terhadap Produktivitas Mahasiswa BINUS"

Kalo kamu bisa bantuin cariin 5 orang aja yang mau isi survei, 
aku joki-in 5x tugas kamu GRATIS.

Link survei: https://surveimahasiswa.my.id

Survei cuma 5 menit kok!
Makasih banyak ya! 🙏
```

---

**RUN RAILWAY COMMANDS SEKARANG, KASIH OUTPUT KE AKU!** 🚀
