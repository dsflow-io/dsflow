
    #   dsflow_py_path = os.path.join(DSFLOW_ROOT, 'dsflow')
    #   dsflow_spark_config_path = os.path.join(get_app_path(), "config", "spark-conf")
    #   dsflow_ipython_config_path = os.path.join(get_app_path(), "config", "ipython-conf")

    # docker_volumes = {get_datastore_path(): {'bind': '/data', 'mode': 'rw'},
    #                   get_flows_path(): {'bind': '/home/jovyan/flows', 'mode': 'ro'},
    #                   dsflow_py_path:  {'bind': '/home/jovyan/dsflow', 'mode': 'ro'},
    #                   dsflow_spark_config_path: {'bind': '/usr/local/spark/conf', 'mode': 'ro'},
    #                   dsflow_ipython_config_path: {'bind': '/home/jovyan/.ipython', 'mode': 'ro'},
    #                   }

    #   - $DSFLOW_WORKSPACE/config/ipython-conf:/home/jovyan/.ipython
    #   - $DSFLOW_WORKSPACE/config/jupyter-conf:/home/jovyan/.jupyter
    #   - $DSFLOW_WORKSPACE/config/spark-conf:/home/jovyan/.spark-conf


    # output = client.containers.run("jupyter/pyspark-notebook:latest",
    #                                docker_cmd,
    #                                volumes=docker_volumes
    #                                )


@cli.command()
@click.argument("query")
def sql(query):
    """Run Spark SQL code -- BROKEN!"""

    # FIXME: this should be independant from the notebook sessions
    execute_sql(query)


@cli.command(short_help="Refresh Spark tables")
def refresh():
    """Refresh Spark"""

    possible_tables = os.listdir(get_datastore_path() + '/tables')

    pprint(possible_tables)

    data = {'kind': 'pyspark3', }
    headers = {'Content-Type': 'application/json'}
    # r = requests.post(host + '/sessions', data=json.dumps(data), headers=headers)
    #
    # print("Spark Contexts:")
    # pprint(r.json())

    statements_url = "{}/sessions/0/statements".format(LIVY_HOST)

    for table in possible_tables:
        try:
            execute_sql("DROP TABLE if exists " + table)

            execute_sql("""
              CREATE TABLE IF NOT EXISTS %s
              USING parquet
              OPTIONS (path='/data/tables/%s')
            """ % (table, table))

            execute_sql("MSCK REPAIR TABLE %s" % table)
            execute_sql("REFRESH TABLE %s" % table)

            print("INFO - %s was successful imported/updated" % table)
        except Exception as e:
            print("ERROR - %s could not be imported" % table)
            logging.error(e)
            pass



# class FlowTemplates(click.MultiCommand):
#
#     def list_commands(self, ctx):
#         list_flows()
#
#     def get_command(self, ctx, name):
#         ns = {}
#         dag_specs = os.path.join(flow_templates_dir, name, 'dag_specs.yaml.j2')
#         with open(dag_specs) as f:
#             pass
#             # code = compile(f.read(), fn, 'exec')
#             # eval(code, ns, ns)
#         return {"test": "test"} # ns['cli']
