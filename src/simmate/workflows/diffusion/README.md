
## Fractured Hierarchical Architecture for High-Throughput Diffusion Analysis

While this module will eventually be for common diffusion analysis workflows, it is currently for my grad-school project on halide diffusion energies. I'm on a time-crunch to graduate (lmao) and thus take some shortcuts by using pymatgen and custodian -- rather than the functionality I've rewritten in simmate. This will allow me to have an easier time publishing because I can say I'm using well-established codes instead of my new simmate code. So instead of introducing a new
framework, this paper will be introducing the effectiveness of my "Fractured Hierarchical Architecture". This is breaking of a hierarchical workflow (i.e. one that has increasely accurate calculations separated by halting/filtering criteria) into individual ETL pipelines, each with their own table.


### Fixed-Workflow Architecture

You have an overall workflow where you pass in one structure at a time. The entire workflow for that structure is ran immediately and to completion (or until a check fails).


With this setup, it makes sense to publish on a well-designed workflow, and then have a separate paper where we scale to a full database.

Scaling your computation resources is tricky here because we want to run as many structure workflows in parallel as possible. The amount of resources the structure needs scales as the workflow progresses so we would need a complex Executor to handle this. An example of this is when the first task can be ran on one core in seconds while the final task needs >20 cores and hours to run. There may be a scenario where all structures make it far along the analysis and many resources are all needed at once (or resources underused if the reverse occurs). So you can set resources by calc/task but we will like over- or under-submit to that queue at any given time. There is one advantage though, and it’s that we can run all calculations in the same directory and utilize the previous output files for continuation on VASP calcs.


You can certainly move your code back and forth between these architectures, but it’s much easier said than done due to data storage. Further, converting from each isn’t equally easy depending on how you wrote your code.


### Fractured-Workflow Architecture

You have individual tasks (calcs) that are each applied to an entire database -- where the database can be structures, pathways, or outputs from a previous calculation. The input database for each task is constantly read by a ‘priority ranking’ function. The task runs independently and pulls the top priority entry (structure/pathway/etc) and runs it next. 


With this setup, we can have a single paper on the database and workflow architecture. The architecture encompasses how the workflow is constantly evolving, thus the initial publicized workflow doesn’t become immediately obsolete.


Scaling computational resources is very easy here as we can assign a set number of resources for each task - then those resources are always being utilized at the exact specified amount. The downside is that since the tasks are ran independently across differing computational resources, it’s no longer possible to run all of a given workflow in a single working directory (unless we only use a single cluster). Here, the database must carry any connecting information between calculations (if only one cluster is used, we can use a working directory name to connect information with ease). Therefore we can only utilize the previous output files for continuation on VASP calcs if we save them to a database somewhere. If the data is extremely large and expensive to store (or even time consuming to transfer!) this becomes an issue. In many cases, it may be simpler to just redo an analysis or calculation, which results in a decrease in overall workflow efficiency.


You can write your code for fixed-workflow architecture in a way where there is a high-level class that holds all data in memory for every analysis/task done. This uses more memory but ensures that no analysis needs to be repeated, saving on computational cost. Analogously, the other architecture can do the same by saving to a database, but this introduces large write/read times of that data. The solution is to introduce an abstraction of the database layer in fractured architecture, where we can use an in-memory database type (such as Pandas dataframe or Dask global variables) when speed is preferred.


This setup is extremely powerful because it focuses on depth-first scaling - that is, a single cheap calculation can be done on all structures and doesn’t have to wait for workflows to complete before moving on. For example, if one calculation finishes all of the queue pathways, it can trigger a request to broaden cutoff criteria such that more pathways are added to it’s queue. Thus we can change a task/calculation cutoff setting without disrupting the entire workflow.


Priority ranking can adapt overtime as well. For example, we may want to replace a generic priority ranking function with a new calculation entirely (such as a machine-learned descriptor). We could even produce a fork in the workflow for a specific application where priority is based on the target application.


## Stages in my workflow

1. We want to start with a clean database so let's reset ours:
```python
from simmate.configuration.manage_django import reset_db
reset_db()
```

