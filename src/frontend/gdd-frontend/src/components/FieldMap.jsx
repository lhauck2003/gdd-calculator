// src/components/FieldMap.jsx
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

export default function FieldMap({ fields }) {
    //TODO: calculate center based on field locations
  const position = [38.0749, -95.4194]; // default center 

  // TODO: add ability to click on field and see details, 
  // edit field info, add a planted crop, etc.
  // use leaflet for map rendering and interactivity, with pin markers for 
  // each sample location and popups for field details, should be able to interact with
  // a corresponding samples table (PestSamplesTable.jsx, SoilSamplesTable.jsx) 
  // to highlight/select fields on the map and show details in the table, and vice versa
  return (
    <MapContainer center={position} zoom={5} style={{ height: '700px', width: '95%', margin: '0 auto' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />
      {fields.map((field) => {
        const [lng, lat] = field.geolocation.coordinates;
        return (
          <Marker key={field.id} position={[lat, lng]}>
            <Popup>Field ID: {field.id}</Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
}