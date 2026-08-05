import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Search,
  Image as ImageIcon,
  Sparkles,
} from "lucide-react";

function VerifyForm() {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);

  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const mode = file ? "image" : "text";
  const canSubmit = file || text.trim().length > 0;

  const handleSubmit = () => {
    if (!canSubmit) return;

    navigate("/verifying", {
      state: {
        mode,
        text,
        file,
      },
    });
  };

  const handleTextChange = (e) => {
    setText(e.target.value);

    if (file) {
      setFile(null);
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files?.[0];

    if (selectedFile) {
      setFile(selectedFile);
      setText("");
    }
  };

  return (
    <motion.section
      initial={{ opacity: 0, y: 35 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="relative z-10 mb-24"
    >
      <div className="mx-auto w-full max-w-4xl">

        <div className="overflow-hidden rounded-3xl border border-white/10 bg-white/5 backdrop-blur-2xl shadow-[0_20px_60px_rgba(0,0,0,0.35)]">

          {/* Header */}

          <div className="px-8 pt-8 pb-2">

            <div className="inline-flex items-center gap-2 rounded-full border border-cyan-400/20 bg-cyan-500/10 px-4 py-2 text-sm font-medium text-cyan-300">
              <Sparkles size={16} />
              AI Verification
            </div>

            <h2 className="mt-5 text-3xl font-bold text-white">
              Verify Any Claim
            </h2>

            <p className="mt-2 text-slate-400">
              Paste a news claim, social media post, or upload a screenshot.
            </p>

          </div>

          {/* Form */}

          <div className="p-8">

            <textarea
              rows={7}
              value={text}
              onChange={handleTextChange}
              placeholder="Example: UPI payments have been banned across India..."
              className="w-full resize-none rounded-2xl border border-white/10 bg-slate-900/70 p-5 text-white outline-none transition duration-300 placeholder:text-slate-500 focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/30"
            />

            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              hidden
              onChange={handleFileChange}
            />

            <div className="mt-6 flex flex-col gap-4 md:flex-row">

              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="flex flex-1 items-center justify-center gap-3 rounded-2xl border border-white/10 bg-white/5 py-4 font-medium transition duration-300 hover:border-cyan-400/40 hover:bg-cyan-500/10"
              >
                <ImageIcon size={20} />

                {file
                  ? file.name.length > 28
                    ? `${file.name.substring(0, 28)}...`
                    : file.name
                  : "Upload Screenshot"}
              </button>

              <button
                type="button"
                onClick={handleSubmit}
                disabled={!canSubmit}
                className="flex flex-1 items-center justify-center gap-3 rounded-2xl bg-gradient-to-r from-cyan-500 via-indigo-500 to-purple-600 py-4 font-semibold text-white shadow-xl transition duration-300 hover:scale-[1.02] disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:scale-100"
              >
                <Search size={20} />
                Verify using AI
              </button>

            </div>

          </div>

        </div>

      </div>
    </motion.section>
  );
}

export default VerifyForm;