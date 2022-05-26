import React from "react";
import { Form, useActionData, useTransition } from "@remix-run/react";
import { Ballet } from "~/components/illustrations/ballet";
import type { ActionFunction } from "@remix-run/node";
import {
  unstable_createMemoryUploadHandler as createMemoryUploadHandler,
  unstable_parseMultipartFormData as parseMultipartFormData,
  json,
} from "@remix-run/node";
import { Meditation } from "~/components/illustrations/meditation";

export const action: ActionFunction = async ({ request }) => {
  const uploadHandler = createMemoryUploadHandler();
  const formData = await parseMultipartFormData(request, uploadHandler);
  const image = formData.get("img");
  console.log(
    "🚀 ~ file: index.tsx ~ line 15 ~ constaction:ActionFunction= ~ image",
    image
  );

  const res = await fetch("http://localhost:8000/predict", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((json) => json.result);

  console.log(res);

  if (!image || typeof image === "string") {
    return json({
      error: "something wrong",
    });
  }

  return json({
    imgSrc: image.name,
    res,
  });
};

function FileUpload() {
  const [previewUrl, setPreviewUrl] = React.useState("");
  console.log(
    "🚀 ~ file: index.tsx ~ line 7 ~ FileUpload ~ previewUrl",
    previewUrl ? "cc" : "u la tr"
  );

  return (
    <div className="sm:max-w-lg w-full p-10 bg-white rounded-xl z-10">
      <div className="text-center">
        <h2 className="mt-5 text-3xl font-bold text-gray-900">Image Upload!</h2>
        <p className="mt-2 text-sm text-gray-400">
          Lorem ipsum is placeholder text.
        </p>
      </div>
      <Form
        encType="multipart/form-data"
        className="mt-8 space-y-3"
        method="post"
      >
        <div className="grid grid-cols-1 space-y-2">
          <label className="text-sm font-bold text-gray-500 tracking-wide">
            Gắn đồ vào đây
          </label>
          <div className="relative flex items-center justify-center w-full">
            <label className="relative flex flex-col rounded-lg border-4 border-dashed w-full h-60 p-10 group text-center">
              {previewUrl ? (
                <div className="relative w-4/5">
                  <img
                    alt="preview"
                    src={previewUrl}
                    className="object-cover object-center w-full"
                  />
                </div>
              ) : (
                <div className="h-full w-full text-center flex flex-col items-center justify-center">
                  <p className="pointer-none text-gray-500 ">
                    <span className="text-sm">Drag and drop</span> files here{" "}
                    <br /> or from your computer
                  </p>
                </div>
              )}
              <input
                type="file"
                name="img"
                className="hidden"
                accept="image/*"
                onChange={(event) => {
                  console.log(
                    "🚀 ~ file: index.tsx ~ line 41 ~ FileUpload ~ event",
                    event.currentTarget.files
                  );
                  const files = event.currentTarget.files;

                  if (files) setPreviewUrl(URL.createObjectURL(files[0]));
                }}
              />
            </label>
          </div>
        </div>
        <div>
          <button
            type="submit"
            className="my-5 w-full flex justify-center bg-red-500/50 text-gray-100 p-4  rounded-full tracking-wide font-semibold  focus:outline-none focus:shadow-outline hover:bg-red-400/75 shadow-lg cursor-pointer transition ease-in duration-300"
          >
            Upload
          </button>
        </div>
      </Form>
    </div>
  );
}

type ActionData = {
  errorMsg?: string;
  imgSrc?: string;
  res?: Record<string, string>;
};

// classification = ['airplane', 'automobile', 'bird','cat','deer','dog','frog','horse','ship','truck']

export default function Index() {
  const data = useActionData<ActionData>();
  const transition = useTransition();
  const isSubmitted = transition.state !== "submitting" && !!data?.res;
  const isSubmitting = transition.submission?.formData.get("img");

  return (
    <div className="flex flex-col justify-center items-center h-screen">
      <div className="flex justify-around w-full">
        <div className="w-1/3">
          <FileUpload />
        </div>
        <div className="w-1/3 flex items-center justify-center">
          {isSubmitting ? (
            <Meditation size="100%" />
          ) : (
            <Ballet size="100%" flip={isSubmitted} />
          )}
        </div>
        <div className="w-1/3 flex p-10">
          <table className="w-full table-fixed text-left rounded-3xl shadow-lg">
            <thead>
              <tr className="border-b-2">
                <th className="p-5">Dataset</th>
                <th className="p-5">Prediction</th>
              </tr>
            </thead>
            <tbody>
              {data?.res
                ? Object.entries(data.res).map(([key, value]) => (
                    <tr key={key} className="border-b-2 last-of-type:border-0">
                      <td className="p-5 border-r-2">{key}</td>
                      <td className="p-5">{value}</td>
                    </tr>
                  ))
                : null}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
