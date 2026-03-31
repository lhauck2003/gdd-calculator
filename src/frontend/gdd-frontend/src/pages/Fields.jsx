// src/pages/Fields.jsx
import { useEffect, useState } from 'react';
import { fetchFields } from '../api/api';
import FieldMap from '../components/FieldMap';

export default function Fields() {
  const [fields, setFields] = useState([]);

  useEffect(() => {
    fetchFields().then(setFields).catch(console.error);
  }, []);

  return (
    <div>
      <h1>All Fields</h1>
      <FieldMap fields={fields} />
    </div>
  );
}