REM usage run.bat <code_dir>
REM add -javaagent:FULL\PATH\TO\jcov.jar=grabber -Xms512m -Xmx1024m to surefire argline
call java -jar jcov.jar tmplgen -verbose  -abstract on -field on %1
start java -jar jcov.jar grabber -vv -t template.xml -o result.xml -scale
pushd %1
call mvn install
popd
call java -jar jcov.jar grabberManager -stop
call java -jar jcov.jar repgen -format text -o report -src %1 -javap %1 -verbose -testsinfo result.xml 
call java -jar jcov.jar repgen -format html -o report -src %1 -javap %1 -verbose -testsinfo result.xml 