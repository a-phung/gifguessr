# gifGuessr

## Table of contents
* [General Info](#general-info)
* [Website Details](#website-details)
* [Technologies](#technologies)

## General Info
gifGuessr is an image-word guessing game involving anagrams, rhymes, synonyms, and syllables! Guesses are entered in the text box and a correct guess will turn the box border from a red outline to a green outline. Hints are provided for each of the three words that are associated with the related image.\
\
The software project is designed using the microservices architecture. The project uses a teammate's microservice for word hints, as well as an accompanying image microservice to fetch the related image and words. The image microservice is called to fetch a random image and to parse the image description for three relevant words associated with the image to guess. These words are then passed to a teammate's microservice which returns hints related to each of the three words, and then the main application handles displaying the image and the three words alongside the respective hints. The image microservice is listed in the website details section and the repository is located here: https://github.com/a-phung/image-microservice.

## Website Details
Main application link: https://gifguessr.herokuapp.com/
Microservice link: https://image-microservice-us.herokuapp.com/

https://user-images.githubusercontent.com/72109757/171080161-da1a60ca-ba7e-4860-92a8-66408b0841ec.mp4

## Technologies
This project is created with:
* Python, Flask
* Heroku
* Microservices
	
