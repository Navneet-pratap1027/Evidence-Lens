import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Result from "./pages/Result";
import History from "./pages/History";
import Verifying from "./pages/Verifying";

function App() {
  return (
    <div className="app-background">
      {/* Background Gradients */}
      <div className="gradient-1"></div>
      <div className="gradient-2"></div>
      <div className="gradient-3"></div>

      {/* Content */}
      <div className="relative z-10">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/result" element={<Result />} />
          <Route path="/history" element={<History />} />
          <Route path="/verifying" element={<Verifying />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;