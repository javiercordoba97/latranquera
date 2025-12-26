import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import "../styles/App.css";

export default function Producto() {
  const { id } = useParams();
  const [producto, setProducto] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/productos")
      .then(res => res.json())
      .then(data => {
        const found = data.find(p => p.id === Number(id));
        setProducto(found || null);
      })
      .catch(() => setProducto(null));
  }, [id]);

  const getImage = (file) =>
    new URL(`../assets/img/${file}`, import.meta.url).href;

  if (!producto) return <h2>Producto no encontrado</h2>;

  return (
    <div className="product-page">
      <h2>{producto.nombre}</h2>

      <img
        src={getImage(producto.imagen)}
        alt={producto.nombre}
        className="product-image-large"
      />

      <p><strong>Precio:</strong> ${producto.precio}</p>
      <p><strong>Talles:</strong> {producto.talles.join(", ")}</p>
      <p><strong>Stock:</strong> {producto.stock} unidades</p>

      <button
        className="chat-button"
        onClick={() => alert("Abrir chatbot con producto preseleccionado (lo hacemos después)")}
      >
        Consultar por este producto
      </button>
    </div>
  );
}