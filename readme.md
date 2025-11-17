
# **AI Transliterator – React App**

### Convert text between **156+ world writing systems** using AI (Claude Sonnet 4)

This app provides advanced **AI-powered transliteration + OCR** using Anthropic’s Claude Vision & Language models.
It supports **text input, file upload, OCR from images, script selection, and downloadable output.**

---

## 🚀 **Features**

### ✅ Transliteration Between 156+ Scripts

Includes Latin, Devanagari, Arabic, Cyrillic, Bengali, Tamil, Hangul, Chinese, Japanese, Thai, Tibetan, historic scripts, and many rare writing systems.

### ✅ OCR Support

Upload an image to extract text before transliteration.

### ✅ File Upload Support

Upload `.txt` files and auto-load text into input box.

### ✅ Two-Panel UI

* **Left:** Input text
* **Right:** AI-generated transliteration

### ✅ Download Output

Export transliterated text as `.txt`.

### ✅ Modern UI

Tailwind-based, responsive, clean design using React and Lucide icons.

---

## 📦 **Installation**

### 1. Clone the repository

```bash
git clone https://github.com/yourname/transliterator-app
cd transliterator-app
```

### 2. Install dependencies

```bash
npm install
```

### 3. Add your API keys

Create a file:

```
src/config.js
```

Inside it add:

```js
export const ANTHROPIC_API_KEY = "your_anthropic_api_key_here";
```

Then import it in the component:

```js
import { ANTHROPIC_API_KEY } from "./config";
```

---

## ▶️ **Run the App**

```bash
npm run dev
```

Your app will be available at:

```
http://localhost:5173/
```

---

## 🧩 **Project Structure**

```
src/
 ├── components/
 │    └── TransliteratorApp.jsx
 ├── config.js   <-- API keys stored here
 ├── App.jsx
 ├── main.jsx
 └── index.css
```

---

## 🔧 **How Transliteration Works**

### 1. Text Input

User enters text or uploads `.txt`.

### 2. Optional OCR

If the uploaded file is an image, the app:

* Converts image → Base64
* Sends it to Claude Vision model
* Extracts raw text

### 3. AI Transliteration

App sends:

```
"Transliterate text from <source> to <target>"
```

Claude responds with **only clean transliterated output**.

---

## 🛡 Environment Variables (Optional)

You can also store your API key in `.env`:

```
VITE_ANTHROPIC_API_KEY=your_key
```

Then access it using:

```js
const apiKey = import.meta.env.VITE_ANTHROPIC_API_KEY;
```

---

## 📝 Notes

* All OCR and transliteration is done via **Anthropic Claude Sonnet 4 (May 2025)**.
* No backend server is required.
* App is fully client-side.

---

## 📜 **License**

MIT License – Free to modify and use.

---

## 🤝 Contribute

Pull requests welcome!
If you make improvements (UI, more scripts, backend version, caching), feel free to submit PRs.


