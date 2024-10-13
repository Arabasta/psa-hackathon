import axios from 'axios';
import { API_BASE_URL } from './base_url';

const axiosInstance = axios.create({
    baseURL: API_BASE_URL,
});

export default axiosInstance;