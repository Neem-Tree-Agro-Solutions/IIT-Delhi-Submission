# NTAS-Progress-2021

[Neem Tree Agro Solutions](https://neemtreeagrico.in) provide farmers with knowledge, technology, marketing and extension services for improved planning for enhanced quantity and quality of produce.

# The Services

* **[Crop Recommendation](https://github.com/Neem-Tree-Agro-Solutions/IIT-Delhi-Submission/tree/master/Crop%20Recommendation%20System):**

This recommendation system will focus on giving viable options to the farmer taking into account their location and weather condition.

This System builds on top of past weather data of more than 50 years to make a weather model which can predict upto 80% accurate weather. 

* **[Crop Information](https://github.com/Neem-Tree-Agro-Solutions/IIT-Delhi-Submission/tree/master/Crop%20Information):**

New and better practices of growing crops and crop protection are displayed to the farmer in a interactive and easy to understand UI
The crop information data is researched and collected.

* **[Pest Analysis](https://github.com/Neem-Tree-Agro-Solutions/IIT-Delhi-Submission/tree/master/Pest%20Analysis%20Models):** 

Deep Learning Models have been trained for various crops with 3-4 pests and diseases for detecting pests and diseases using image recognition.
Some models perform upwards of 80%

* **[Pest Model API](https://github.com/Neem-Tree-Agro-Solutions/IIT-Delhi-Submission/tree/master/Pest_Model-API)**
This API is created to try and test the pest models. The instructions to run the API are given in the ReadMe file

* **Weather Models:** 

They are in 2 types.
- [State Wise](https://github.com/Neem-Tree-Agro-Solutions/IIT-Delhi-Submission/tree/master/State%20Wise%20Weather%20Prediction%20Models)
- [Cluster Wise](https://github.com/Neem-Tree-Agro-Solutions/IIT-Delhi-Submission/tree/master/Weather%20Prediction%20Models)

*State Wise*
Each state weather has been taken for more than 50 years and a time series model has been used to make a weather prediction model.

*Cluster Wise*
India is divided into 15 agroclimatic zones. These zones are taken into account and models for these clusters has been made.
They are beneficial over state models as clusters have similar weather conditions hence low computation power will be needed. 

# The Application

NT-Kisan Backend:
https://github.com/Neem-Tree-Agro-Solutions/MongoDB-Deployment

MongoDB Deployment on Google Kubernetes Engine
Uses:
- Statefulset for state applications like mongodb
- Replica set for data redundancy
- Persistent Storage Volume Claims for persistent and redundant data in the event of cluster failure
- Internal Load Balancer to expose to apis using database
- Shared VPC and subnet with CIDR format Ip addresses to Share Load Balancing IP

NT-Kisan-RestAPI
- Hosted on Github on a private repository (interested users can be added for viewing)

Uses:
- Custom Written API code using Node and Express server
- Mongoose as a driver for node and mongodb interface

Deployment:
- Google Kubernetes Engine
- Replica Set
- External HTTPS Load Balancer service to expose the api
- Connected to company domain for easy serving to company applications
- Uses the same VPC as mongo for easy internal secured communication

Neem Tree Kisan Application
Hosted on Github on a private repository (interested users can be added for viewing)

Uses:
- Flutter 2.0 
- Multiple Platforms one code base
- BloC Pattern for state management and state saving using hydrated bloc
- Firebase Authentication for user auth with google and phone number for one tap logins

