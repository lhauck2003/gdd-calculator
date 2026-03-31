import './App.css';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import NavBar from './components/NavBar';
import Crops from './pages/Crops';
import Farms from './pages/Farms';
import PlantedCrops from './pages/PlantedCrops';
import Samples from './pages/Samples';
import Fields from './pages/Fields';

const pageLinks = [
  { key: 'farms', label: 'Farms', to: '/farms' },
  { key: 'fields', label: 'Fields', to: '/fields' },
  { key: 'planted-crops', label: 'Planted Crops', to: '/planted-crops' },
  { key: 'crops', label: 'Crops', to: '/crops' },
  { key: 'samples', label: 'Samples', to: '/samples' },
];

function App() {
  return (
    <Router>
      <NavBar pageLinks={pageLinks} />
      <Routes>
        <Route path="/" element={<Navigate replace to="/fields" />} />
        <Route path="/fields" element={<Fields />} />
        <Route path="/planted-crops" element={<PlantedCrops />} />
        <Route path="/crops" element={<Crops />} />
        <Route path="/farms" element={<Farms />} />
        <Route path="/samples" element={<Samples />} />
      </Routes>
    </Router>
  );
}

export default App;
