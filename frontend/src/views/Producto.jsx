import { useParams } from "react-router-dom";
import "./../styles/App.css";

export default function Producto() {
  const { id } = useParams();

  const products = [
    { id: 1, nombre: "Poncho de lana artesanal", precio: 45000, talles: ["Único"], stock: 8 },
    { id: 2, nombre: "Camisa gaucha blanca", precio: 28000, talles: ["S", "M", "L", "XL"], stock: 15 },
    { id: 3, nombre: "Bombacha de campo marrón", precio: 32000, talles: ["38", "40", "42", "44", "46"], stock: 10 }
  ];

  const product = products.find(p => p.id === Number(id));

  if (!product) return <h2>Producto no encontrado</h2>;

  return (
    <div className="product-page">
      <h1>{product.nombre}</h1>
      <p><strong>Precio:</strong> ${product.precio}</p>
      <p><strong>Talles:</strong> {product.talles.join(", ")}</p>
      <p><strong>Stock:</strong> {product.stock} unidades</p>

      <button
        className="chat-button"
        onClick={() => alert("Abrir chatbot con producto preseleccionado (lo hacemos después)")}
      >
        Consultar por este producto
      </button>
    </div>
  );
}