2. We want to add all of the Fluoride structures from the Materials Project to our own database. This includes some extra data such as the hull energy and also running some "sanitation" on the structures. For safe-keeping, I also want to save all of this to a csv file. This is just in case I accidently reset my database. I also make a copy of the database file as db_checkpoint001.sqlite3
```python
# import all of the data to our sqlite database
from simmate.workflows.add_structure import workflow
workflow.visualize()
status = workflow.run(criteria={"elements": {"$all": ["F"],}})

# now convert the entire table to a csv file
from simmate.configuration import manage_django  # ensures django setup
from simmate.database.all import Structure as Structure_DB
queryset = Structure_DB.objects.all()
from django_pandas.io import read_frame
df = read_frame(queryset, index_col="id")
df.to_csv("initial_structuredb.csv")

# if you want to reload the csv
# import pandas
# df = pandas.read_csv("initial_structuredb.csv", index_col="id")
```

3. Using this database, let's make a table for the diffusion pathways. Note that I hardcode some options here, such as limiting each structure to 5 pathways. See the find_paths.py workflow for details. I also make a copy of the database file as db_checkpoint002.sqlite3
```python
from simmate.workflows.diffusion.find_paths import workflow
from simmate.configuration import manage_django  # ensures django setup
from simmate.database.all import Structure as Structure_DB, Pathway as Pathway_DB
workflow.visualize()
# grab all structure ids in our database
structure_ids = Structure_DB.objects.values_list("id", flat=True).all()
# now run the find_paths workflow for all of them. Keep track of which ones fail too.
failed_ids = []
for id in structure_ids:
    status = workflow.run(structure_id=id)
    # make sure all of these complete successfully
    if status.is_failed():
        failed_ids.append(id)
        # raise Exception(f"Structure id {id} failed. Look into this!")

# now convert the entire table to a csv file
queryset = Pathway_DB.objects.all()
from django_pandas.io import read_frame
df = read_frame(queryset, index_col="id")
df.to_csv("initial_pathwaydb.csv")

# for reference these are the structure ids that failed
failed_ids = [134, 339, 465, 466, 479, 481, 482, 990, 995, 1037, 1486, 1487, 1639, 1880, 1928, 1994, 1996, 2482, 2531, 2815, 3113, 3489, 3529, 4044, 4415, 4478, 4480, 4488, 4491, 4997, 5464, 5739, 7911, 7929, 8452, 9327, 9450]

```



## Extra notes

OPTION 1 -- we constantly loop to check number of running workflows and submit new one if needed. This requires a separate process to be constantly running. Or I can have this as a workflow that runs every few seconds.


psuedo-code:


    Connect Prefect client.
    
    
    Check number of workflow runs pending on Prefect. If it is less than our limit, we need to submit another.
    I can also write this to submit multiple at a time, rather than only one per check.
    
    
    Sort pathways by one calc column (priority) and then grab the first pathway where another
    column is null (not completed).
    https://docs.djangoproject.com/en/3.1/ref/models/querysets/#std:fieldlookup-isnull
    https://docs.djangoproject.com/en/3.1/ref/models/querysets/#first    
        filter isnull one column, orderby the other, then grab first
    
    
    Set that column to 'in progress' so that it's not grabbed again. Look at my custom executor class for tips.
    
    
    Submit the workflow via Prefect
    
    
    Sleep for a set amount of time before checking again
    
    
Want to manually submit a specific structure? You can do this through the Prefect UI or a separate script.

Option 2 -- We start a set number of workflows. We have the end of one workflow trigger the start of a new one. This doesn't require any separate running process but instead uses the Prefect Agents/Executors. I think this approach will give rise to messy code and issues where we want to increase/decrease the number of jobs.


Option 2 -- We control the number of jobs through PrefectCloud concurrency settings. This requires a paid method and may require submitting all jobs to the queue at once though (or in stages like option 1).


extra utils to add...


Have a workflow that runs every month, day, etc. and deletes completed workflows to keep meta db size down


Check that pathways come out in the same order (index) despite cell shape