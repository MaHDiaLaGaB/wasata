import Address from "./Address";
import Home from "./Home";
import PaymentDetails from "./PaymentDetails";
import Navbar from "./components/Global/Navbar/Navbar";
import About from "./components/about/About";
import { BrowserRouter, Route, Routes } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <header className="App-header">  
        <Navbar/>
      </header>
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/address" element={<Address/> } /> 
        <Route path="/payment" element={<PaymentDetails/> } />
        <Route path={`/about`} element={<About/>} />
      </Routes>
    </BrowserRouter> 
  );
}

export default App;
