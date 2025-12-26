import { Link } from "react-router-dom";
import "../styles/App.css";

export default function Home() {

  const categorias = [
    { nombre: "Ponchos", slug: "ponchos", imagen: "poncho1.jpg" },
    { nombre: "Bombachas", slug: "bombachas", imagen: "bombacha1.jpg" },
    { nombre: "Alpargatas", slug: "alpargatas", imagen: "alpargatas1.jpg" },
    { nombre: "Fajas", slug: "fajas", imagen: "faja1.jpg" },
    { nombre: "Sombreros", slug: "sombreros", imagen: "sombreros1.jpg" },
    { nombre: "Camisas", slug: "camisas", imagen: "camisa1.jpg" },
    { nombre: "Chalecos", slug: "chalecos", imagen: "chaleco1.jpg" },
    { nombre: "Cintos", slug: "cintos", imagen: "cintos1.jpg" },
    { nombre: "Boinas", slug: "boinas", imagen: "boina1.jpg" },
    { nombre: "Mates", slug: "mates", imagen: "mate1.jpg" },
    { nombre: "Materas", slug: "materas", imagen: "matera1.jpg" },
    { nombre: "Cuchillos", slug: "cuchillos", imagen: "cuchillo1.jpg" },
  ];

  const getImage = (file) =>
    new URL(`../assets/img/${file}`, import.meta.url).href;

  return (
    <div className="home-container">

      <h2 className="section-title">Nuestros Productos</h2>

      {/* GRID DE 4 COLUMNAS */}
      <div className="product-grid">
        {categorias.map(cat => (
          <Link
            key={cat.slug}
            to={`/categoria/${cat.slug}`}
            className="product-card"
          >
            <img
              src={getImage(cat.imagen)}
              alt={cat.nombre}
              className="product-image"
            />
            <h3>{cat.nombre}</h3>
          </Link>
        ))}
      </div>

    </div>
  );
}