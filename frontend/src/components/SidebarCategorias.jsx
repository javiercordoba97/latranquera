import { Link } from "react-router-dom";

export default function SidebarCategorias() {
  const categorias = [
    "ponchos", "bombachas", "alpargatas", "fajas", "sombreros",
    "camisas", "chalecos", "cintos", "pilcheros", "carteras",
    "mantas", "boinas", "chiripas"
  ];

  return (
    <aside className="sidebar">
      <h3>Categorías</h3>
      <ul>
        {categorias.map(cat => (
          <li key={cat}>
            <Link to={`/categoria/${cat}`}>{cat}</Link>
          </li>
        ))}
      </ul>
    </aside>
  );
}