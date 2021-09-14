# URL Shortener Application Backend
For the full readme of the fullstack application, refer to this github [link](https://github.com/ngkc1996/url-shortener-ui).

## API Documentation
Refer to this Swagger page for the [API Documentation](https://app.swaggerhub.com/apis-docs/ngkc1996/url-shortener/1.0.0).

## Deployment to Azure
This [link](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=bash&pivots=python-framework-flask) provides a reasonably good guide.
1. Create a Web App on Azure, using _Python_ as the Stack.
2. Push the code to GitHub.
3. Use the _Deployment Center_ to set up a build and deploy pipeline via _GitHub Actions_. Use the `.yml` file provided in this repository.
4. Edit the configurations.
   - Under _Configuration_ > _Application Settings_, add an application setting: `Name`: `SCM_DO_BUILD_DURING_DEPLOYMENT`; `Value`: `1`
   - For each environment variable listed below, add an application setting.
5. The app should be running at `<app-name>.azurewebsites.net`. Every time a new commit is added to the GitHub repository, the app will be deployed automatically to Azure.

## Local Development
- Clone this repository.
- Navigate to project folder root.
- Create virtual environment: `virtualenv <name>`, e.g. `virtualenv venv`
- Activate virtual environment:
  - Windows _cmd.exe_: `venv\Scripts\activate.bat`
  - Mac: `source <venv>/bin/activate`
  - To deactivate: `deactivate`
- Install libraries: `pip install -r requirements.txt`
- Run `app.py` in project folder, with the environment variables.

## Environment Variables

| Variable                    | Description                                                                                                                    |
|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| BASE_URL                    | The URL for the server. Used to generate the shortened links.   
| DB_URI                      | The Connection String URI for the database. Example for MongoDB: `mongodb+srv://[username:password]@[host].mongodb.net/[database-name]?retryWrites=true&w=majority`
