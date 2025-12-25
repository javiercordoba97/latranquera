import { Link } from "react-router-dom";
import "./../styles/App.css";

export default function Home() {
  const products = [
    { id: 1, nombre: "Poncho de lana artesanal", precio: 45000, categoria: "ponchos" },
    { id: 2, nombre: "Camisa gaucha blanca", precio: 28000, categoria: "camisas" },
    { id: 3, nombre: "Bombacha de campo marrón", precio: 32000, categoria: "pantalones" }
  ];

  return (
    <div className="home-container">
      <h1>Llaqta — Ropa de campo</h1>

      <h2>Categorías</h2>
      <div className="category-grid">
        <Link to="/categoria/ponchos" className="category-card">Ponchos</Link>
        <Link to="/categoria/camisas" className="category-card">Camisas</Link>
        <Link to="/categoria/pantalones" className="category-card">Pantalones</Link>
      </div>

      <h2>Productos destacados</h2>
      <div className="product-grid">
        {products.map(p => (
          <Link key={p.id} to={`/producto/${p.id}`} className="product-card">
            <h3>{p.nombre}</h3>
            <p>${p.precio}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}