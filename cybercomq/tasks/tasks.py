from celery.task import task
from dockertask import docker_task
from subprocess import call,STDOUT
import requests
import os

#Default base directory 
basedir="/data/static/"


#Example task
@task()
def add(x, y):
    """ Example task that adds two numbers or strings
        args: x and y
        return addition or concatination of strings
    """
    result = x + y
    return result

@task()
def add_usingR(x, y):
    task_id = str(add_usingR.request.id)
    resultDir = setup_result_directory(task_id)
    host_data_resultDir = "/data/static/someapp_tasks/{0}".format(task_id)
    runfile = "simple.R"	
    #Run R Script in an R container
    #docker_opts = "-d --rm -v '/opt/someapp/data/static':/home/$USER -w /home/$USER -e USERID=$UID "
    docker_opts = "-v /opt/someapp/data/static:/home/dwilson1:z "	
    docker_cmd ="Rscript {0}".format(runfile)
    result = docker_task(docker_name="rocker/r-base",docker_opts=docker_opts,docker_command=docker_cmd,id=task_id)
    #result_url ="http://{0}/someapp_tasks/{1}".format(result['host'],result['task_id'])
    result_url = x + y
    return result_url
	
def setup_result_directory(task_id):
    resultDir = os.path.join(basedir, 'someapp_tasks/', task_id)
    os.makedirs(resultDir)
    os.makedirs("{0}/input".format(resultDir))
    os.makedirs("{0}/output".format(resultDir))
    return resultDir 

	
# docker run -d --rm -v "$PWD":/home/$USER -w /home/$USER -e USERID=$UID rocker/r-base R CMD BATCH '--args 2 2' add_usingR.R
# docker run -d --rm -v "$PWD":/home/$USER -w /home/$USER -e USERID=$UID rocker/r-base R CMD BATCH '--args 2 2' ./add_usingR.R
# docker run -d --rm -v "$PWD":/home/$USER -w /home/$USER -e USERID=$UID rocker/r-base R CMD BATCH '--args 2 2' ./someapp_tasks/add_usingR.R
# docker run -d --rm -v "$PWD":/home/$USER -w /home/$USER -e USERID=$UID rocker/r-base R CMD BATCH --no-save --no-restore '--args 2 2' add_usingR.R
# docker run -d --rm -v '/opt/someapp/data/static':/home/$USER:z -w /home/$USER -e USERID=$UID rocker/r-base R CMD BATCH --no-save --no-restore '--args 2 2' add_usingR.R
