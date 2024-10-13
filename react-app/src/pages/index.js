import useImage from "../hooks/useImage";
import {useEffect, useState} from "react";

export default function Home() {
  const { message, data, error, postUploadImage } = useImage(); // Properly destructuring postUploadImage
  const [selectedFile, setSelectedFile] = useState(null); // State to store the selected file
  const [imageCaption, setImageCaption] = useState(""); // Optional: State for image caption if needed
  const [employees, setEmployees] = useState(""); // Optional: State for employees data if needed
  const [generatedImageUrl, setGeneratedImageUrl] = useState(""); //
  const [oksScore, setOksScore] = useState(""); //

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

  const handleEmployeeNames = (event) => {
    setEmployees(event.target.value);
    console.log(employees);
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
      const response = await postUploadImage(formData);  // Get the response directly
      alert("Image uploaded successfully!");
      console.log("Response received:", response);

      // Check the response data and set the image URL
      if (response && response.data && response.data.image_url) {
        console.log("Image URL received:", response.data.image_url);
        setGeneratedImageUrl(response.data.image_url);  // Set the generatedImageUrl directly from the response
        setOksScore(response.data.oks_score);  // Set the generatedImageUrl directly from the response
      } else {
        console.error("Image URL not found in response");
      }
    } catch (err) {
      console.error("Error uploading image:", err);
      alert("Failed to upload image.");
    }
  };

  return (
      <div
          className={`grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]`}
      >
        <h1>SUBMIT PAGE</h1>
        <main className="flex flex-col gap-6
        row-start-2 items-center justify-center sm:items-center">

        {/* Generated Image */}
        <div>
          {(generatedImageUrl) ?
              <div>
                <img
                    src={generatedImageUrl}
                    alt="new"
                    width={300} height={300}
                />
                <h1>Your image scored: {oksScore}</h1>
              </div>
              :
              <></>
          }
        </div>

          {/* Image Selector */}
          <input
              type="file"
              accept="image/png, image/jpeg"
              onChange={handleFileChange} // Handle file selection
              className="file-input file-input-bordered w-full max-w-xs"
          />

          {/* Image Caption */}
          <label className="form-control w-full max-w-xs">
            <div className="label">
              <span className="label-text">Image Caption</span>
            </div>
            <input type="text"
                   placeholder="Type your caption here!"
                   className="input w-full max-w-xs"
                   onChange={handleImageCaption}
            />
          </label>

          {/* Employee Names */}
          <label className="form-control w-full max-w-xs">
            <div className="label">
              <span className="label-text">Who are in this picture? {<br/>}(Type your names, separated by comma)</span>
            </div>
            <input type="text"
                   placeholder="Type your caption here!"
                   className="input w-full max-w-xs"
                   onChange={handleEmployeeNames}
            />
          </label>

          <button className="btn" onClick={handleUploadImage}>
            SUBMIT
          </button>

          {/* Divider */}
          <div className="flex w-full flex-col border-opacity-50">
            <div className="divider m-0"></div>
          </div>

          <footer className="row-start-3 flex gap-4 items-center justify-center">
            <button className="btn">GALLERY</button>
            <button className="btn">CHOOSE IMAGE</button>
            <button className="btn">TODAY</button>
          </footer>
        </main>
      </div>
  );
}
