## Requirements

#### Python  
You will need to install Python 3+ and install the following modules:  pygraphviz, python-decouple, getpass, rich
`pip3 install -r requirements.txt`

#### Graphviz

You will also need to install the [Graphviz](https://graphviz.org/download/) library applicable to your OS.   

## Getting started:

1.  Rename the *creds_example.env* file to *.env*. The file is now hidden inside the current directory.

2.  Then, change the environment variables inside the .env file to match the credentials you would use to log into the devices.
Create a .txt file inside the commands folder with whatever command you want to run on each device.
Then, you need to set the `FILE` variable inside `.env` to the name of the .txt file you just created.

3.  Inside `.env` define the device IP's you want to run command on.  There are examples inside the `examples_cred.env` file on how this should be formatted.

4.  Now, navigate to the folder inside a terminal and run the `main.py` file with Python:
`python main.py` or `python3 main.py`


### Push to multiple devices at once 

1.  To run the program on multiple device sets asynchronously, you can set the `TYPE` variable equal to singlemode or multimode.  Multimode will log into devices 5x faster than singlemode which logs into devices one at a time.


