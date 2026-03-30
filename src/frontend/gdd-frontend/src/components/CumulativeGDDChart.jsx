// TODO: Create a function that plots cumulative GDD based on
// from a planted crop. It should take in a planted crop object (json)
// which comes from the backend and then plot the cumulative GDD based
// on that object. The cumulative GDD should be plotted against the date.

import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, Legend, ResponsiveContainer } from 'recharts';

export default function CumulativeGDDChart({ plantedCrop }) {
    // calculate cumulative GDD
    const sortedGDD = [...plantedCrop.gdd].sort((a,b) => new Date(a.date) - new Date(b.date));
    let cumulative = 0;
    const data = sortedGDD.map(gdd => {
        cumulative += gdd.gdd;
        return ({
            date: gdd.date,
            cumulativeGDD: cumulative
        })
    });

    return(
        <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="cumulativeGDD" stroke="#8884d8" activeDot={{ r: 8 }} />
            </LineChart>
        </ResponsiveContainer>
    )
}