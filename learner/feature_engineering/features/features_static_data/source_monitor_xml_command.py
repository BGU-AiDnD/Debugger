SOURCE_MONITOR_XML_COMMAND = """
    <!--?xml version="1.0" encoding="UTF-8" ?-->
<sourcemonitor_commands>

   <write_log>true</write_log>

   <command>
       <project_file>verP.smp</project_file>
       <project_language>Java</project_language>
       <file_extensions>*.java</file_extensions>
       <source_directory>verREPO</source_directory>
       <include_subdirectories>true</include_subdirectories>
       <checkpoint_name>Baseline</checkpoint_name>

       <export>
           <export_file>verP.csv</export_file>
           <export_type>3 (Export project details in CSV)</export_type>
           <export_option>1 (do not use any of the options set in the Options dialog)</export_option>
       </export>
   </command>

   <command>
       <project_file>verP.smp</project_file>
       <project_language>Java</project_language>
       <file_extensions>*.java</file_extensions>
       <source_directory>verREPO</source_directory>
       <include_subdirectories>true</include_subdirectories>
       <checkpoint_name>Baseline</checkpoint_name>
       <export>
           <export_file>verP_methods.csv</export_file>
           <export_type>6 (Export method metrics in CSV)</export_type>
           <export_option>1 (do not use any of the options set in the Options dialog)</export_option>
       </export>
   </command>

</sourcemonitor_commands>"""