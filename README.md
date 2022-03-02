## Activate the Virtual Environment 

To enter the virtual environment, navigate to the *api* directory and run the command:

**venv\Scripts\activate**

If you've correctly activated the virtual environment, the command line will start with (venv).


## Start the Flask Backend 

To start the backend API, navigate to the *Scripts* directory and run the command:

``` flask run ```

If successful, you should see:

 ``` 
 * Serving Flask app 'api.py' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 542-534-549
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 ```

Do **NOT** CTRL+C until you want to close the API.


## Start the React Frontend 

To start the frontend, navigate to the *frontend* directory and run the command (once only):

```npm install -g yarn ```

Once the yarn command is installed, or if it is already installed, start the React App using the command:

``` yarn start ```

If successful, you should see:

```
Starting the development server...
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
```
