export default function Header() {
  return (
    <header className="header">
      <h1 className="logo">Llaqta</h1>

      <input
        type="text"
        placeholder="Buscar productos..."
        className="search-input"
      />
    </header>
  );
}