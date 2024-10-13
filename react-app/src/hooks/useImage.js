// useImage.js

import { useState } from "react";
import FastapiService from "@/services/FastapiService";

const useImage = () => {
    const [message, setMessage] = useState("");
    const [data, setData] = useState({});
    const [error, setError] = useState("");

    const postUploadImage = async (formData) => {
        try {
            const result = await FastapiService.postUploadImage(formData);
            setMessage(result.message);
            setData(result.data);
        } catch (err) {
            setError("Failed to upload image");
            console.error(err); // Log the error to the console
        }
    };

    return { message, data, error, postUploadImage };
};

export default useImage;
