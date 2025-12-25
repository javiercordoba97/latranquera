import { Routes, Route } from "react-router-dom";
import Home from "./views/Home";
import Producto from "./views/Producto";
import Categoria from "./views/Categoria";

import Header from "./components/Header";
import SidebarCategorias from "./components/SidebarCategorias";
import Footer from "./components/Footer";
import ChatBubble from "./components/ChatBubble";

export default function App() {
  return (
    <div className="app-layout">

      {/* HEADER */}
      <Header />

      <div className="content-layout">
        {/* SIDEBAR FIJA */}
        <SidebarCategorias />

        {/* CONTENIDO PRINCIPAL */}
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/producto/:id" element={<Producto />} />
            <Route path="/categoria/:categoria" element={<Categoria />} />
          </Routes>
        </main>
      </div>

      {/* FOOTER */}
      <Footer />

      {/* CHATBOT COMO BURBUJA */}
      <ChatBubble />
    </div>
  );
}