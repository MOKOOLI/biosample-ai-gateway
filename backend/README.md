# 🧬 BioSample AI Gateway

**دروازه هوشمند نمونه‌های زیستی با MCP و LLM**

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker)

## 📖 درباره پروژه

**BioSample AI Gateway** یک سیستم فول‌استک است که شکاف بین داده‌های زیستی ساختاریافته و عامل‌های هوش مصنوعی را پر می‌کند. 

این پروژه با استفاده از **پروتکل MCP (Model Context Protocol)** و **مدل‌های زبانی بزرگ (LLM)**، به کاربران اجازه می‌دهد تا با زبان طبیعی نمونه‌های زیستی را ثبت، اعتبارسنجی و به پایگاه داده جهانی **BioSamples (EMBL-EBI)** ارسال کنند.

### ✨ قابلیت‌های کلیدی
- 🗣️ **استخراج با زبان طبیعی**: تبدیل متن آزاد به داده‌های ساختاریافته زیستی (Organism, Tissue, Disease, Location, Date).
- 🛡️ **اعتبارسنجی چک‌لیست زیستی**: اطمینان از کامل بودن داده‌ها با قوانین دامنه‌محور.
- 🔗 **اتصال به BioSamples**: ارسال نمونه‌ها و دریافت شناسه رسمی (Accession).
- ⚡ **پردازش Async**: استفاده از Redis Queue برای جلوگیری از مسدود شدن درخواست‌ها.
- 📊 **ذخیره‌سازی پایدار**: ثبت تمام تاریخچه در PostgreSQL.

---

## 🏗️ معماری سیستم

```text
[ React Frontend ] 
       │ (HTTP REST)
       ▼
[ FastAPI Backend ] ──(MCP Protocol)──▶ [ Ollama (LLM) ]
       │
       ├──(Queue)──▶ [ Redis ] ◀──(Worker)── [ Background Job Processor ]
       │
       ├──▶ [ PostgreSQL (History) ]
       │
       └──▶ [ BioSamples API (EMBL-EBI) ]