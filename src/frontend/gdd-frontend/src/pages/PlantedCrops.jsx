import CumulativeGDDChart from '../components/CumulativeGDDChart';
// src/pages/PlantedCrops.jsx
import { useEffect, useState } from 'react';
import { fetchPlantedCrops } from '../api/api';

export default function PlantedCrops() {
  const [crops, setCrops] = useState([]);

  useEffect(() => {
    fetchPlantedCrops().then(setCrops).catch(console.error);
  }, []);

  {crops.map(pc => (
    <div key={pc.id}>
        <h3>Crop: {pc.crop}</h3>
        <CumulativeGDDChart plantedCrop={pc} />
    </div>
    ))}

  return (
    <div>
      <h1>Planted Crops + GDD</h1>
      {crops.map((pc) => (
        <div key={pc.id}>
          <h3>Crop: {pc.crop}</h3>
          <CumulativeGDDChart plantedCrop={pc} />
          <p>Plant Date: {pc.plant_date}</p>
          <ul>
            {pc.gdd.map((g) => (
              <li key={g.id}>
                {g.day}: {g.gdd.toFixed(2)}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}