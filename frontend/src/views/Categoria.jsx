import { useParams, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import "../styles/App.css";

export default function Categoria() {
  const { categoria } = useParams();
  const [productos, setProductos] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/productos")
      .then(res => res.json())
      .then(data => setProductos(data))
      .catch(() => setProductos([]));
  }, []);

  const filtered = productos.filter(p => p.categoria === categoria);

  const getImage = (file) =>
    new URL(`../assets/img/${file}`, import.meta.url).href;

  return (
    <div className="category-page">

      <h2 style={{ textTransform: "capitalize" }}>
        {categoria}
      </h2>

      {filtered.length === 0 && (
        <p>No hay productos en esta categoría.</p>
      )}

      <div className="product-grid">
        {filtered.map(p => (
          <Link
            key={p.id}
            to={`/producto/${p.id}`}
            className="product-card"
          >
            <img
              src={getImage(p.imagen)}
              alt={p.nombre}
              className="product-image"
            />
            <h3>{p.nombre}</h3>
            <p>${p.precio}</p>
          </Link>
        ))}
      </div>

    </div>
  );
}