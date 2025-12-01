# Dashboard Tutorial for Digital Twin 
## Initialization



### 1.	Create a folder where we are going to store the app
    
    ```My_folder/Dashboard```

### 2.	Initialize Github repository ** Optional – Connect with github
    ```git
    cd My_folder/Dashboard
    git init
    git add .
    git commit -m "Initialize repo"
    git remote add origin https://github.com/username/Dashboard
    git push -u origin master
    ```
    Or you can use VS Code + Github extension. Then go to the github tab and click on the button "Initialize repository"

    You will be asked to log in with your github account and write a name for your remote repository.

### 3.	Create intial files in the folder. 

Create a Dashboard.py file for the Streamlit app,
Create a Map.html which will be your map container.

### 4. Create a virtual environment and add packages to it
a.	I have been using UV for package management (a bit easier and cleaner than only pip)

b. On the terminal

    ```py
    pip install uv  
    
    ```
	
For mac 
  ```
 brew install uv
 ```
c.	Now uv venv to create a virtual environment
