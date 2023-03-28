
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
