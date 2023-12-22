import Header from "./components/Header";
import Home from "./components/Home";
import About from "./components/About";
import SingUp from "./components/SingUp";
import Login from "./components/Login"
import { Route, Routes } from "react-router-dom";

export default function App() {
  return (
    <div className="App">
      <Header />
      <Routes>    
        <Route path="/resgister" element={<SingUp />}/>
        <Route path="/login" element={<Login />}/>
        <Route path="/" element={<Home />}/>
        <Route path="/about" element={<About />}/>
       </Routes>

    </div>
  );
}


