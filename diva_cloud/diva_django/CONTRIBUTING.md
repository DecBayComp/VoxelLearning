# CONTRIBUTE

## Git help

* See [README.md](https://gitlab.pasteur.fr/diva/diva-cloud/-/blob/master/diva_django/README.md) for install documentation

* All changes to [diva-cloud](https://gitlab.pasteur.fr/diva/diva-cloud) should be made through merge
  requests to this repository (with just two exceptions outlined below).

* Fork the [diva-cloud repository](https://gitlab.pasteur.fr/diva/diva-cloud) on
  GitLab to make your changes.  To keep your copy up to date with respect to
  the main repository, you need to frequently [sync your
  fork](https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html#repository-mirroring):
  ```
    $ git remote add upstream https://gitlab.pasteur.fr/diva/diva-cloud
    $ git fetch upstream
    $ git checkout dev
    $ git merge upstream/dev
  ```

* Choose the correct branch to develop your changes against.

  * Additions of new features to the code base should be pushed to the `dev`
    branch (`git checkout dev`).

* Commit and push your changes to your
  [fork](https://docs.gitlab.com/ee/user/project/push_options.html).

* Open a [merge
  request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html) with
  these changes. You merge request message ideally should include:

   * A description of why the changes should be made.

   * A description of the implementation of the changes.

   * A description of how to test the changes.


## Add a new job 

4 steps to add a new job:

* Copy and paste the [job_wrapper.py](https://gitlab.pasteur.fr/diva/diva-cloud/-/blob/master/diva_django/jobapp/jobs/job_wrapper.py) file into a new file with the name of your job.

* Replace all the <something> fields in your job_x.py file with job specifications (_You can take à look at [job_train.py](https://gitlab.pasteur.fr/diva/diva-cloud/-/blob/master/diva_django/jobapp/jobs/job_train.py) if you need inspiration_)
   

* Udate [joblauncher.py](https://gitlab.pasteur.fr/diva/diva-cloud/-/blob/master/diva_django/jobapp/joblauncher.py) with:

   * Imports ([line 7](https://gitlab.pasteur.fr/diva/diva-cloud/-/blob/master/diva_django/jobapp/joblauncher.py#L7))
   
   * Jobstype ([line 10](https://gitlab.pasteur.fr/diva/diva-cloud/-/blob/master/diva_django/jobapp/joblauncher.py#L10))
   
   * Job call ([line 24](https://gitlab.pasteur.fr/diva/diva-cloud/-/blob/master/diva_django/jobapp/joblauncher.py#L24))
   
* Udate [job_views.py](https://gitlab.pasteur.fr/diva/diva-cloud/-/blob/master/diva_django/jobapp/views/job_views.py) with:

   * Specific job parameters_tab and inputs_tab ([line 87](https://gitlab.pasteur.fr/diva/diva-cloud/-/blob/master/diva_django/jobapp/views/job_views.py#L87))