# cdktf-get-started
cdktf-get-started

Getting started guide for cdktf on IBMCLOUD

## how to try (in us-south region)

If it's the first time you're trying, then pull the docker image (the dev-env) first:
```
docker-compose pull
```
and,
```
export IBMCLOUD_API_KEY=<YOUR IBMCLOUD API KEY>
docker-compose run cdktf-get-started
cd learn-cdktf-python
cdktf get
cdktf synth
cdktf deploy --auto-approve
cdktf destroy --auto-approve
```
