import React, { useState } from 'react';
import {
  Upload, FileText, Image, Globe, Loader2, Download
} from 'lucide-react';

const TransliteratorApp = () => {
  const [file, setFile] = useState(null);
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [sourceScript, setSourceScript] = useState('Latin');
  const [targetScript, setTargetScript] = useState('Devanagari');

  // -----------------------------
  // FULL SCRIPT LIST
  // -----------------------------
  const scripts = [
    'Latin', 'Devanagari', 'Arabic', 'Cyrillic', 'Chinese', 'Japanese (Hiragana)', 'Japanese (Katakana)',
    'Korean (Hangul)', 'Greek', 'Hebrew', 'Thai', 'Bengali', 'Tamil', 'Telugu', 'Gujarati',
    'Kannada', 'Malayalam', 'Oriya', 'Punjabi (Gurmukhi)', 'Sinhala', 'Tibetan', 'Burmese',
    'Khmer', 'Lao', 'Georgian', 'Armenian', 'Ethiopic', 'Cherokee', 'Mongolian', 'Tifinagh',
    'N\'Ko', 'Vai', 'Osmanya', 'Hanifi Rohingya', 'Syriac', 'Thaana', 'Adlam', 'Bamum',
    'Mandaic', 'Samaritan', 'Coptic', 'Glagolitic', 'Gothic', 'Ogham', 'Runic', 'Old Italic',
    'Phoenician', 'Lydian', 'Carian', 'Lycian', 'Ugaritic', 'Old Persian', 'Deseret', 'Shavian',
    'Elbasan', 'Caucasian Albanian', 'Linear A', 'Linear B', 'Cypriot', 'Imperial Aramaic',
    'Palmyrene', 'Nabataean', 'Hatran', 'Meroitic', 'Old South Arabian', 'Old North Arabian',
    'Manichaean', 'Avestan', 'Inscriptional Parthian', 'Inscriptional Pahlavi', 'Psalter Pahlavi',
    'Old Turkic', 'Old Hungarian', 'Hanunoo', 'Buhid', 'Tagbanwa', 'Tagalog', 'Sundanese',
    'Batak', 'Lepcha', 'Ol Chiki', 'Cyrillic Extended', 'Glagolitic Supplement', 'Nyiakeng Puachue Hmong',
    'Wancho', 'Chorasmian', 'Dives Akuru', 'Khitan Small Script', 'Yezidi', 'Old Sogdian', 'Sogdian',
    'Elymaic', 'Nandinagari', 'Zanabazar Square', 'Soyombo', 'Pau Cin Hau', 'Bhaiksuki', 'Marchen',
    'Masaram Gondi', 'Gunjala Gondi', 'Makasar', 'Medefaidrin', 'Mende Kikakui', 'Modi',
    'Mro', 'Multani', 'Newa', 'Nushu', 'Pahawh Hmong', 'Tai Tham', 'Tai Viet', 'Warang Citi',
    'Ahom', 'Anatolian Hieroglyphs', 'Bassa Vah', 'Duployan', 'Grantha', 'Khojki',
    'Khudawadi', 'Mahajani', 'Meroitic Cursive', 'Meroitic Hieroglyphs', 'Old Permic',
    'Siddham', 'Tirhuta', 'Takri', 'Cuneiform', 'Egyptian Hieroglyphs',
    'Katakana (Japanese)', 'Bopomofo', 'Javanese', 'Balinese', 'Chakma', 'Sharada', 'Syloti Nagri',
    'Meetei Mayek', 'Limbu', 'Tai Le', 'New Tai Lue', 'Buginese', 'Tai Viet Extended', 'Kharoshthi',
    'Brahmi', 'Kaithi', 'Sora Sompeng', 'Canadian Aboriginal', 'Rejang', 'Cham', 'Kayah Li',
    'Lisu', 'Phags-pa', 'Tangut', 'Tangsa', 'Vithkuqi', 'Kawi', 'Nag Mundari'
  ];

  // -----------------------------
  // FILE UPLOAD HANDLER
  // -----------------------------
  const handleFileUpload = (e) => {
    const uploaded = e.target.files[0];
    setFile(uploaded);

    if (uploaded?.type === "text/plain") {
      const reader = new FileReader();
      reader.onload = (event) => setInputText(event.target.result);
      reader.readAsText(uploaded);
    }
  };

  // -----------------------------
  // MAIN TRANSLITERATION LOGIC
  // -----------------------------
  const transliterate = async () => {
    if (!inputText && !file) {
      alert("Enter text or upload a file first!");
      return;
    }

    setLoading(true);

    let textToProcess = inputText;

    try {
      // Image OCR using Claude
      if (file && file.type.startsWith("image/")) {
        const reader = new FileReader();
        const base64 = await new Promise((resolve) => {
          reader.onload = (e) => resolve(e.target.result.split(",")[1]);
          reader.readAsDataURL(file);
        });

        const ocrResponse = await fetch("https://api.anthropic.com/v1/messages", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            model: "claude-sonnet-4-20250514",
            max_tokens: 1000,
            messages: [
              {
                role: "user",
                content: [
                  {
                    type: "image",
                    source: { type: "base64", media_type: file.type, data: base64 }
                  },
                  { type: "text", text: "Extract all text from this image. Return only the text, nothing else." }
                ]
              }
            ]
          }),
        });

        const ocrJSON = await ocrResponse.json();
        textToProcess = ocrJSON?.content?.[0]?.text || "";
      }

      // Actual transliteration request
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          messages: [
            {
              role: "user",
              content:
                `Transliterate the following text from ${sourceScript} to ${targetScript}. ` +
                `Return ONLY the transliterated text with no explanations:\n\n${textToProcess}`
            }
          ]
        }),
      });

      const json = await response.json();
      setOutputText(json?.content?.[0]?.text || "");

    } catch (err) {
      console.error(err);
      alert("Error occurred: " + err.message);
    }

    setLoading(false);
  };

  // -----------------------------
  // DOWNLOAD OUTPUT
  // -----------------------------
  const downloadOutput = () => {
    const blob = new Blob([outputText], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `transliterated_${targetScript}.txt`;
    a.click();
  };

  // -----------------------------
  // UI
  // -----------------------------
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-indigo-50 to-blue-50 p-6">
      <div className="max-w-7xl mx-auto">

        {/* Header */}
        <div className="text-center mb-10">
          <div className="flex items-center justify-center gap-3 mb-3">
            <Globe className="w-10 h-10 text-indigo-600" />
            <h1 className="text-4xl font-bold text-gray-800">AI Transliterator</h1>
          </div>
          <p className="text-gray-600 text-lg">
            Convert text between <b>156+ world scripts</b>
          </p>
        </div>

        {/* Script selectors */}
        <div className="grid md:grid-cols-2 gap-6 mb-6">
          <div className="bg-white p-4 rounded shadow">
            <label className="font-semibold">Source Script</label>
            <select
              value={sourceScript}
              onChange={(e) => setSourceScript(e.target.value)}
              className="w-full border p-3 rounded mt-2"
            >
              {scripts.map((s) => <option key={s}>{s}</option>)}
            </select>
          </div>

          <div className="bg-white p-4 rounded shadow">
            <label className="font-semibold">Target Script</label>
            <select
              value={targetScript}
              onChange={(e) => setTargetScript(e.target.value)}
              className="w-full border p-3 rounded mt-2"
            >
              {scripts.map((s) => <option key={s}>{s}</option>)}
            </select>
          </div>
        </div>

        {/* Two text boxes side by side */}
        <div className="grid md:grid-cols-2 gap-6">

          {/* Left side: Input */}
          <div className="bg-white p-6 rounded shadow">
            <label className="font-semibold text-gray-700">Input Text</label>

            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              className="w-full h-64 border p-3 rounded mt-2 resize-none"
              placeholder="Enter text here…"
            />

            <div className="mt-4">
              <label className="font-medium">Upload File (optional)</label>
              <input
                type="file"
                accept=".txt,image/*"
                onChange={handleFileUpload}
                className="w-full border p-3 rounded mt-2"
              />
            </div>
          </div>

          {/* Right side: Output */}
          <div className="bg-white p-6 rounded shadow">
            <label className="font-semibold text-gray-700">Transliterated Output</label>

            <textarea
              value={outputText}
              readOnly
              className="w-full h-64 border p-3 rounded mt-2 bg-gray-50 resize-none"
              placeholder="Transliterated text will appear here…"
            />

            {outputText && (
              <button
                onClick={downloadOutput}
                className="mt-4 bg-green-600 text-white py-2 px-4 rounded flex items-center gap-2 hover:bg-green-700"
              >
                <Download className="w-4 h-4" /> Download Result
              </button>
            )}
          </div>
        </div>

        {/* Transliterate Button */}
        <button
          onClick={transliterate}
          disabled={loading}
          className="mt-8 w-full bg-indigo-600 text-white py-4 rounded text-lg font-semibold flex justify-center items-center gap-3 hover:bg-indigo-700 disabled:bg-indigo-400"
        >
          {loading && <Loader2 className="w-5 h-5 animate-spin" />}
          {loading ? "Processing…" : "Transliterate"}
        </button>
      </div>
    </div>
  );
};

export default TransliteratorApp;
