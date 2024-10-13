import useImage from "../hooks/useImage";
import { useState } from "react";

export default function Home() {
  const { message, data, error, postUploadImage } = useImage(); // Properly destructuring postUploadImage
  const [selectedFile, setSelectedFile] = useState(null); // State to store the selected file
  const [imageCaption, setImageCaption] = useState(""); // Optional: State for image caption if needed
  const [employees, setEmployees] = useState(["employee1"]); // Optional: State for employees data if needed

  /*
   * EVENT HANDLERS
   */
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    console.log("File selected:", event.target.files[0]);
  };

  const handleImageCaption = (event) => {
    setImageCaption(event.target.value);
    console.log(imageCaption);
  };

  /*
   * onClick / onChange HANDLERS
   */
  const handleUploadImage = async () => {
    console.log("Upload button clicked");

    if (!selectedFile) {
      console.log("No file selected!");
      alert("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile); // Append the image file
    formData.append("image_caption", imageCaption); // Append the image caption if needed
    formData.append("employees", employees); // Append employees data if needed

    try {
      // This is where the formData gets passed to postUploadImage
      await postUploadImage(formData); // Ensure this function is properly invoked
      alert("Image uploaded successfully!");
    } catch (err) {
      console.error("Error uploading image:", err);
      alert("Failed to upload image.");
    }
  };

  return (
      <div
          className={`grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]`}
      >
        <main className="flex flex-col gap-8 row-start-2 items-center justify-center sm:items-center">
          <h1>SUBMIT PAGE</h1>

          <input
              type="file"
              accept="image/png, image/jpeg"
              onChange={handleFileChange} // Handle file selection
              className="file-input file-input-bordered w-full max-w-xs"
          />

          {/* User Upload Image*/}
          <div className="flex gap-4 items-center flex-col sm:flex-row">

            <input type="text"
                   placeholder="Type your caption here!"
                   className="input w-full max-w-xs"
                   onChange={handleImageCaption}
            />

            <button className="btn"
                    onClick={handleUploadImage}
            >
              GO!
            </button>
          </div>

          {/* Divider */}
          <div className="flex w-full flex-col border-opacity-50">
            <div className="divider m-0"></div>
          </div>

          <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
            <button className="btn">GALLERY</button>
            <button className="btn">SUBMIT</button>
            <button className="btn">TODAY</button>
          </footer>
        </main>
      </div>
  );
}
