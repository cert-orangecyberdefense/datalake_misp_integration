# Datalake misp integration

### This repo is used to continuously retrieve threats from the Datalake platform and insert them into a Misp instance 

## Setting up the image
```shell
# Retrieve the image with:
docker pull ocddev/datalake-misp-integration
# Copy the template.env to .env and fill the value
# Copy the template_queries.json to queries.json and fill the value
# Then finally run the image with:
docker run --env-file .env -v /path/to/queries.json:/code/queries.json ocddev/datalake-misp-integration
```

## Stopping the container

To stop the container gracefully, allowing the events to be fully inserted, use:
```shell
docker stop -t 120 <container_name>
```

## Testing the image with a local misp

Set up a local misp by following [the instruction of this repo](https://github.com/MISP/misp-docker#building-your-image)  
Set the env variable `OCD_DTL_MISP_HOST` to `localhost` and get the API key here: http://localhost/events/automation for `OCD_DTL_MISP_API_KEY`  
Then build and run the image with:
```shell
docker build -t misp_push . && docker run --env-file .env --net=host misp_push
```

## Running tests
Install pytest with: `pip install pytest`  
Then run: `OCD_DTL_MISP_API_KEY='x' python -m pytest`