import { motion } from "framer-motion";

function Hero() {
  return (
    <section className="w-full pt-16 pb-10 text-center">
      {/* Badge */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="inline-flex items-center gap-2 rounded-full border border-cyan-500/20 bg-cyan-500/10 px-5 py-2 text-sm font-medium text-cyan-300"
      >
        🚀 AI Powered Fact Verification
      </motion.div>

      {/* Main Heading */}
      <motion.h1
        initial={{ opacity: 0, y: 25 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.6 }}
        className="mx-auto mt-8 max-w-4xl text-4xl font-extrabold leading-tight text-white sm:text-5xl lg:text-6xl"
      >
        Verify Claims &amp; Screenshots
      </motion.h1>

      {/* Subtitle */}
      <motion.h2
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.45, duration: 0.6 }}
        className="mt-4 bg-gradient-to-r from-cyan-400 via-indigo-400 to-purple-500 bg-clip-text text-2xl font-bold text-transparent sm:text-3xl"
      >
        Using Trusted AI Sources
      </motion.h2>

      {/* Description */}
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.65 }}
        className="mx-auto mt-6 max-w-3xl px-4 text-base leading-8 text-slate-300 sm:text-lg"
      >
        Detect misinformation using Retrieval-Augmented Generation (RAG),
        semantic search, trusted evidence retrieval, and explainable AI to
        verify claims from news, social media, and screenshots.
      </motion.p>
    </section>
  );
}

export default Hero;