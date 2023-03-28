/**
 * To find your Firebase config object:
 * 
 * 1. Go to your [Project settings in the Firebase console](https://console.firebase.google.com/project/_/settings/general/)
 * 2. In the "Your apps" card, select the nickname of the app for which you need a config object.
 * 3. Select Config from the Firebase SDK snippet pane.
 * 4. Copy the config object snippet, then add it here.
 */
const config = {
  apiKey: "AIzaSyDF9PCvV5dOaZNOdAVbp6AtA9bYosSrRR0",
  authDomain: "hackathon-chat-c98b9.firebaseapp.com",
  projectId: "hackathon-chat-c98b9",
  storageBucket: "hackathon-chat-c98b9.appspot.com",
  messagingSenderId: "233435732399",
  appId: "1:233435732399:web:dbaae3172d82e1c856b75a",
};

export function getFirebaseConfig() {
  if (!config || !config.apiKey) {
    throw new Error('No Firebase configuration object provided.' + '\n' +
    'Add your web app\'s configuration object to firebase-config.js');
  } else {
    return config;
  }
}
