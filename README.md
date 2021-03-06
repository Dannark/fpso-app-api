# FPSO Management Backend
This project is to demonstrate how to use python to get a simple backend API with Django. The pipeline uses Travis, docker and heroku for the CI/CD!
You can try it alive in `https://fpso-app-api.herokuapp.com/api`

## Workflow
[![FPSO Management Backend Flow](https://user-images.githubusercontent.com/7622553/95813333-088adc80-0cee-11eb-9beb-805238d8f9df.png)](https://whimsical.com/UG7Yb1dtYLgPRB7JBnRjoe)

## Entitys
* Vessel
* Equipments

## Tools Used
* Django
* djangorestframework
* flake8 (for the linter)
* SQLite (migrations)
* Docker
* Travis

## Instructions
1. Merge the repository, and start the docker container
2. To run the tests use: `docker-compose run app sh -c "python manage.py test && flake8"`

**Note:** You can also try it alive in `https://fpso-app-api.herokuapp.com/api`

### Registering a vessel
To register a new Vessel use `POST` method on the Url: `http://127.0.0.1:8000/api/vessels/create` with:

**Body Json:**
```yaml
{
  "code": "MV102"
}
```

### Get the list of vessel
To get the list of Vessels use `GET` method on the url: `http://127.0.0.1:8000/api/vessels`

### Registering a new equipment in a vessel
To register a new equipment use `POST` method on the the following url with the `code` at the end, for example `http://127.0.0.1:8000/api/equipment/create/MV102`

**Body Json:**
```yaml
{
  "code": "5310B9D7",
  "name": "compressor",
  "location": "Brazil"
}
```

### Setting an equipment’s status to inactive
To update an equipment use `PUT` method on the url `http://127.0.0.1:8000/api/equipment/update`

**Body Json:**
```yaml
[
  {
    "code": "5310B9D7",
    "status": "active"
  },
    {
    "code": "5310B9D8",
    "status": "inactive"
  },
]
```

### Returning all active equipment of a vessel
To get the list of all equipments use `GET` method on the url: `http://127.0.0.1:8000/api/equipments/`

If you want to get filter by status pass on the body:

**Body Json:**
```yaml
{
  "status": "active"
}
```

Or with multiple filters:

**Body Json:**
```yaml
{
  "status": "active",
  "vessel_code": "MV102"
}
```
