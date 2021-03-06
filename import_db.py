from dbclient import *
from timeit import default_timer as timer
from datetime import timedelta
from os import makedirs, path
from datetime import datetime


# python 3.6

def main():
    # define a parser to identify what component to import / export
    parser = get_import_parser()
    # parse the args
    args = parser.parse_args()

    # parse the path location of the Databricks CLI configuration
    login_creds = get_login_credentials(profile=args.profile)

    # cant use netrc credentials because requests module tries to load the creds into http basic auth headers
    # aws demo by default
    is_aws = (not args.azure)
    # parse the credentials
    url = login_creds['host']
    token = login_creds['token']
    if is_aws:
        export_dir = 'logs/'
    else:
        export_dir = 'azure_logs/'

    makedirs('logs', exist_ok=True)
    makedirs('artifacts', exist_ok=True)

    debug = False
    if debug:
        print(url, token)

    now = str(datetime.now())
    if args.workspace:
        print("Import the complete workspace at {0}".format(now))
        print("Import on {0}".format(url))
        ws_c = WorkspaceClient(token, url, export_dir)
        start = timer()
        # log notebooks and libraries
        ws_c.import_all_workspace_items()
        end = timer()
        print("Complete Workspace Import Time: " + str(timedelta(seconds=end - start)))

    if args.libs:
        lib_c = LibraryClient(token, url, export_dir)
        start = timer()
        ########### TO DO #######################
        end = timer()
        #print("Complete Library Import Time: " + str(timedelta(seconds=end - start)))

    if args.users:
        print("Import all users and groups at {0}".format(now))
        ws_c = WorkspaceClient(token, url, export_dir)
        start = timer()
        # log all users
        ################## TO DO : IMPORT USERS ############################
        end = timer()
        print("Complete Users Import Time: " + str(timedelta(seconds=end - start)))
        start = timer()
        # log all groups
        ################## TO DO : IMPORT GROUPS
        end = timer()
        print("Complete Group Import Time: " + str(timedelta(seconds=end - start)))

    if args.clusters:
        print("Import the cluster configs at {0}".format(now))
        cl_c = ClustersClient(token, url, export_dir)
        if is_aws:
            print("Start import of instance profiles ...")
            start = timer()
            cl_c.import_instance_profiles()
            end = timer()
            print("Complete Instance Profile Import Time: " + str(timedelta(seconds=end - start)))
        print("Start import of instance pool configurations ...")
        start = timer()
        cl_c.import_instance_pools()
        end = timer()
        print("Complete Instance Pools Creation Time: " + str(timedelta(seconds=end - start)))
        print("Start import of cluster configurations ...")
        start = timer()
        cl_c.import_cluster_configs()
        end = timer()
        print("Complete Cluster Import Time: " + str(timedelta(seconds=end - start)))

    if args.jobs:
        print("Importing the jobs configs at {0}".format(now))
        start = timer()
        jobs_c = JobsClient(token, url, export_dir)
        jobs_c.import_job_configs()
        end = timer()
        print("Complete Jobs Export Time: " + str(timedelta(seconds=end - start)))

    if args.metastore:
        print("Importing the metastore configs at {0}".format(now))
        start = timer()
        hive_c = HiveClient(token, url, export_dir)
        # log job configs
        hive_c.import_hive_metastore(is_aws)
        end = timer()
        print("Complete Metastore Import Time: " + str(timedelta(seconds=end - start)))


if __name__ == '__main__':
    main()
