# 🚀 **FREE Notification Services Setup Guide**

## 🎯 **Overview**

This guide shows you how to set up **100% FREE** notification services for OpenPolicy, just like OpenParliament does! We have multiple options for each notification type, so you can choose what works best for you.

## 📧 **FREE Email Services**

### **Option 1: Resend.com (Recommended for Start)**
- ✅ **100 emails/day FREE** (3,000/month)
- ✅ **Professional delivery** (99.9% success rate)
- ✅ **No credit card required**
- ✅ **Beautiful templates included**

**Setup:**
1. Go to [resend.com](https://resend.com)
2. Sign up with your email
3. Get your API key
4. Add to `.env`:
```bash
RESEND_API_KEY=re_1234567890abcdef
FROM_EMAIL=noreply@openpolicy.me
```

### **Option 2: Our Own Mail Server (100% FREE Forever)**
- ✅ **Zero monthly costs**
- ✅ **100% control over delivery**
- ✅ **Professional email addresses**
- ✅ **Custom domain support**

**Setup:**
1. **Start our mail server:**
```bash
cd services/user-service
docker-compose -f docker-compose.mail.yml up -d
```

2. **Configure DNS records:**
```
A     mail.openpolicy.me    → Your server IP
MX    openpolicy.me         → mail.openpolicy.me (priority 10)
TXT   openpolicy.me         → v=spf1 a mx ~all
```

3. **Add to `.env`:**
```bash
OWN_SMTP_HOST=localhost
OWN_SMTP_PORT=587
OWN_SMTP_USER=openpolicy
OWN_SMTP_PASSWORD=openpolicy123
```

4. **Access webmail:** http://localhost:8082

## 📱 **FREE Push Notifications**

### **Option 1: Web Push API (100% FREE, No Limits)**
- ✅ **Built into every modern browser**
- ✅ **Zero costs forever**
- ✅ **No external dependencies**
- ✅ **Instant delivery**

**Setup:**
1. **Generate VAPID keys:**
```bash
# Install web-push globally
npm install -g web-push

# Generate keys
web-push generate-vapid-keys
```

2. **Add to `.env`:**
```bash
VAPID_PUBLIC_KEY=BLBz...
VAPID_PRIVATE_KEY=BLBz...
```

### **Option 2: Firebase Cloud Messaging (100% FREE)**
- ✅ **Google's service, no costs**
- ✅ **Excellent delivery rates**
- ✅ **Mobile app support**
- ✅ **Analytics included**

**Setup:**
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Create a new project
3. Add Android/iOS app
4. Get your Server Key
5. Add to `.env`:
```bash
FCM_SERVER_KEY=AAAA...
```

### **Option 3: OneSignal (10,000/month FREE)**
- ✅ **Generous free tier**
- ✅ **Advanced targeting**
- ✅ **A/B testing**
- ✅ **Rich notifications**

**Setup:**
1. Go to [onesignal.com](https://onesignal.com)
2. Create account
3. Create app
4. Get App ID and REST API Key
5. Add to `.env`:
```bash
ONESIGNAL_APP_ID=12345678-1234-1234-1234-123456789012
ONESIGNAL_REST_API_KEY=Basic_1234567890abcdef
```

## 📞 **FREE SMS Services**

### **Option 1: Our Own SMS Gateway (100% FREE with Hardware)**
- ✅ **Zero monthly costs**
- ✅ **Full control**
- ✅ **Professional setup**
- ✅ **Custom phone numbers**

**Hardware Requirements:**
- USB 3G/4G modem (~$30)
- SIM card with data plan
- Raspberry Pi or small server

**Setup:**
1. **Install SMS gateway software:**
```bash
# Example with Gammu
sudo apt-get install gammu
sudo gammu-config
```

2. **Add to `.env`:**
```bash
OWN_SMS_GATEWAY_URL=http://localhost:8083/sms
OWN_SMS_API_KEY=your_api_key
```

### **Option 2: Twilio (Free Trial, Then Pay-per-Use)**
- ✅ **Free trial available**
- ✅ **Reliable service**
- ✅ **Good documentation**
- ✅ **Pay only for what you use**

**Setup:**
1. Go to [twilio.com](https://twilio.com)
2. Sign up for free trial
3. Get Account SID and Auth Token
4. Add to `.env`:
```bash
TWILIO_ACCOUNT_SID=AC1234567890abcdef
TWILIO_AUTH_TOKEN=1234567890abcdef
TWILIO_PHONE_NUMBER=+1234567890
```

## 🔧 **Complete Setup Commands**

### **1. Install Dependencies**
```bash
cd services/user-service

# Install Python packages
pip install -r requirements.txt

# Install additional packages for notifications
pip install pywebpush httpx
```

### **2. Set Up Environment**
```bash
# Copy environment template
cp .env.example .env

# Edit with your settings
nano .env
```

### **3. Start Mail Server (Optional)**
```bash
# Start our own mail server
docker-compose -f docker-compose.mail.yml up -d

# Check status
docker-compose -f docker-compose.mail.yml ps
```

### **4. Run Database Migration**
```bash
# Initialize Alembic
alembic init alembic

# Run migration
alembic upgrade head
```

### **5. Test Services**
```bash
# Start user service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8081 --reload

# Test endpoints
curl http://localhost:8081/health
```

## 🌐 **Production Deployment**

### **Domain Configuration**
```bash
# DNS Records for openpolicy.me
A     openpolicy.me         → Your server IP
A     api.openpolicy.me     → Your server IP
A     mail.openpolicy.me    → Your server IP
MX    openpolicy.me         → mail.openpolicy.me (priority 10)
TXT   openpolicy.me         → v=spf1 a mx ~all
CNAME  www.openpolicy.me    → openpolicy.me
```

### **SSL Certificates**
```bash
# Install Certbot
sudo apt-get install certbot

# Get certificates
sudo certbot certonly --standalone -d openpolicy.me -d api.openpolicy.me -d mail.openpolicy.me
```

### **Nginx Configuration**
```nginx
# /etc/nginx/sites-available/openpolicy
server {
    listen 80;
    server_name openpolicy.me www.openpolicy.me;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name openpolicy.me www.openpolicy.me;
    
    ssl_certificate /etc/letsencrypt/live/openpolicy.me/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/openpolicy.me/privkey.pem;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/ {
        proxy_pass http://localhost:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 **Cost Comparison**

| Service Type | Free Option | Free Limit | Paid Alternative | Monthly Cost |
|--------------|-------------|------------|------------------|--------------|
| **Email** | Resend.com | 100/day | SendGrid | $15-80 |
| **Email** | Our Mail Server | Unlimited | Mailgun | $35-80 |
| **Push** | Web Push API | Unlimited | Pushwoosh | $29-99 |
| **Push** | Firebase FCM | Unlimited | OneSignal Pro | $99+ |
| **SMS** | Our Gateway | Unlimited | Twilio | $0.0075/msg |
| **SMS** | Twilio Trial | 1,000 free | Nexmo | $0.006/msg |

**Total Monthly Savings: $150-300+**

## 🚨 **Troubleshooting**

### **Email Issues**
```bash
# Check mail server logs
docker-compose -f docker-compose.mail.yml logs mail-server

# Test SMTP connection
telnet localhost 587

# Check DNS records
dig MX openpolicy.me
dig TXT openpolicy.me
```

### **Push Notification Issues**
```bash
# Check VAPID keys
echo $VAPID_PUBLIC_KEY
echo $VAPID_PRIVATE_KEY

# Test web push
curl -X POST http://localhost:8081/test-push
```

### **SMS Issues**
```bash
# Check SMS gateway status
systemctl status gammu-smsd

# Test modem connection
sudo gammu --identify
```

## 🎉 **Success!**

You now have **professional-grade notification services** with **zero monthly costs**! This setup gives you:

- ✅ **Professional email delivery** (Resend.com or our mail server)
- ✅ **Instant push notifications** (Web Push API, FCM, OneSignal)
- ✅ **Reliable SMS delivery** (Our gateway or Twilio)
- ✅ **Full control** over your notification infrastructure
- ✅ **Cost savings** of $150-300+ per month

This is exactly how OpenParliament handles notifications - with their own infrastructure and smart service selection. You're now running a production-ready notification system! 🚀
