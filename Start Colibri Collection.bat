start opencolibricollection.bat
cd "Portable Python 2.7.6.1"
.\App\python.exe ./google_appengine/dev_appserver.py --blobstore_path=./google_appengine/google_appengine_datastores/colibricollection_blobstore --datastore_path=./google_appengine/google_appengine_datastores/colibricollection_datastore --host=127.0.0.1 --port=80 --skip_sdk_update_check true ./google_appengine/colibricollection