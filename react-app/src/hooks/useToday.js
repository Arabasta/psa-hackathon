import { useState } from "react";
import FastapiService from "@/services/FastapiService";

const useToday = () => {
    const [todayMessage, setMessage] = useState("");
    const [todayData, setData] = useState({});
    const [todayError, setError] = useState("");

    const getBomenOfTheDay = async (formData) => {
        try {
            const result = await FastapiService.getBomenOfTheDay(formData);
            setMessage(result.message);
            setData(result.data);
            return result;  // Return the result so it can be used directly
        } catch (err) {
            setError("Failed to get Bomen of the day");
            console.error(err); // Log the error to the console
            throw err;  // Re-throw the error to be caught in the component
        }
    };

    return { todayMessage, todayData, todayError, getBomenOfTheDay };
};

export default useToday;