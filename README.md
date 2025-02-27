# **GPU Stock Alert**

**v1.0.1 - Initial Release**

🔹 **Purpose**

- Made this because I have a life and can't camp out the store or spend my entire day refreshing the page. So I figured it would be nice to have something running at home or on a cloud, and to just get an alert on my phone when there is one in stock. That way if I'm at work, school, or home, I'll know when one is in stock near me. That way, if I can, I can head to the store when I get the noti. Additionally, it will only check for the models I want, specficially those at MSRP. 

🔹 **Overview**

- As I have struggled to find a 5070 TI, I decided it was a good opportunity to create a python script that just checked the stores near me, and alerted me when an MSRP Card was available. My plan is to just leave this running on my main PC, and the SMS pops up on my watch. I'm aware it's not the most efficient, but I made it in a rush

🔹 **Features**

- Refreshes this page: https://www.canadacomputers.com/en/search?s=RTX+5070+Ti, each time rotating through Burnaby, Coquitlam, Surrey, Richmond, and Vancouver Broadway. 
- Checks for Specific Models: I have it checking for the MSRP models available at the time of writing. 

🔹 **Planned Update**

- Instead of having an array that checks for the models specifically, will change it to check them based on price, that way it's automatic. 
- Improve Efficiency


🔹 **Known Bug**
- The "Pause" and "restart" sms don't work as intended, but won't necessarily affect the script. It'll keep running after you say "restart"

🔹 **Installation & Setup**

 ***Note: Will need to have ngrok installed, and a Twilio account made***
To run this project locally: 

1. **Clone the repository:**
- Create/Open a folder, right click -> More Options -> "Open in Terminal"
   ```bash
   git clone https://github.com/RRRafael25/gpuAlertScraper
   cd gpuBot
  ```
2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```
3. **Activate the virtual Envinronment:**
- On Windows:
```bash
  venv/Scripts/activate
```
- On macOS/Linux:
```bash
  source venv/bin/activate
```
4. **Install the required dependencies**
``` bash
  pip install -r requirements.txt
```

5. **Use ngrok to configure twilio**
- After setting up twillio account and phone number, auth token and token ID, run:
```bash
ngrok http 5000
```
- Copy the "https://example.ngrok-free.app" or whatever it is that comes after "Forwarding" and before the "->"
```bash
Forwarding                    https://example.ngrok-free.app -> http://localhost:5000        
```
- Go to your twilio dashboard, for your account -> Manage # Numbers -> Active -> Click on the phone # -> Configure -> Scroll down to "A message comes in." Make sure it is set to webhook, and paste what you copied earlier into the URL, and add /sms at the end. Should look like this: https://example.ngrok-free.app/sms. And lastly make sure HTTP is set to HTTP Post

***Note: You will have to repeat this anytime you close the terminal running ngrok***

6. **Your information**
- Create a .env file, copy and paste this:
ACCOUNT_ID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
PHONE_NUMBER=

- Replace with your account ID, Twilio Auth token, Twilio Phone number, and your phone number on the right of the = sign.

7. **Running the files**:

***Note: Up to this point, it should work and will check Burnaby, Coquitlam, Surrey, Richmond and Vancouver Broadway in British Columbia.***

It will also only check these models:

https://www.canadacomputers.com/en/powered-by-nvidia/269440/gigabyte-geforce-rtx-5070-ti-windforce-sff-16g-graphics-card-gv-n507twf3-16gd.html?keyword=rtx%205070%20Ti
https://www.canadacomputers.com/en/powered-by-nvidia/268823/gigabyte-geforce-rtx-5070-ti-windforce-oc-sff-16g-graphics-card-gv-n507twf3oc-16gd.html?keyword=rtx%205070%20Ti
https://www.canadacomputers.com/en/powered-by-nvidia/268304/asus-prime-geforce-rtx-5070-ti-16gb-gddr-prime-rtx5070ti-16g.html?keyword=rtx%205070%20Ti
https://www.canadacomputers.com/en/powered-by-nvidia/269441/msi-geforce-rtx-5070-ti-16g-shadow-3x-oc-16gb-gddr7-2482-mhz-pci-e-5-0-256-bit-16-pin-x-1-hdmi-2-1b-x-1-display-port-2-1b-x-3-geforce-rtx-5070-ti-16g-shadow-3x-oc.html?keyword=rtx%205070%20Ti

*For how to change location ,look further below, same as for specific models. Planning to also change looking for models so it does it by price instead of manually, so it will check based on price instead of 4 specific models, in case price changes* 

``` bash
python receivesms.py
```
- Open a new terminal

```bash 
python gpuAlertCC.py
```


I tried making the instructions as clear as possible, so this should hopefully work, you can leave it running as long as you want it to keep checking.

***To change Locations and GPU model, and/Or Product overall:***

**Product**

- To change which page, just go to the Canada Computers Search bar, type what will find your product in mind, copy and paste the irl to the "page" variable. 
***Note: This will only work for Canada Computers specifically, as it relies on their website structure. Furthermore, I have only tested this for the 5070 Ti, as it is the one I specifically want. Cannot guarantee it will work for other products as of right now, you will have to test that.***

**Location**
- Find the "storeLocations" variable, you will notice is just numbers. All you have to do is change the numbers according to the guide beneath:

Ajax: 1  
Barrie: 2  
Brampton: 4  
Brossard: 67  
Burlington: 3  
Burnaby: 56  
Cambridge: 66  
Coquitlam: 57  
Etobicoke: 5  
Gatineau: 60  
Halifax: 62  
Hamilton: 8  
Kanata: 9  
Kingston: 11  
Laval: 12  
London Masonville: 71  
Marche Central: 68  
Markham Unionville: 17  
Mississauga: 15  
Montreal: 46  
Newmarket: 18  
North York: 64  
Oakville: 69  
Oshawa: 23  
Ottawa Downtown: 44  
Ottawa Merivale: 20  
Ottawa Orleans: 21  
QC Vanier: 73  
Richmond: 58  
Richmond Hill: 26  
St Catharines: 27  
Surrey: 72  
Toronto Down Town 284: 28  
Toronto Kennedy: 29  
Vancouver Broadway: 51
Vaughan: 32
Waterloo: 33  
West Island: 35
Whitby: 34

- Just put in whatever numbers correspond to your desired locations, delete the ones that aren't and you're good to go.

**Model**
- To change the specific model, find the "validIDs" variable. It is a list of a bunch of "product_card_######." To change what models you want, search it using Canada Computers' website, it will give you their listings. Find the product you specifically want, right click on the image, then go to inspect. A new "tab" should open up, highlighting the image that you clicked. it should be something like:
```html
...
<picture>
  <img src=".......">
</picture>
...
```
- You want to just look up, line by line until you find something that looks like this: 
```html
...
<div id="product_card_269440" ...>
  ...
</div>
...
```
- Take note of the numbers, go to the validIds variable, and just replace the numbers on the existing one, and delete or add any necessary numbers. If you're searching for a different product than the 5070 Ti, you will have to delete the ones that don't belong to that product.


## ***Happy Hunting Everyone***


