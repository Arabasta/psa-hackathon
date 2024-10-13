import useImage from "../hooks/useImage";
import useToday from "../hooks/useToday";
import { useEffect, useState } from "react";

export default function Home() {
  /*
   * constants for SUBMIT view - handling user input and data to and from backend
   */
  const {imageMessage, imageData, imageError, postUploadImage } = useImage();
  const [selectedFile, setSelectedFile] = useState(null);
  const [imageCaption, setImageCaption] = useState("");
  const [employees, setEmployees] = useState("");
  const [generatedImageUrl, setGeneratedImageUrl] = useState("");
  const [currentView, setCurrentView] = useState("chooseImage");

  /*
   * constants for TODAY view - handling bomen of the day
   */
  const { todayMessage, todayData, todayError, getBomenOfTheDay } = useToday();
  const [loadingTodayData, setLoadingTodayData] = useState(false); // To handle loading state


  /*
   * EVENT HANDLERS for SUBMIT view
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
   * Fetch Bo-men of the Day when the user navigates to the "TODAY" view
   */
  useEffect(() => {
    if (currentView === "today") {
      setLoadingTodayData(true);
      getBomenOfTheDay()
          .then(() => {
            setLoadingTodayData(false);
          })
          .catch((err) => {
            console.error("Error fetching Bo-men of the day:", err);
            setLoadingTodayData(false);
          });
    }
  }, [currentView]); // Fetch Bo-men data only when the "TODAY" view is active

  /*
   * onClick / onChange HANDLERS for SUBMIT view
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
      const response = await postUploadImage(formData); // Ensure this function is properly invoked
      alert("Image uploaded successfully!");
      // Check the response data and set the image URL
      if (response && response.imageData && response.imageData.image_url) {
        console.log("Image URL received:", response.imageData.image_url);
        setGeneratedImageUrl(response.imageData.image_url); // Set the generatedImageUrl
      } else {
        console.error("Image URL not found in response");
      }
    } catch (err) {
      console.error("Error uploading image:", err);
      alert("Failed to upload image.");
    }
  };

  // Function to render content based on the current view
  const renderView = () => {
    switch (currentView) {
      /*
       * SUBMIT / CHOOSE IMAGE VIEW
       */
      case "chooseImage":
        return (
            <div className="flex flex-col gap-3 row-start-2 items-center justify-center sm:items-center">
              <div>Submit your poses!</div>
              {/* Generated Image */}
              <div>
                {generatedImageUrl ? (
                    <img src={generatedImageUrl} alt="new" width={300} height={300} />
                ) : (
                    <></>
                )}
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
                <input
                    type="text"
                    placeholder="Type your caption here!"
                    className="input w-full max-w-xs"
                    onChange={handleImageCaption}
                />
              </label>

              {/* Employee Names */}
              <label className="form-control w-full max-w-xs">
                <div className="label">
                <span className="label-text">
                  Who are in this picture? <br />
                  (Type your names, separated by comma)
                </span>
                </div>
                <input
                    type="text"
                    placeholder="Type your names here!"
                    className="input w-full max-w-xs"
                    onChange={handleEmployeeNames}
                />
              </label>

              <button className="btn" onClick={handleUploadImage}>
                SUBMIT
              </button>
            </div>
        );

        /*
        * TODAY / BO-MEN OF THE DAY VIEW
        */
      case "today":
        if (loadingTodayData) {
          return <div>Loading Bo-men of the day...</div>;
        }

        if (todayError) {
          return <div>Error: {todayError}</div>;
        }

        return (
            <div className="flex flex-col gap-3 row-start-2 items-center justify-center sm:items-center">
              <h2>Bo-Men of the Day!</h2>
              {todayData?.imageURL ? (
                  <img src={todayData.imageURL} alt="Bo-men of the Day" width={300} height={300} />
              ) : (
                  <div>No image available</div>
              )}
              {todayData?.imageCaption ? <p>Caption: {todayData.imageCaption}</p> : null}
              {todayData?.fun_fact ? <p>Fun Fact: {todayData.fun_fact}</p> : null}
            </div>
        );

      /*
       * GALLERY / NEXT IMAGE VIEW
       */
      case "gallery":
        return <div>Alongside your fellow colleagues!</div>; // Placeholder for gallery content

      default:
        return <div>Invalid View</div>;
    }
  };


  return (
      <div
          className={`grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]`}
      >
        <main className="flex flex-col gap-6 row-start-2 items-center justify-center sm:items-center">
          {/* Render content based on the current view */}
          {renderView()}

          {/* Divider */}
          <div className="flex w-full flex-col border-opacity-50">
            <div className="divider m-0"></div>
          </div>

          <footer className="row-start-3 flex gap-4 items-center justify-center">
            <button className="btn" onClick={() => setCurrentView("gallery")}>
              GALLERY
            </button>
            <button className="btn" onClick={() => setCurrentView("chooseImage")}>
              CHOOSE IMAGE
            </button>
            <button className="btn" onClick={() => setCurrentView("today")}>
              TODAY
            </button>
          </footer>
        </main>
      </div>
  );
}
