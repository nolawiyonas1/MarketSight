@echo off
if "%1"=="build" goto build
if "%1"=="start" goto start
if "%1"=="stop" goto stop

echo Usage: mp [start|build|stop]
echo   start - Run the app
echo   build - Rebuild and run (use when adding libraries)
echo   stop  - Stop all containers
goto :eof

:start
echo Starting MarketSight...
docker compose up
goto :eof

:build
echo Rebuilding MarketSight...
docker compose build --no-cache
docker compose up
goto :eof

:stop
echo Stopping MarketSight...
docker compose down
goto :eof
