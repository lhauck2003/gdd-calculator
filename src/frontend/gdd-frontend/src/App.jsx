import './App.css';
import { BrowserRouter as Router, Routes, Route, Link} from 'react-router-dom';
import PlantedCrops from './pages/PlantedCrops';
import Fields from './pages/Fields';

function App() {
  return (
    <Router>
      <nav>
        <Link to="/fields">Fields</Link> | <Link to="/planted-crops">Planted Crops</Link>
      </nav>
      <Routes>
        <Route path="/" element={<div>Hello, World!</div>} />
        <Route path="/fields" element={<Fields />} />
        <Route path="/planted-crops" element={<PlantedCrops />} />
      </Routes>
    </Router>
  );
}

export default App;