import datetime
import os, os.path

deadline = 0 // in minutes
one_finish = 0 // estimate
nmb_input_files = 0
nmb_output_files = 0
datetime.time start_time, end_time
sec_counter = 0
nmb_starting_instances = 0
done = false 
infra_id = ""



// We have to scale MICADO to fit the time period the user give us, to finish X experiments (jobs). 
// Depending on the time, we have to provision MICADO to be able to finish in time.

def main ():
{
	init()
	while done == false:
	{
		display_completion()
		if nmb_input_files == nmb_output_files 
			{
			done = true
			}
				provision(one_finish, nmb_output_files)
				datetime.time.sleep(60) //check every X minute 
	}

}

def init ():
{
	nmb_input_files = len([name for name in os.listdir('/path/to/inputfolder') if os.path.isfile(name)])
	print ("There are %s input files stored in the input directory.", nmb_input_files)
	deadline = input("deadline in mimutes: ")
	one_finish = input("Expected finish time of one experiment: ")
	infra_id = input("ID of the infrastructure: ")
	done = false
	start_time = time.time()
	end_time = start_time + convert.Totime(deadline) // TODO
	calc_nmb_starting_instances_needed (deadline, one_finish, nmb_input_files)

}

def calc_nmb_starting_instances_needed (deadline, one_finish, nmb_input_files):
{
	//one instance finish one experiment in one_finish time. Two make 2 times more.
	if nmb_input_files*one_finish <= deadline
	{
		theoritical_completion_time = one_finish*nmb_input_files
		count_how_much_to_fasten = theoritical_completion_time / float(deadline)
		nmb_starting_instances = math.floor(count_how_much_to_fasten)
	}
	else
	{
		theoritical_completion_time = (one_finish*nmb_input_files) / float(deadline)
		nmb_starting_instances = math.floor(theoritical_completion_time)
	}
	worker_starter(nmb_starting_instances, infra_id)
}
def worker_starter (nmb_starting_instances, infra_id):
{
	call_string = "http://0.0.0.0:5000/infrastructures/" + infra_id + "/scaleup/worker"
	for  x in range(1, nmb_starting_instances):
	{
	    curl -X POST call_string //TODO
	}
}

def provision (one_finish, nmb_output_files):
{
	// check every X min if it is over or underprovisioned. Make adjustements
	theoritical_status = math.floor(one_finish*(sec_counter(start_time)))
	if nmb_output_files < theoritical_status
	{
		for x in range (0,theoritical_status):
		scale_up(infra_id)
	}
	if nmb_output_files >= theoritical_status
	{
		theoritical_status = theoritical_status - nmb_output_files
        for x in range (0,theoritical_status):
		scale_down(infra_id)
	}
}

def scale_up (infra_id):
{
    call_string = "http://0.0.0.0:5000/infrastructures/" + infra_id + "/scaleup/worker"

	//TODO
   curl -X POST call_string

}
def scale_down (infra_id):
{
	//TODO
	// need to consider if a job is running on an instance what will happen with it.
}

def sec_counter (start_time):
{
    time.clock()    
    elapsed = 0
    while elapsed < seconds:
        elapsed = time.time() - start_time
        time.sleep(1)
	return elapsed
}

def display_completion ():
{
	print(nmb_output_files ," of  ", nmb_input_files, " is finished.")

}






