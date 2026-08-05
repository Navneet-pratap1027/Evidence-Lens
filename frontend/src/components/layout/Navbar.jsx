import { NavLink } from "react-router-dom";
import { ShieldCheck, Github } from "lucide-react";
import { motion } from "framer-motion";

function Navbar() {
  return (
    <motion.header
      initial={{ y: -70, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="fixed inset-x-0 top-0 z-50 border-b border-white/10 bg-slate-950/70 backdrop-blur-xl"
    >
      <div className="mx-auto flex h-20 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">

        {/* Logo */}
        <NavLink
          to="/"
          className="flex items-center gap-3 flex-shrink-0"
        >
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 shadow-lg shadow-cyan-500/30">
            <ShieldCheck size={24} className="text-white" />
          </div>

          <div>
            <h1 className="text-lg sm:text-xl lg:text-2xl font-extrabold text-white">
              EvidenceLens
            </h1>

            <p className="hidden sm:block text-xs text-slate-400">
              Explainable AI Verification
            </p>
          </div>
        </NavLink>

        {/* Navigation */}
        <nav className="hidden md:flex items-center gap-8">

          <NavLink
            to="/"
            className={({ isActive }) =>
              isActive
                ? "font-semibold text-cyan-400"
                : "text-slate-300 transition hover:text-cyan-300"
            }
          >
            Verify
          </NavLink>

          <NavLink
            to="/history"
            className={({ isActive }) =>
              isActive
                ? "font-semibold text-cyan-400"
                : "text-slate-300 transition hover:text-cyan-300"
            }
          >
            History
          </NavLink>

        </nav>

        {/* Right Side */}
        <div className="hidden md:flex items-center gap-4">

          <button
            type="button"
            className="rounded-xl border border-white/10 bg-white/5 p-3 transition duration-300 hover:scale-105 hover:bg-cyan-500/20"
          >
            <Github size={18} />
          </button>

          <button
            type="button"
            className="rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 px-5 py-2 font-semibold text-white transition duration-300 hover:scale-105"
          >
            Verify Now
          </button>

        </div>

      </div>
    </motion.header>
  );
}

export default Navbar;