# synchronization_task
Veeam Technical Task for Internal Development in QA Team (Python)

The following steps are provided as an easy guide to run the file for testing purposes.

1. Download the Script: Download the sync_task_final.py script to your computer.
   
2. Set Up Folders: In the same directory where you saved the script, create an empty folder named 'Source' or use the provided one. Similarly, create an empty folder named 'Replica' or use the provided one.

3. Prepare Log File: In the same directory, create a new plain text document named 'log.txt' or use the provided one.

4. Run the Script: Open the command prompt and navigate to the directory where sync_task_final.py is located.

5. Execute the Script: Run the script using the following command:

      python sync_task_final.py /path/to/Source /path/to/Replica sync_interval log.txt

Replace /path/to/Source with the actual path to your 'Source' folder, /path/to/Replica with the actual path to your 'Replica' folder, and sync_interval with the synchronization interval in seconds. For example, if you want to sync every 10 seconds, use 10. Make sure you use a positive number greater than 0. The log.txt file will store synchronization logs.

Note: Make sure you have Python installed on your system. You can check by opening the command prompt and entering 'python --version'. If you don't have Python installed, you can download it from the official Python website. Ensure you have Python 3.7+ in order for the script to run properly.
