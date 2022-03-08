# cdktf-get-started
cdktf-get-started

Getting started guide for cdktf on IBMCLOUD

## how to test ( in us-south region)
```
export IBMCLOUD_API_KEY=<YOUR IBMCLOUD API KEY>
docker-compose run cdktf-get-started
cd learn-cdktf-python
cdktf get
cdktf synth
cdktf deploy --auto-approve
cdktf destroy --auto-approve
```
