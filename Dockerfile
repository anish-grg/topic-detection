# A dockerfile must always start by importing the base image.
# We use the keyword 'FROM' to do that.
FROM python:3.8
# Set pythonpath environment variable to run/import custom python packages
ENV PYTHONPATH "${PYTHONPATH}:/app"
# In order to copy/launch any files, we must import it into our image.
# We use the keyword 'COPY' to do that.
COPY ./requirements.txt / 
# To run a command during building an image
# We use keyword 'RUN' 
RUN pip install --upgrade pip && pip install -r /requirements.txt
# We are copying our primary python directory 'app' into our image at path current path with name 'app' 
COPY ./app ./app
# We copy our 'entrypoint' script into image
COPY ./entrypoint.sh /
# Provide executable permission to 'entrypoint' so that we can run commands from it
RUN chmod +x /entrypoint.sh
# We need to define the command to launch when we are going to run the image.
# We use the keyword 'CMD' to do that.
# The following command will execute 'entrypoint' script
CMD ["/entrypoint.sh"]
# The following command will execute "python ./main.py".
# CMD [ "python", "./app/main.py" ]