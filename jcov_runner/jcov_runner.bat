REM usage run.bat <code_dir>
call java -jar C:\Users\User\Downloads\jcov-2.0-beta-1\JCOV_BUILD\jcov_2.0\jcov.jar tmplgen -verbose  -abstract on -field on %1
start java -jar C:\Users\User\Downloads\jcov-2.0-beta-1\JCOV_BUILD\jcov_2.0\jcov.jar grabber -vv -t template.xml -o result.xml -scale
pushd %1
call mvn install
popd
call java -jar C:\Users\User\Downloads\jcov-2.0-beta-1\JCOV_BUILD\jcov_2.0\jcov.jar grabberManager -stop
call java -jar C:\Users\User\Downloads\jcov-2.0-beta-1\JCOV_BUILD\jcov_2.0\jcov.jar repgen -format text -o report -src %1 -javap %1 -verbose -testsinfo result.xml 