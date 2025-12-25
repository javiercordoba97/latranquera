import { useParams, Link } from "react-router-dom";
import "./../styles/App.css";

export default function Categoria() {
  const { categoria } = useParams();

  const products = [
    { id: 1, nombre: "Poncho de lana artesanal", precio: 45000, categoria: "ponchos" },
    { id: 2, nombre: "Camisa gaucha blanca", precio: 28000, categoria: "camisas" },
    { id: 3, nombre: "Bombacha de campo marrón", precio: 32000, categoria: "pantalones" }
  ];

  const filtered = products.filter(p => p.categoria === categoria);

  return (
    <div className="category-page">
      <h1>Categoría: {categoria}</h1>

      <div className="product-grid">
        {filtered.map(p => (
          <Link key={p.id} to={`/producto/${p.id}`} className="product-card">
            <h3>{p.nombre}</h3>
            <p>${p.precio}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}