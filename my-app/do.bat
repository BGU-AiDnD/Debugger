copy .\pomNoAgent.xml .\pom.xml
call mvn clean install
copy .\target\uber-my-app-1.0.1-SNAPSHOT.jar .\agent.jar
copy .\target\uber-my-app-1.0.1-SNAPSHOT.jar .\uber-my-app-1.0.1-SNAPSHOT.jar
copy .\pomAgent.xml .\pom.xml
call mvn clean install