# Skin Cancer Predictor Web App

## Demo

![screenshot](https://raw.githubusercontent.com/makeavish/SkinCancerPredictor/master/demo.gif)

## Getting Started

Create a [virtual env](https://docs.python.org/3/tutorial/venv.html) or [conda env](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/) and install all the required packages

### Requirements

- setuptools>=41.0.0
- scipy==1.4.1
- Flask>=1.1.2
- gunicorn>=20.0.4
- numpy>=1.19.0
- Keras>=2.4.3
- tensorflow-cpu>=2.2.0
- gevent>=20.6.2
- Werkzeug>=1.0.1
- MarkupSafe>=1.1.1
- Jinja2>=2.11.2

## How To Use

After installing all the required packages
From your command line:

```bash
# Clone this repository
$ git clone https://github.com/makeavish/SkinCancerPredictor

# Go into the repository
$ cd SkinCancerPredictor

# Run the app
$ python3 app.py [host] [port] [debug]
```

Arguments are optional

**Default values**
```
host = localhost
port = 5000
debug = False
```

## API

### Using predict function

**Request** : `POST /predict`

**Body** : form-data (key: file, value: image file of format .png, .jpg, .jpeg)

### Success response

**Code** : `200`

**Body** : html page with benign/malignment

### Error Response

**Code** : `400`

**Body** : Json
```
{
  "message": "No image selected for uploading"
}
```

or

```
{
  "message": "Incorrect image format selected for uploading"
}
```

## Todo

- Generate image preview

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://github.com/makeavish/SkinCancerPredictor/blob/master/LICENCE)