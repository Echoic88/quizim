[![Build Status](https://travis-ci.org/Echoic88/quizim.svg?branch=master)](https://travis-ci.org/Echoic88/quizim)

# Quizim
The website is a fun way for friends to create and share quizes while keeping score against each other. Internet quizes are usually designed in a multiple choice format however this does not work if friends want to create quizes to play amongst themselves. There's added pressure in deciding wrong answers in addition to correct answers which is off-putting and adds work to creating quizes. Quizim is designed with a simple Question/Answer format just like when friends quiz each other in person. In addition a site owner can design custom curated quizes which general users can purchase.  

## UX
### Features
* Play quiz - Play quizes designed by other users by selecting a quiz either from the Home page which displays the most recent uploaded quizes or by navigating to the Quiz page where all user-created quizes are available to play. On selection of a quiz the user fills out a Question/Answer form and on submission the user is presented with their results.  
Answers submitted by the player is compared with the correct answer with both being formatted removing spaces, punctuation and leading article words ("the", "a", "an") and converted to lowercase. For example, if the correct answer is "X-Men" then player answers of "xmen", "The X-Men", "Xmen" would all be counted as correct.

* Create quiz - Button to create Quiz accessible from Home page for logged in users or from the Quiz page. User is presented with a Question/Answer with form withg variable rows to allow them to create quizes with any number of questions.

* Store - Allows users to purchase quizes curated by the site owner. On checkout profile details (name, address)provided by the user are selected by default as the cardholder details. This can be changed by amending the card holder details form.

* Statistics - The site provides basic stats for the performance including score for each quiz played, number of quizes played, percentage of questions answered correctly as well as a graph in the User Area displaying performance over the most recent five quizes played.

* Notifications - From the Userarea a user may select to receive notifications when a new quiz is uploaded.

Wireframes used are available in the ProjectDocuments folder.
https://github.com/Echoic88/quizim/tree/master/ProjectDocuments

### Features left to implement

* Player can rate quizes.
* Add categories to quizes so a user can assign a category to a quiz.
* Add categories to questions for quizes similar to popular quiz boardgames.
* Ability for user to create social media style groups.
* Timer and stopwatch functions when quizes are played.
* Additional statistics based on timed quizes e.g. weighting player performance in a quiz by time taken to answer.
* Add additional graphs to user area based on the above.
* Dropzone for user profile picture in Userarea.

## Testing


## Technologies used
* Django  
https://www.djangoproject.com/  
Web development framework

* Heroku  
https://www.heroku.com/platform  
Host the django app and PostGreSQL database

* Bootstrap
Used primarily for responsive page design.

* AWS Simple Email Service  
https://aws.amazon.com/ses/  
Email sending service for registration confirmation, password reset and user notifications

* AWS S3  
https://aws.amazon.com/s3/  
Host static css, js and media files 


## Deployment

## Credits
In addition to Code Insititute lessons the following sites were used extensively to research functionality in designing this site.

* Django documentation
https://docs.djangoproject.com/en/3.0/
* Simple Is Better Than Complex
https://simpleisbetterthancomplex.com/
* MDN Django Tutorial
https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Tutorial_local_library_website


## Image credits
* Question Mark logo from Clipart Library  
http://clipart-library.com/clipart/pTqre5xac.htm
* Question mark background image from vecteezy.com  
https://www.vecteezy.com/vector-art/92726-question-mark-background-vector
* Default profile picture (question-mark-profile-temp.jpg)
https://www.collaborativepracticesimcoecounty.com/what-do-you-want/question-mark/

### Acknowledgments
Inspiration from this project came primarily from family and friends that live abroad. Many of my friends and family enjoy quizing each other off the top of their head when on calls or on the rare occassions when they meet up.
