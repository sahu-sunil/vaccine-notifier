import requests
from datetime import datetime
import time


age = 28
pincodes = ["452006", "452001"]
num_days = 2
wait_time = 60 # seconds


print("Starting search for Covid vaccine slots!")

today = datetime.today().strftime("%d-%m-%Y") 

while True:
    is_available = False  

    for pincode in pincodes:   
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={}&date={}".format(pincode, today)
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 
        try:
            result = requests.get(URL, headers=header)
            result.raise_for_status()
        except Exception as exc:
            print(f"exception occurred {exc}")
        response_json = result.json()
        if response_json.get("sessions"):
            for session in response_json["sessions"]:
                if (session["min_age_limit"] <= age and session["available_capacity"] > 0 ) :
                    print('Pincode: ' + pincode)
                    print("Available on: {}".format(today))
                    print("\t", session["name"])
                    print("\t", session["block_name"])
                    print("\t Price: ", session["fee_type"])
                    print("\t Availablity : ", session["available_capacity"])

                    if(session["vaccine"] != ''):
                        print("\t Vaccine type: ", session["vaccine"])
                    print("\n")
                    is_available = True
            
    if not is_available:
        print("No Vaccination slot available!")
        time.sleep(wait_time)
        print(f"Retrying after {wait_time} seconds ")
    else:
        print("Search Completed!")
        break
