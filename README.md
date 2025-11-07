# 🏃💬 AI Asistent pro Půlmaraton Plzeňského kraje

> **Hackathon Otevřených Dat, Sušice** | Tým **Data maniaci**

Cílem projektu je **automatizace odpovidani** pro organizovani půlmaratonu Plzeňského kraje pomocí umělé inteligence, čímž ulehčujeme práci organizátorům a zlepšujeme servis pro účastníky.

---

## ✨ Klíčové Funkce

* **AI Chatbot (Gemini):** Okamžité odpovídání na dotazy k závodu s využitím dat organizatoru jako znalostní báze.
* **AI Email Autoreply:** Inteligentní systém, který automaticky generuje personalizované odpovědi na příchozí emailové dotazy.
* **n8n Workflow:** Celá logika, integrace a správa komunikace je řízena pomocí no-code automatizačního nástroje **n8n**.

---

## 🛠️ Použité Technologie

| Komponenta | Technologie | Účel |
| :--- | :--- | :--- |
| **AI Model** | **Google Gemini API** | Zpracování jazyka, generování přesných a kontextových odpovědí. |
| **Automatizace** | **n8n** | Propojení emailu/chatu s AI, řízení workflow (příjem -> analýza -> odpověď). |

---

## ⚙️ Struktura a Workflow

Projekt je postaven na jednoduchém a robustním **n8n** workflow:

1.  **Trigger:** N8N sleduje příchozí email (IMAP) nebo dotaz z chatu.
2.  **Analýza (Gemini):** Dotaz je odeslán do Gemini API s kontextem otevřených dat.
3.  **Generování Odpovědi:** Gemini generuje relevantní text odpovědi.
4.  **Akce:** N8N odešle odpověď zpět uživateli 



---

## 🚀 Proč náš projekt?

* **Rychlost:** Zkracuje dobu reakce z hodin na sekundy.
* **Přesnost:** AI využívá oficiální otevřená data k minimalizaci chyb.
* **Efektivita:** Uvolňuje lidské zdroje organizátorů pro komplexnější úkoly.

---

**Tým:** Studenti **Vyšší odborné školy a Střední průmyslové školy elektrotechnické Plzeň**
