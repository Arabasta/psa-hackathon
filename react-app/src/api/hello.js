// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import axiosInstance from '../config/axiosInstance';

const getFastapiHealth = async () => {
  try {
    const response = await axiosInstance.get('/health');
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error('Error fetching health', error);
    throw error;
  }
};

export default getFastapiHealth;
