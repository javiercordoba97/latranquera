import { Link } from "react-router-dom";
import "./../styles/App.css";

export default function Home() {
  const categorias = [
    { nombre: "Ponchos", slug: "ponchos", imagen: "/img/categorias/ponchos.jpg" },
    { nombre: "Bombachas", slug: "bombachas", imagen: "/img/categorias/bombachas.jpg" },
    { nombre: "Alpargatas", slug: "alpargatas", imagen: "/img/categorias/alpargatas.jpg" },
    { nombre: "Fajas", slug: "fajas", imagen: "/img/categorias/fajas.jpg" },
    { nombre: "Sombreros", slug: "sombreros", imagen: "/img/categorias/sombreros.jpg" },
    { nombre: "Camisas", slug: "camisas", imagen: "/img/categorias/camisas.jpg" },
    { nombre: "Chalecos", slug: "chalecos", imagen: "/img/categorias/chalecos.jpg" },
    { nombre: "Cintos", slug: "cintos", imagen: "/img/categorias/cintos.jpg" },
    { nombre: "Pilcheros", slug: "pilcheros", imagen: "/img/categorias/pilcheros.jpg" },
    { nombre: "Carteras", slug: "carteras", imagen: "/img/categorias/carteras.jpg" },
    { nombre: "Mantas", slug: "mantas", imagen: "/img/categorias/mantas.jpg" },
    { nombre: "Boinas", slug: "boinas", imagen: "/img/categorias/boinas.jpg" },
    { nombre: "Chiripás", slug: "chiripas", imagen: "/img/categorias/chiripas.jpg" }
  ];

  return (
    <div className="home-container">

      {/* BANNER PRINCIPAL */}
      <div className="home-banner">
        <img
          src="/img/banner/banner1.jpg"
          alt="Llaqta Banner"
          className="home-banner-img"
        />
      </div>

      {/* CATEGORÍAS */}
      <h2 className="section-title">Categorías</h2>

      <div className="categorias-grid">
        {categorias.map(cat => (
          <Link
            key={cat.slug}
            to={`/categoria/${cat.slug}`}
            className="categoria-card"
          >
            <div className="categoria-img-wrapper">
              <img
                src={cat.imagen}
                alt={cat.nombre}
                className="categoria-img"
              />
            </div>
            <h3 className="categoria-nombre">{cat.nombre}</h3>
          </Link>
        ))}
      </div>

      {/* NOVEDADES (opcional, listo para usar) */}
      {/* 
      <h2 className="section-title">Novedades</h2>
      <div className="novedades-grid">
        {novedades.map(prod => (
          <ProductCard key={prod.id} producto={prod} />
        ))}
      </div>
      */}

    </div>
  );
}