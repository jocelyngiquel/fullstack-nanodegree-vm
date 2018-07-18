# ITEM CATALOG PROJECT
## Context
The current document is to help the reader to run an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Requirements
To run the application, you will need to download and install a Linux virtual machine.
In addition, you'll need to clone a github repository on your machine to ensure you have all the needed tools.
The application is based on the flask framework, running on python (Python 2.7). Python is implemented in the solution presented below, no extra steps needed on this one.

### Installing a Linux VM with Vagrant
A Linux virtual machine (VM) configuration that already contains the PostgreSQL database software has been put together. To run it, you will need to install two things on your computer (if you don't already have them):
- The **VirtualBox** VM environment
- The **Vagrant** configuration program

### Installing VirtualBox
VirtualBox is the program that runs your Linux virtual machine. [Install it from this site](https://www.virtualbox.org/wiki/Downloads). Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it.

### Installing Vagrant
Vagrant is the program that will download a Linux operating system and run it inside the virtual machine. [Install it from this site](https://www.vagrantup.com/downloads.html).
**Windows users**: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

### Bringing up the database server
Vagrant takes a configuration file called `Vagrantfile` that tells it how to start your Linux VM. [Download the Vagrantfile here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f73b_vagrantfile/vagrantfile). Put this file into a new directory (folder) on your computer. Using your terminal, change directory (with the `cd` command) to that directory, then run `vagrant up`. You should see something like the picture below.

![alt text](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57ae307b_screen-shot-2016-08-12-at-13.23.07/screen-shot-2016-08-12-at-13.23.07.png)

Now you have a server running in a Linux virtual machine. This setup is independent of any other database or web services you might have running on your computer. The VM is linked to the directory where you ran `vagrant up`.
To log into the VM, use a terminal in that same directory and run `vagrant ssh`. You'll then see something like this:

![alt text](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b38d85_screen-shot-2016-08-16-at-15.02.19/screen-shot-2016-08-16-at-15.02.19.png)

### Download the data
Connect to your github account and clone [the following repository](https://github.com/jocelyngiquel/udacity-item-catalog)

### Google based authentication and authorization set up
The application uses a Google based authentication and authorization (Google Oauth 2.0). In order to use the application, you need to create a client ID and a client secret with Google Developers Console in order to communicate with its Application Programming Interface (API) library.
To do so, visit the [Google Developers Console](https://console.developers.google.com/apis)
Choose **Credentials** from the menu on the left. Then select **Create credentials** and create an **OAuth Client ID**.
This will require zou to configure the OAuth consent screen. Name the project with any name.
When you are presented with a list of application types, choose **Web Application**.
Set the Autorised Javascript Origins as: http://localhost:8000
Set the Authorised redirect URIs as: http://localhost:8000/login and http://localhost:8000/gconnect.
Save and press the **Download JSON**
Rename the newly JSON downloaded file as **client_secrets.json** and save the file under the location /vagrant/catalog in the folder where you cloned the github repository

### Set your Google client ID in the application
In the Google Developers Console, and in the the client_secrets.json you'll find a Google Client ID referencing the newly created project.
The ID has the format ####.apps.googleusercontent.com.
Copy the CLient ID and paste it in the **login.html** file under the location /vagrant/catalog/template. In the file paste the ID line 6, at the place of "PLACE_YOUR_GOOGLE_CLIENT_ID_HERE.apps.googleusercontent.com" with the quotation marks

### Load the database
To set up the database with a sample of example data, bring up the vagrant server as pointed above.
Type `cd /vagrant/catalog` in the command line to move into the desired location.
Type `python models.py` in the command line to set up the database.
Type `python legodataloader.py` in the command line to populate the database with a data sample.

### Launch the application
In order to launch the application, type `python project.py` in the command line.
Then in your internet browser, type `http://localhost:8000/` to access the application. Note that you will need an internet connection to be able to display images.

### Disclaimer
All the content is coming from https://shop.lego.com.