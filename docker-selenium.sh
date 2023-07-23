docker pull selenium/standalone-chrome
docker run -d -p 4444:4444 --shm-size=2g selenium/standalone-chrome