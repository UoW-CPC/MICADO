 #!/bin/bash

    while true
    do

    #getservices
    curl -X GET http://hostIP:2375/v1.27/services > getservices.json

    jq '. | length-1' getservices.json > nmbservices
    jq '.[].Spec.Name' getservices.json | sed 's/.//;s/.$//' > servicenames
    grep ALERT "/etc/prometheus/prometheus.rules" | sed  's/ALERT\s*//g;s/^ *//;s/_.*//' | awk '!seen[$0]++' > alertnames
    cat alertnames | wc -l > nmbalerts
    nmbservices=$(cat nmbservices)
    for i in $(seq 0 $nmbservices); do
      echo "${i}" > counter
      # set the cpu limit from the config, cut get back 0-100 value
      cpulimit=$(jq --slurpfile newvalue counter '.[$newvalue[0]].Spec.TaskTemplate.Resources.Limits.NanoCPUs' getservices.json | cut -c 1-2)
      
      if [ "$cpulimit" = "nu" ]; then
        cpulimit=95
      fi
      ((cpulimit-=10)) # top limit adjust so it can overload
      name=$(jq --slurpfile newvalue counter '.[$newvalue[0]].Spec.Name' getservices.json | sed 's/.//;s/.$//')
      namequotes=$(jq --slurpfile newvalue counter '.[$newvalue[0]].Spec.Name' getservices.json)

      #create new rules
      if [ -n "$name" ]; then
      if grep -q $name "/etc/prometheus/prometheus.rules"; then
          echo "already exists"     
      else
          echo "create new rule named $name " 

          echo "ALERT $name"_overloaded"
          IF avg(rate(container_cpu_usage_seconds_total{container_label_com_docker_swarm_service_name=$namequotes }[30s]))*100 > $cpulimit
          FOR 30s
          LABELS {alert="'"overloaded"'", type="'"docker"'", application=$namequotes}
          ANNOTATIONS {
          summary = "'"overloaded"'"}

          ALERT $name"_underloaded"
          IF avg(rate(container_cpu_usage_seconds_total{container_label_com_docker_swarm_service_name=$namequotes }[30s]))*100 < 20
          FOR 30s
          LABELS {alert="'"underloaded"'", type="'"docker"'", application=$namequotes}
          ANNOTATIONS {
          summary = "'"underloaded"'"}" >> /etc/prometheus/prometheus.rules
      fi
      fi
      done



    echo "remove olds"
    # remove old alerts
    nmbalerts=$(cat nmbalerts)
    echo "nmb of alerts  $nmbalerts"

    for e in $(seq 1 $nmbalerts); do
      alertnametemp=$(sed "${e}q;d" alertnames)
     echo "current  $alertnametemp"
      if grep -q $alertnametemp servicenames;then 
          echo "need"
      else
          if [ "$alertnametemp" != "lb" ] && [ "$alertnametemp" != "worker" ];then
          echo "dont need"
          #every app has 2 alerts we need the first alert which starts with the name of the service, then delete 12 lines, 2 rules
          endline=12
          startline=$(grep -m1 -n "ALERT $alertnametemp" /etc/prometheus/prometheus.rules | awk -F  ":" '{print $1}')
          ((endline+=startline))
          sed "$startline,$endline d" /etc/prometheus/prometheus.rules > alerttmp
          mv alerttmp /etc/prometheus/prometheus.rules
          fi

      fi
    done
    #reload prometheus configuration
    curl -X POST http://hostIP:9090/-/reload
    sleep 10
    done
