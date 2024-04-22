// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyD7FYEWanKHQvbegx9UXartlY2mIKLtNLQ",
  authDomain: "encrypt-51b08.firebaseapp.com",
  projectId: "encrypt-51b08",
  storageBucket: "encrypt-51b08.appspot.com",
  messagingSenderId: "1015246435132",
  appId: "1:1015246435132:web:75976ce1244fd97e81e439",
  measurementId: "G-Z0WK82RTRQ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
// Get a reference to the storage service, which is used to create references in your storage bucket
const storage = firebase.storage();
// Function to upload file to Firebase Storage
function uploadFileToStorage(file) {
  // Create a storage reference from our storage service
  const storageRef = storage.ref();

  // Upload file to storage
  const fileRef = storageRef.child(file.name);
  return fileRef.put(file)
    .then(snapshot => {
      console.log('File uploaded to Firebase Storage:', snapshot.ref.fullPath);
      // Return the download URL of the uploaded file
      return snapshot.ref.getDownloadURL();
    })
    .catch(error => {
      console.error('Error uploading file to Firebase Storage:', error);
      throw error;
    });
}

// Example usage in your client-side code (e.g., when handling file uploads)
const fileInput = document.getElementById('file-input');
fileInput.addEventListener('change', async (event) => {
  const file = event.target.files[0];
  try {
    const downloadURL = await uploadFileToStorage(file);
    console.log('Download URL:', downloadURL);
    // Send the download URL to the serverless function for further processing
    // You can use an HTTP request to send the URL to the serverless function
  } catch (error) {
    // Handle error
    console.error('Error uploading file:', error);
  }
});