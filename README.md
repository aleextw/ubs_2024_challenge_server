Example challenge developer project using python

Initial project setup:
- CICD using `gitlab-ci.yml` 
- Heroku for server

To set up on intellij:
- install Python 3.9
- pip install -r .\requirements.txt
- go to Project Structure > SDKs > + > Add Python SDK (this will create the venv folder)

Run Tests
- 'Edit Configurations...'
- `Run All Tests.run.xml`
- option.SDK_HOME.value
- option.WORKING_DIRECTORY.value

Run App
- Update `Run App.run.xml`
- option.target.value
- option.SDK_HOME.value
- option.WORKING_DIRECTORY.value 
- should be able to see page running at http://localhost:5000/decoder 
- in tests/http run test_http.http to hit localhost endpoints

# Challenges

[Asteroid](static/asteroid.md)

[Decoder](static/decoder.md)