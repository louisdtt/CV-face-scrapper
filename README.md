# CV-face-scrapper
Extracting faces with computer vision
# Quick start
- Run : `pip install -r requirements.txt --user`  
- If you have issues with the wheel run : `pip install --upgrade pip setuptools wheel`
# Image downloader
- The app is using Microsoft Bing image API to download images based on user input
- In order to use this service you need to subscribe to bing search service on Azure (free) and setup your API key in the `.env`
- To do so just run `python search_bing_api.py --query "query" --output location` where "query" is your keywords and location is the folder where you want the images saved
# Face scrapper
- Run : `pip install -r requirements.txt --user`  
- Put your images in a `images` folder at the root of the application  
- Run `python face_scrapper.py` , it will extract every faces to a `faces` folder  
# To do
- Dockerize