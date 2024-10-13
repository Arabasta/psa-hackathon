import {useState, useEffect} from "react";
import FastapiService from "@/services/FastapiService"

const useImage = (image, image_caption, employees) => {
    const [message, setMessage] = useState('');
    const [data, setData] = useState({});
    const [error, setError] = useState('');

    const postUploadImage = async (image, image_caption, employees) => {
        try {
            const result = await FastapiService.postUploadImage(image, image_caption, employees);
            // Set the result to the state
            setMessage(result.message);
            setData(result.data)
        } catch (err) {
            setError('Failed to upload image');
            console.error(err);  // Log the error to the console
        }
    }

    const getImageData = async (image_id) => {
        try {
            const result = await FastapiService.getImageData(image_id);
            // Set the result to the state
            setMessage(result.message);
            setData(result.data)
        } catch (err) {
            setError('Failed to get data from image_id: '+image_id);
            console.error(err);  // Log the error to the console
        }
    }

    const getRandomImage = async () => {
        try {
            const result = await FastapiService.getRandomImage();
            // Set the result to the state
            setMessage(result.message);
            setData(result.data)
        } catch (err) {
            setError('Failed to get random image');
            console.error(err);  // Log the error to the console
        }
    }

    const getNextImages = async () => {
        try {
            const result = await FastapiService.getNextImages();
            // Set the result to the state
            setMessage(result.message);
            setData(result.data)
        } catch (err) {
            setError('Failed to get next images');
            console.error(err);  // Log the error to the console
        }
    }

    return {message, data, error};
}

export default useImage;