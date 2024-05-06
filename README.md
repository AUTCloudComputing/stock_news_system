## stock news aggregation system 

Here are some features of the system:

- Automated news collection from various financial news outlets by eodhd-openAPI.

- Initial setup for integrating ChatGPT to condense news content and perform data cleaning.

 ![eodhd-system_2024-05-05_21-52-18](assets/eodhd-system_2024-05-05_21-52-18.jpg)

![eodhd-system_2024-05-05_21-53-30](assets/eodhd-system_2024-05-05_21-53-30.jpg)

![eodhd-system_2024-05-05_21-56-38](assets/eodhd-system_2024-05-05_21-56-38.jpg)

## config.py

Create a config.py file in the project root containing your EODHD APIs token.




 ```Java
    API_TOKEN = "YOUR_TOKEN"
    OPENAI_KEY = "YOUR_TOKEN"
 ```


run this project:


 ```Java
 python -m venv .venv
 . .venv/bin/activate
 . .venv/bin/activate
  pip install -r requirements.txt
  import openai
  
python app.py --host 0.0.0.0 --port 5000 --debug                

 ```
 