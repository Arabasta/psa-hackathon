import {useState, useEffect} from "react";
import FastapiService from "@/services/FastapiService"

const useHealth = () => {
    const [healthStatus, setHealthStatus] = useState('');
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    const getHealth = async () => {
        try {
            const result = await FastapiService.getFastapiHealth();
            setHealthStatus(result);  // Set the result to the state
            setError(null)
        } catch (err) {
            setError('Failed to fetch health status');
            console.error(err);  // Log the error to the console
        } finally {
            setLoading(false);  // Set loading to false when request is done
        }
    }

    useEffect(() => {
        getHealth();
    }, []);

    return {healthStatus, error, loading};
};

export default useHealth;