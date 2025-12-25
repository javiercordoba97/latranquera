import { Routes, Route } from "react-router-dom";
import Home from "./views/Home";
import Producto from "./views/Producto";
import Categoria from "./views/Categoria";
import ChatBox from "./components/ChatBox";

export default function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/producto/:id" element={<Producto />} />
        <Route path="/categoria/:categoria" element={<Categoria />} />
      </Routes>

      <ChatBox />
    </>
  );
}