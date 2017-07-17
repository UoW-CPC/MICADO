int deadline
int one_finish
int nmb_input_files
int nmb_output_files
time start_time
time end_time
int sec_counter
int nmb_starting_instances
bool done 
int infra_id

// We have to scale MICADO to fit the time period the user give us, to finish X experiments (jobs). 
// Depending on the time, we have to provision MICADO to be able to finish in time.

func main ()
{
	init()
	while !done
	{
		display_completion()
		if nmb_input_files == nmb_output_files 
			{
			done =true
			}
				provision(one_finish)
				time.sleep(one_finish) //check every X minute 
	}

}

func calc_nmb_starting_instanced_needed (deadline, one_finish, nmb_input_files)
{
	//one instance finish one experiment in one_finish time. Two make 2 times more.
	if nmb_input_files*one_finish < deadline
	{
		theoritical_deadline = one_finish*nmb_input_files
		count_how_much_to_fasten = theoritical_deadline / deadline
		nmb_starting_instances=floor(count_how_much_to_fasten)
	}
	else
	{
		nmb_starting_instances = 1
	}
	worker_starter()
}
func worker_starter (nmb_starting_instances, infra_id)
{
	for (int i = 0; i < nmb_starting_instances; ++i)
	{
	    curl -X POST http://0.0.0.0:5000/infrastructures/infra_id/scaleup/worker
	}
}

func provision (one_finish, nmb_output_files) 
{
	//TODO

	// check every X min if it is over or underprovisioned. Make adjustements
	theoritical_status = one_finish*(sec_counter/60)
	if nmb_output_files < theoritical_status
	{
		scale_up()
	}
	if nmb_output_files > theoritical_status
	{
		scale_down()
	}
}

func scale_up ()
{
	//TODO
   curl -X POST http://0.0.0.0:5000/infrastructures/$1/scaleup/$2

}
func scale_down ()
{
	//TODO
	// need to consider if a job is running on an instance what will happen with it.
}

func sec_counter ()
{
	start = time.time()
    time.clock()    
    elapsed = 0
    while elapsed < seconds
	    {
        elapsed = time.time() - start
        time.sleep(1)
        }  
	return elapsed
}

func display_completion ()
{
	printf(nmb_output_files ," of  ", nmb_input_files, " finished.");
}
func init ()
{
	nmb_input_files = count("input_directory")
	printf("There are $1 input files stored in the input directory.\n", nmb_input_files);
	printf("Deadline in mimutes: \n");
	deadline = console.read()
	printf("Expected finish time of one experiment: \n");
	one_finish = console.read()
	printf("ID of the infrastructure: \n");
	infra_id = console.read()
	done = false
	start_time = time.now()
	end_time = start_time + convert.Totime(deadline)
	calc_nmb_starting_instanced_needed (deadline, one_finish, nmb_input_files)

}





