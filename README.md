Overview
This project implements a product recommendation system for an e-commerce application using FastAPI and a Language Model (LLM). The system provides personalized product recommendations based on user behavior and product descriptions.

Features
Personalized Recommendations: Uses user behavior and product descriptions to generate dynamic recommendations.
FastAPI Backend: A high-performance backend for handling requests and serving recommendations.
LLM Integration: A smaller, efficient language model that generates recommendations based on data input.
Setup
Prerequisites
Python 3.x
FastAPI
Uvicorn (for running the FastAPI app)
Required Python libraries (listed in requirements.txt)

Installation
Clone the repository:

```git clone <repository-url>```

Navigate to the project directory:

```cd <project-directory>```

Install the dependencies:

```pip install -r requirements.txt```

Running the Application
Start the FastAPI server:

```uvicorn app.main:app --reload```

The application will be accessible at http://127.0.0.1:8000.

Note: make sure to activate the environment

Testing the API with Postman
To test the product recommendations, you can use Postman by sending a POST request to the /recommendations endpoint with a JSON payload.

Open Postman and set the request method to POST.

Enter the following URL in the Postman URL field:

``` http://127.0.0.1:8000/recommendations ```

In the Body tab of Postman, select raw and choose JSON from the dropdown. Then, paste the following JSON input 

**Input**

```
 {
    "user_id": "1",
    "browsing_history": ["Fitness"]
}
```

Click Send to make the request. If everything is set up correctly, you should receive a JSON response with product recommendations.
It gives the following 

**output:**

```
{
    "user_id": "1",
    "recommendations": [
        {
            "id": 3,
            "name": "Yoga Mat",
            "category": "Fitness",
            "description": "Eco-friendly non-slip yoga mat for all fitness levels.",
            "price": 50.0
        },
        {
            "id": 4,
            "name": "Resistance Bands",
            "category": "Fitness",
            "description": "Set of resistance bands for home workouts.",
            "price": 30.0
        }
    ]
}
```

**Verifying the Output**

To verify that the product recommendation system is working as expected, check the output_samples file in the repository. This file contains sample outputs that demonstrate the system’s functionality.
After testing the /recommendations endpoint with Postman, you can compare the actual output with the samples provided in the output_samples file. Iu ploaded them for sample tests I have done to show you as an example proof.
The file is located in the root directory 
