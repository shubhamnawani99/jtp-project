# Book Recommender System

The system requires the user to provide 5 book titles with their ratings.

The book recommender system works in two ways
1. Select a book from the given drop down list and give a corresponding rating to it.
2. Use the image search feature to upload the cover art of a book and select that book with it's rating for recommendation.

A table with the current selection of books and ratings is maintained for convinience. 

The user can use this table to delete any of the selected books or reset the whole selection of books.

A cover-art for the book (if available) is generated on selecting a book from the drop down menu.

## Table of Contents 

- [Getting Started](#getting-started)
- [Build and run](#build-and-run)
- [High Level Workflow](#high-level-workflow)
- [Image recognition](#image-recognition)
- [Book Recommendation Algorithm](#book-recommendation-algorithm)

## Getting Started

Follow these instructions to get the recommender system up and running on your system.To get started, clone the repository to your system.

### Pre-requisites

- **For Windows/MacOS Users**

[Docker Desktop](https://docs.docker.com/desktop/) - Includes Docker Engine and Docker-Compose required to run the project.

The steps to download and install docker are mentioned in the link.

__*Note:* Please enable the following windows feautes__
- Virutal Machine Platform
- Windows Hypervisor Platform
- Windows Subsystem for Linux

Run the following command to check your installation:
```
$ docker --version
$ docker-compose --version
```
- **For Linux Based OS Users**

[Docker](https://docs.docker.com/engine/) - Includes Docker Engine to work with Containers.  
[Docker-Compose](https://docs.docker.com/compose/) - Includes Docker-Compose to combine containers running for an application.

__*Note:* For the linux based system, run the below commands by granting them admin privileges (sudo)__

Run the following command to check your installation:
```
$ sudo docker --version
$ sudo docker-compose --version
```

## Build and run

After completing the above prerequisites it's time to build and run the project

1. Extract the project files to the downloads folder
2. Open command prompt, powershell or the terminal and change the current working directory to the location where the files were extracted. The folder would be named jtp-project
```
 cd <repository-path>
```
3. Execute the following commands with admin privileges to get the project running
```
 docker-compose build
 docker-compose up
```
4. Open any broswer and then hit the url - http://localhost:5000 to access the book recommender system
5. pydocs can be generated for this project by the following command 
```
python -m pydoc -p 8726
```
  - The docs are genereted at localhost:8726

__*Note:* Please ensure that the port 5000 is not in use. This port number is required for the Flask application to run.__

## High Level Workflow

![image](https://user-images.githubusercontent.com/62939406/134805167-88fe29eb-0ee2-4c3d-a6c7-42f6cdbf3991.png)

## Image recognition

![image](https://user-images.githubusercontent.com/62939406/134805191-a75076b4-a358-4cbc-956c-9d0f87077973.png)

__*Note:* The image recognition service uses an online reverse search index called yandex, it has a fixed request limit of 5 after which the connection would not be made with the website and the service will shut down. Solution to this is to change your connection to use a different IP address.__

## Book Recommendation Algorithm

The following recommendation algorithm is based on collaborative filtering, where the user choices and ratings are matched with choices of existing users in the database to find the most similar users. The highly rated books by those mutual users are suggested based on similarity.

![image](https://user-images.githubusercontent.com/62939406/134805195-1f2fb637-17f2-448f-830a-7c4fbc9f746a.png)

## Built With

* [Flask](https://flask.palletsprojects.com/en/2.0.x/) - The web framework used
* [SQLite](https://www.sqlite.org/index.html) - Database used
* [Python](https://docs.python.org/3/) - Programming Language used

## Dataset used

* [goodbooks-10k](https://www.kaggle.com/zygmunt/goodbooks-10k)

## Author

* Shubhbam Nawani
