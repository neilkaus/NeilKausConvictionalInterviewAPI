This is my submission for the Convictional Interview API challenge.

I made two primary assumptions the first was that the data would be fully updated from the Product API upon each request to ensure up to date information. The second was in regards to the 404 exception for /products and /store/inventory for which I decided would be thrown if no products could be found from the Product API.

This API was built in the REST API architectural style using FastAPI. The full documentation can be accessed at /docs or alternatively /redoc.

Testing the API can be done locally via Docker. In the directory /NeilKausConvictionalInterviewAPI run the docker build command:

docker build -t neil_kaus_convictional_api_image .

Followed by the run command (uvicorn is set to host at 0.0.0.0 using port 80, map whichever port you choose on your local machine to this port in the container):

docker run -p 127.0.0.1:80:80 --name neil_kaus_convictional_api_container -d neil_kaus_convictional_api_image

Thanks for taking the time to look at my code!
