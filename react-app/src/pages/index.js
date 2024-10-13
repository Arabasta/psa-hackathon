import Image from "next/image";
import useHealth from "../hooks/useHealth";
import useImage from "../hooks/useImage";
import {useState, useEffect} from "react";

export default function Home() {
  const {message, data, error} = useImage();

  const handleUploadImage = () => {
    postUploadImage()
  }

  return (
      <div
          className={`grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]`}
      >
        <main className="flex flex-col gap-8 row-start-2 items-center justify-center sm:items-center">

          <input
              type="file"
              accept="image/png, image/jpeg"
              className="file-input file-input-bordered w-full max-w-xs"
          />

          <div className="flex gap-4 items-center flex-col sm:flex-row">
            <button className="btn">Show Next Photo</button>

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
