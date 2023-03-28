/**
 * To find your Firebase config object:
 * 
 * 1. Go to your [Project settings in the Firebase console](https://console.firebase.google.com/project/_/settings/general/)
 * 2. In the "Your apps" card, select the nickname of the app for which you need a config object.
 * 3. Select Config from the Firebase SDK snippet pane.
 * 4. Copy the config object snippet, then add it here.
 */
const config = {
  apiKey: "AIzaSyBJstHGp6vw92I9HIrPDUU9yMJwVReoQnU",
  authDomain: "hackathon-chat-2-5a1f1.firebaseapp.com",
  projectId: "hackathon-chat-2-5a1f1",
  storageBucket: "hackathon-chat-2-5a1f1.appspot.com",
  messagingSenderId: "1014398643350",
  appId: "1:1014398643350:web:a222821bc190c399e426b7",
};

export function getFirebaseConfig() {
  if (!config || !config.apiKey) {
    throw new Error('No Firebase configuration object provided.' + '\n' +
    'Add your web app\'s configuration object to firebase-config.js');
  } else {
    return config;
  }
}
