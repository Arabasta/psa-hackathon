// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import axiosInstance from '../config/axiosInstance';

const getFastapiHealth = async () => {
  const response = await axiosInstance.get('/health');
  return response.data;
};

const postUploadImage = async (formData) => {
  const response = await axiosInstance.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

const getImageData = async (image_id) => {
  const response = await axiosInstance.get('/image',image_id);
  return response.data;
}

const getRandomImage = async () => {
  const response = await axiosInstance.get('/random_image');
  return response.data;
}

const getNextImages = async () => {
  const response = await axiosInstance.get('/next_images');
  return response.data;
}

const getBomenOfTheDay = async () => {
  const response = await axiosInstance.get('/bomen_of_the_day');
  return response.data;
}

const FastapiService ={
  getFastapiHealth,
  postUploadImage,
  getImageData,
  getRandomImage,
  getNextImages,
  getBomenOfTheDay
};

export default FastapiService;
