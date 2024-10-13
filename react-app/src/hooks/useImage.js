import { useState } from "react";
import FastapiService from "@/services/FastapiService";

const useImage = () => {
    const [imageMessage, setMessage] = useState("");
    const [imageData, setData] = useState({});
    const [imageError, setError] = useState("");

    const postUploadImage = async (formData) => {
        try {
            const result = await FastapiService.postUploadImage(formData);
            setMessage(result.message);
            setData(result.data);
            return result;  // Return the result so it can be used directly
        } catch (err) {
            setError("Failed to upload image");
            console.error(err); // Log the error to the console
            throw err;  // Re-throw the error to be caught in the component
        }
    };


    return { imageMessage, imageData, imageError, postUploadImage };
};

export default useImage;
