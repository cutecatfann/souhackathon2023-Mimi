# Shakespeare Chat Room

Join our chatroom with the link *https://hackathon-chat-c98b9.web.app/* and have fun with your friends talking like Shakespearerian lunatics! It's a fun way to kill time and also maybe kill your starcrossed lover! Or if you want to ruin the fun, you can also talk in normal English... I'm not your dad.

This code was loosely inspired by this repo: *https://github.com/firebase/codelab-friendlychat-web*

It also builds off of this training model: *https://github.com/Jmkernes/Shakespeare-Translator*

For actual implementation we would train our own model, but given the time constraints of the Hackathon, we decided to use a pretrained model.

# Collaborators:
This was a team effort between Mimi Pieper and Sergio Mendoza. Mimi's Github username is cutecatfann, and Sergio's username is DogeLovesHipster

# NOTE
The Bard function is currently malfunctioning due to flask backend errors, which means that it is not displaying the translated Shakespeare in the chat. The translator works, just not in the chat. As such, appreciate the chat for what it is and know that the AI does work. We would have made it work, but we ran out of time.

## Summary of Code
Our code is a Firebase hosted web based chat application. It is hosted using a combination of Firebase and Google Cloud Platform along with GCP storage and Google Authentication. It uses tenserflow to tokenize standard English into Shakespearean English. It utilizes faithful translation which uses beam search to attempt to find the most probable Shakespearian translation. It therefore allows the user to either input a message in standard English, or enter a message to be translated into Shakespearean English, or enter an image to be shared in the chat. The AI model utilizes a Flask backend, and connects to a React front end, and is facilitated with Firebase.
___

## Requirements for Replication
-  Python
 - Firebase
 - React
 - Node.js
 - Tensorflow
 - Npm
 - Flask

## How To Run It
Either go to the chat room, and play with it there, or go replicate in Firebase.

### Firebase Project Setup
* Clone this code into your IDE and CD open the chat folder
* Go to the Firebase console, and Add project. Do no enable Google Analytics. 
* Click the web icon to create a new Firebase web app, then register the app
* Copy the configuration object for the app that pops up (just the JS object), and pase it into firebase-config.js. 
* Enable Google Sign in by clicking Authentication in the Firebase console, then click Sign-In method tab
* Enable Google sign-in provider, then select save
* Fill in the text boxes with the name of your app and your email
* Go to Google Cloud Console and Enter API and Services, then configure the OAuth 
* Enable Cloud Firestore by clicking Firestore Database. Create a database in Test mode and create
* Enable Storage by clicking storage and enable it in Test mode. It may be already enabled for you

### Connect to Firebase
* Within the chat folder run the following commands: 
- npm -g install firebase-tools
- firebase --version
- firebase login
- firebase use --add // Here, select the project you created above. Set the alias to default

### Deploy the App
- Run this command: firebase deploy --except functions

Yay! You are now running your own Firebase chat app
