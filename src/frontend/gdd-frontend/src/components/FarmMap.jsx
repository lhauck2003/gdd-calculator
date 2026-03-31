// src/components/FieldMap.jsx
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

export default function FarmMap({ farm }) {
    //TODO: calculate center based on farm locations
  const position = [38.0749, -95.4194]; // default center 

  // TODO: add ability to click on field and see details, 
  // edit field info, add a planted crop, etc.
  // use leaflet for map rendering and interactivity, with area markers for 
  // each field location and popups for field details, should be able to interact with
  // a corresponding fields table (FieldsTable.jsx) to highlight/select fields on the 
  // map and show details in the table, and vice versa
  // also should have the capability to add a field via the map, 
  // by adding a polygon shape to the map, and then inputting field details in a form, 
  // and then saving to the backend and updating the map and table views accordingly
  return (
    <MapContainer center={position} zoom={5} style={{ height: '700px', width: '95%', margin: '0 auto' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />
      {fields.map((field) => {
        const [lng, lat] = farm.location.coordinates;
        return (
          <Marker key={farm.id} position={[lat, lng]}>
            <Popup>Farm ID: {farm.id}</Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
}