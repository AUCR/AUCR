# How to write a processing plugin for AUCR    
This is a simple guide on how to write a processing plugin for AUCR
Processing plugins are designed to be run from the Flask app because it makes the application easy to run as a 
standalone all in one or as a highly scalable web app.

## Example plugin #1 A cuckoo file processing submission plugin

### How to process files by using mqtasks.yml and message queuing 
First step to making a processing plugin is to create a mqtasks.yml in the main dir of the plugin. 
In order to listen to the file processing pipeline we hook on to reports: and then file:. 
Then we use our own custom cuckoo queue to duplicate messages going into the file queue into our cuckoo message queue.
    
        reports:
          files: ["cuckoo"]
    

### The \_\_init\_\_.py load function for the plugin
Now that we have a basic message queue being created for us lets make a consumer to process file hashes from that message queue.
        
        import os
        # Import get_a_tasks_mq from the aucr framework to listen to your custom message queue
        from app.plugins.tasks.mq import get_a_task_mq
        # Import submit_file_to_cuckoo function
        from app.plugins.cuckoo.cuckoo import submit_file_to_cuckoo
        # import index_data_to_es to add our report data into an elasticsearch index
        from app.plugins.reports.storage.elastic_search import index_data_to_es
        from multiprocessing import Process
        
        def call_back(ch, method, properties, file_hash):
            """Custom cuckoo file upload message queue call back."""
            # file_hash is passed in by the unum upload plugin when it checks for other mqs to duplicate messages into.
            report = submit_file_to_cuckoo(file_hash)
            cuckoo_url = os.environ.get('CUCKOO_URL')
            for items in report:
                cuckoo_url_path = \
                    {"cuckoo_url": str(cuckoo_url + "/analysis/" + str(items)), "file_hash": file_hash.decode('utf8')}
                index_data_to_es("cuckoo", cuckoo_url_path)
        
        
        def load(app):
            cuckoo_processor = os.environ.get('CUCKOO_API_URL')
            # Listen to our custom message queue named "cuckoo"
            tasks = "cuckoo"
            # Load rabbit mq server config
            rabbitmq_server = os.environ.get('RABBITMQ_SERVER')
            rabbitmq_username = os.environ.get('RABBITMQ_USERNAME')
            rabbitmq_password = os.environ.get('RABBITMQ_PASSWORD')
            tasks = "cuckoo"
            # If CUCKOO_API_URL is enabled to start a sub process message queue consumer by passing in our call_back()            
            if cuckoo_processor:
                p = Process(target=get_a_task_mq, args=(tasks, call_back, rabbitmq_server, rabbitmq_username,
                                                        rabbitmq_password))
                p.start()

Once you have this much written it will run and process things at run time outside the context of the user application.
It simply just hooks on to the upload of any file and processes it.


### How does the message queue get the file_hash message
When a file is uploaded the Unum plugin uses the get_upload_file_hash() function in app.plugins.analysis.file to upload
a file and get the return hash. It gets all message queue config files all plugins define in the main dir with mqtasks.yml.
File is now a reserved plugin message queue name and any plugin can get the messages but using the mqtasks.yml reports: 
file: options as we did above. Example code how the analysis file upload framework does this.
 
        files_config_dict = mq_config_dict["reports"]
        for item in files_config_dict:
            if "files" in item:
                index_mq_aucr_report(file_hash, str(rabbit_mq_server_ip), item["files"][0])