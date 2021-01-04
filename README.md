# Rogers Pass Winter Restricted Area Status SMS V2
**For a live demo, please visit and sign up at https://rogerspass-sms.herokuapp.com/**

Rogers Pass Winter Restricted Area Status SMS is a basic site which records a user's phone number and texts them the updated Winter Restricted Areas status in Roger's Pass BC. When going skiing in the pass, it can be frustrating trying to open and navigate the government app while on the highway in and out of service trying to figure out where you can ski that morning. This app streamlines the process into a convenient SMS alert.

It's written using Flask in python3, and deployed to Heroku using Postgres as the database. Twilio handles the SMS messaging and the public API is used to pull the daily updated data. The front end is HTML with some Jinja for dyanmic message flashing with minimal CSS. V2 enables 2 way communication once a user has been signed up.

## Disclaimer
RogersPass-SMS is powered by information from Parks Canada's Rogers Pass data. There is no affiliation between this service and Parks Canada.

## Usage

To use this site, enter your phone number in the form on the landing page. As long as you have a verified North American phone number, you will be added to the list and texted in the morning when the area statuses update. After signing up you should receive a message confirming the sign-up. To receive updates, reply "update". Standard messaging rates apply.

## Limitations

Currently this is only set up for North American numbers. Due to the nature of being deployed to Heroku with a free account there is no garuntee a dyno will be running to execute the send SMS command if the site receives too many monthly requests. Also, Twilio does cost money so if this service blows up I may have to look at ways of funding to keep it going.

## Contributing

All required files minus the environment variables are included in this GitHub repo. Feel free to take this template and edit it however you would like. I would love to hear about any improvements you make! Twilio is not a free service so any and all donations are appreciated. If I receive enough donations to afford it, I will upgrade to a paid Heroku plan and garuntee uptime. Thanks for the support!

## License
[MIT](https://choosealicense.com/licenses/mit/) Free Usage
