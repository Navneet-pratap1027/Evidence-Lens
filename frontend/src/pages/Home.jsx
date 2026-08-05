import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";
import Hero from "../components/home/Hero";
import VerifyForm from "../components/verify/VerifyForm";

function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1 pt-32">
        <div className="mx-auto w-full max-w-5xl px-6">
          <Hero />
          <VerifyForm />
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default Home;