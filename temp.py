# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------------------

# from dask.distributed import Client, wait
# from simmate.workflows.diffusion.empirical_measures import workflow
# from simmate.configuration.django import setup_full  # ensures setup
# from simmate.database.diffusion import Pathway as Pathway_DB

# # grab the pathway ids that I am going to submit
# pathway_ids = (
#     Pathway_DB.objects.filter(empiricalmeasures__isnull=True)
#     .order_by("structure__nsites", "nsites_777")
#     .values_list("id", flat=True)
#     .all()  # [:1500]  # if I want to limit the number I submit at a time
# )

# # setup my Dask cluster and connect to it. Make sure I have each work connect to
# # the database before starting
# client = Client(preload="simmate.configuration.dask.init_django_worker")

# # Run the find_paths workflow for each individual id
# # To make sure Dask is stable and doesn't have too many futures, I only submit
# # 250 at a time. Once those finish, I submit another 250.
# chunk_size = 250
# chunks = [pathway_ids[i:i + chunk_size] for i in range(0, len(pathway_ids), chunk_size)] 
# for chunk in chunks:
#     futures = client.map(
#         workflow.run,
#         [{"pathway_id": id} for id in chunk],  # for id in pathway_ids chunk
#         pure=False,
#     )
#     results = wait(futures)

# --------------------------------------------------------------------------------------

from prefect import Client
from simmate.configuration.django import setup_full  # ensures setup
from simmate.database.diffusion import Pathway as Pathway_DB

# grab the pathway ids that I am going to submit
pathway_ids = (
    Pathway_DB.objects.filter(
        vaspcalca__isnull=True,
        empiricalmeasures__dimensionality__gte=1,
        # empiricalmeasures__oxidation_state=-1,
        # empiricalmeasures__ionic_radii_overlap_cations__gt=-1,
        # empiricalmeasures__ionic_radii_overlap_anions__gt=-1,
        # nsites_777__lte=150,
        # structure__nsites__lte=20,
    )
    .order_by("nsites_777", "structure__nsites", "length")
    # BUG: distinct() doesn't work for sqlite, only postgres. also you must have
    # "structure__id" as the first flag in order_by for this to work.
    # .distinct("structure__id")
    .values_list("id", flat=True)
    # .count()
    .all()[:300]
)

# connect to Prefect Cloud
client = Client()

# submit a run for each pathway
for pathway_id in pathway_ids:
    client.create_flow_run(
        flow_id="b10a9c46-763f-42e7-8ff5-eff91fb8fb6c",
        parameters={"pathway_id": pathway_id},
    )

# --------------------------------------------------------------------------------------


# from simmate.configuration.django import setup_full  # ensures setup
# from simmate.database.diffusion import EmpiricalMeasures
# queryset = EmpiricalMeasures.objects.all()[:1000]
# from django_pandas.io import read_frame
# df = read_frame(queryset) # , index_col="pathway"

# import datetime
# from simmate.configuration.django import setup_full  # ensures setup
# from simmate.database.diffusion import VaspCalcA
# queryset = VaspCalcA.objects.all()
# from django_pandas.io import read_frame
# df = read_frame(queryset)

# .filter(pathway_id__in=pids)
# pids= [3036,
# 9461,
# 3040,
# 10373,
# 3033,
# 8701,
# 9143,
# 9924,
# 1220,
# 1443,
# 1496,
# 1034,]


# from simmate.database.diffusion import Pathway as Pathway_DB
# path_db = Pathway_DB.objects.get(id=55)
# path = path_db.to_pymatgen()
# path.write_path("test.cif", nimages=3)

# # from dask.distributed import Client
# # client = Client(preload="simmate.configuration.dask.init_django_worker")


# set the executor to a locally ran executor
# from prefect.executors import DaskExecutor
# workflow.executor = DaskExecutor(address="tcp://152.2.172.72:8786")




from simmate.configuration.django import setup_full  # ensures setup
from simmate.database.diffusion import Pathway
from simmate.workflows.diffusion.utilities import (
    run_vasp_custodian_neb,
    get_oxi_supercell_path,
)

path_db = Pathway.objects.first()
path = path_db.to_pymatgen()
structures = path.get_structures(nimages=3)
path_supercell = get_oxi_supercell_path(path, min_sl_v=7)
images = path_supercell.get_structures(nimages=1, idpp=True)

run_vasp_custodian_neb(
    images,
    vasp_cmd="mpirun -n 16 vasp",
    # errorhandler_settings="no_handler",
    custom_incar_endpoints={"NPAR": 1, "EDIFF": 5e-5, "ISIF": 2},  # "NSW": 0,
    custom_incar_neb={"NPAR": 1, "EDIFF": 5e-5, "EDIFFG": -0.1, "ISIF": 2},
)



"""
PZUNMTR parameter number    5 had an illegal value 
{    0,    0}:  On entry to 
PZUNMTR parameter number    5 had an illegal value 
 GSD%LWWORK        1228        5116         456          76
 ERROR in subspace rotation PSSYEVX: not enough eigenvalues found         618


===================================================================================
=   BAD TERMINATION OF ONE OF YOUR APPLICATION PROCESSES
=   RANK 3 PID 3326541 RUNNING AT WarWulf
=   KILLED BY SIGNAL: 6 (Aborted)
===================================================================================
"""


# from prefect import Flow, task, context

# @task
# def access_context():
    
#     # you can initialize context with custom variables
#     # Note, this can be done outside of a task too
#     with context(a=1, b=2) as c:
#         print(c.a) # 1
    
#     # you can also access metadata of the overall flow-run
#     print(context.flow_run_id)
#     # or task-run metadata
#     print(context.task_run_id)


# # The task shown above will only work within a Flow!

# access_context.run()  # does not have context filled and will fail
 
# with Flow("Grab that context!") as flow:
#     access_context()  # has a context filled and works successfully
