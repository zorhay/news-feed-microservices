# News Feed Microservices

The News Feed service is composed of two microservices:
   
    Client Service: responsible for managing client data. 
    Subscription Service: responsible for handling subscriptions.

Both microservices use PostgreSQL databases to store their respective data. \
 The project is built using the Flask web framework for Python, along with SQLAlchemy for database management.

### Running with Docker Compose

To run the News Feed service with **Docker Compose** make sure you have **Docker** and **Docker Compose** installed on your system. \
Run the following command from the terminal to start the services:
    
    docker compose build
    docker compose up

### Tests

The project includes a test suite run with **pytest**. It covers unit tests, integration tests, and database interactions.it

### Predefined Subscription Plans

    Plan Name: Android-All
        Device: android
        Country: Unknown

    Plan Name: iOS-UK
        Device: ios
        Country: UK

    Plan Name: iOS-US
        Device: ios
        Country: US


### Accessing Swagger

    Client Service Swagger: http://localhost:3000/apidocs




- In the Swagger UI, locate the "device type" input bar.

- Type **android** in the "device type" bar and click the "Try it out!" button.

Please note that other plans may not be available for local testing due to the restriction of the local IP address. These plans may become accessible when deployed to a live environment or when using a public IP address for testing.
