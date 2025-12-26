  <h1>La Tranquera — Chatbot + Catálogo de Productos</h1>

  <p>
    La Tranquera es un proyecto fullstack que combina un 
    <strong>chatbot inteligente</strong> con un 
    <strong>catálogo de productos tradicional</strong>, pensado para ofrecer una experiencia de compra más humana, conversacional y cercana al estilo rural argentino.
  </p>

  <p>
    El objetivo principal del proyecto es el <strong>chatbox</strong>, capaz de interpretar mensajes del usuario, responder de forma natural y guiar la navegación del catálogo.
  </p>

  <hr />

  <h2>Tecnologías utilizadas</h2>

  <h3>Frontend</h3>
  <ul>
    <li>React + Vite</li>
    <li>JavaScript (ES6+)</li>
    <li>CSS modular y responsive</li>
    <li>Fetch API para comunicación con el backend</li>
    <li>LocalStorage para persistencia del <code>user_id</code></li>
  </ul>

  <h3>Backend</h3>
  <ul>
    <li>Python</li>
    <li>FastAPI</li>
    <li>Uvicorn (ASGI)</li>
    <li>Pydantic para validación</li>
    <li>CORS Middleware</li>
    <li>Estructura modular escalable</li>
  </ul>

  <h3>Infraestructura / Deploy</h3>
  <ul>
    <li>Render para el backend (FastAPI)</li>
    <li>Vercel para el frontend (React/Vite)</li>
    <li>Arquitectura separada comunicada vía HTTP</li>
  </ul>

  <hr />

  <h2>Objetivo principal del proyecto</h2>

  <p>
    El corazón de La Tranquera es su <strong>chatbox</strong>, diseñado para funcionar como un vendedor real:
  </p>

  <ul>
    <li>Responde preguntas del usuario</li>
    <li>Recomienda productos</li>
    <li>Interpreta categorías y palabras clave</li>
    <li>Mantiene un <code>user_id</code> único por sesión</li>
    <li>Devuelve respuestas naturales y contextualizadas</li>
  </ul>

  <p>
    El chatbot se comunica con el backend mediante el endpoint <code>/chat/</code>, que procesa cada mensaje y devuelve la respuesta adecuada.
  </p>

  <hr />

  <h2>Funcionalidades principales</h2>

  <ul>
    <li>Catálogo de productos organizado por categorías</li>
    <li>Chatbox interactivo con lógica personalizada</li>
    <li>Persistencia de sesión por navegador</li>
    <li>API REST con endpoints para:
      <ul>
        <li><code>/chat/</code> — interacción con el bot</li>
        <li><code>/productos</code> — listado de productos</li>
      </ul>
    </li>
    <li>Diseño visual inspirado en la estética rural argentina</li>
    <li>Arquitectura lista para escalar</li>
  </ul>

  <h2>Cómo correr el proyecto localmente</h2>

  <h3>Desde el Frontend</h3>
  <pre>
npm run dev
  </pre>

</body>
</html>
