import CropsTable from "../components/CropsTable";

export default function Crops(){
    return (
        // TODO:
            // - fetch crops from backend
            // - display in table (from CropsTable components)
            // - button to add new crop (opens form with name, GDD target, etc.)
        <div>
            <h1>Crops</h1>
            <CropsTable crops={[]} />
        </div>
    )
}