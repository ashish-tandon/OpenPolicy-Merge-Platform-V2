import { Outlet } from "react-router-dom";
import AdminNavigation from "./components/navigation/AdminNavigation";
import Footer from "./components/footer";

function App() {
  return (
    <div className="flex flex-col min-h-screen">
      <AdminNavigation />
      <main className="flex-grow">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}

export default App;
