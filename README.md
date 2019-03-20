# nlp-jcag
A Joke Classifier and Generator using Deep Learning methods and Embeddings, for a UCL NLP Project. Unfortunately, due to time constraints and the boldness of the project proposal, we were unable to incorporate our original generative model idea (that included implementing the output of the joke scorer model - that is fully differentiable - directly in our sequence to sequence loss function for the generative model, thereby directly optimising a "score", which we hope to somewhat correlate with "funniness".

## Accompanying Poster
The following poster was presented on a project presentation day. Since teh poster had to be submitted early, it does not include the finalised results of hyperparameter testing, but gives a good overview of the project
![NLP_Poster](https://user-images.githubusercontent.com/30845187/54719292-65df9b80-4b54-11e9-98fe-e8857f3a92ed.png)

## Introduction
The field of computational humour is cross disciplinary, bringing together sociological and psychological theories.
Determining whether a piece of text is funny is a subjective and nontrivial problem. Automatic joke evaluation could be very useful in the
training of generative humour models, as well as providing a principled, scalable methodology for the evaluation of (generative) models.
We set out to automate this evaluation process by training a scoring model that predicts Reddit joke “scores”.
We sought to better understand how our models were learning and why they were not achieving better results.

## Contributions and Conclusions
Please read the attached paper for a detailed analysis of which models worked well and why, but a brief summary is that Google pretrained BERT embeddings that use a bidirectional LSTM model to capture contextual word embeddings worked better than even hyperparameter optimised "classical" Deep Learning models. CNNs worked better than LSTMs for our task. We believe that this is due to the fact that context is a key attribute to the funniness of a joke, as backed up by sociological theory: incongruity juxtaposition resolution theory posits that the moment of realising incongruity (defined by Kao et al (2013) as “perceiving a situation from different viewpoints and finding the resulting interpretations to be incompatible") is what makes a joke funny.
