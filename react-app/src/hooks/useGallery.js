import { useState } from "react";
import FastapiService from "@/services/FastapiService";

const useGallery = () => {
    const [galleryMessage, setMessage] = useState("");
    const [galleryData, setData] = useState({});
    const [galleryError, setError] = useState("");

    const getNextImage = async () => {
        try {
            const result = await FastapiService.getNextImage();
            setMessage(result.message);
            setData(result.data);
            return result;  // Return the result so it can be used directly
        } catch (err) {
            setError("Failed to get gallery image");
            console.error(err); // Log the error to the console
            throw err;  // Re-throw the error to be caught in the component
        }
    };


    return { galleryMessage, galleryData, galleryError, getNextImage };
};

export default useGallery;