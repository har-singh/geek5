#!/bin/awk -f
# https://www.grymoire.com/Unix/Awk.html
# https://www.cyberciti.biz/faq/how-to-print-filename-with-awk-on-linux-unix/
# AWK array
#  https://www.thegeekstuff.com/2010/03/awk-arrays-explained-with-5-practical-examples/
#  http://kirste.userpage.fu-berlin.de/chemnet/use/info/gawk/gawk_12.html

BEGIN {
  RS="\n}\n"; FS="\n"; OFS=",";
  print "\n\n------------------------START------------------------\n";
  print "pool_name_var,description_var,load_balancing_mode_var,pool_member_var,monitor_var,partition_var,FILENAME";
}

{
  { #print "START of Record";
    monitor_var="empty";
    description_var="empty";
    load_balancing_mode_var="empty";
    pool_name_var="empty";
    member_switch=0;
    has_member="FALSE"
    delete member_array
    pool_member_var="empty";
    pool_member_addr_var="empty";
    pool_extra_var="empty";
    partition_var="empty";
  }
  for(i=1;i<=NF;i++){
    #find pool name line
    if ($i ~ /ltm pool/ && member_switch==0) {
      pool_name_var=$i;
    } else if ($i ~ /monitor/ && member_switch==0) {
      #find monitor line. MONITOR does not get printed because the output is displayed as soon as awk hits the pool member line
      monitor_var=$i;
    #find description line
    } else if ($i ~ /description/ && member_switch==0) {
      description_var = $i;
    } else if ($i ~ "load-balancing-mode" && member_switch==0) {
      load_balancing_mode_var=$i;
    } else if ($i ~ /members {/ && member_switch==0) {
      #the swith is being used to process the pool members section. switch to on at the beggening of the section and off when the section ends
      member_switch=1;
      has_member="TRUE";
    } else if ($i ~ /^    }$/ && member_switch==1) {
      member_switch=0;
    } else if($i ~ /^        }$/ && member_switch==1) {
      continue;
    } else if ($i ~ /:.*{/ && member_switch==1) {
      pool_member_var = $i;
      #print pool_name_var, description_var, load_balancing_mode_var, pool_member_var, FILENAME;
      member_array[i]=$i;
    } else if ($i ~ /address/ && member_switch==1) {
      pool_member_addr_var = $i;
      #print pool_member_addr_var;
    } else if ($i ~ /partition/ && member_switch==0) {
      partition_var=$i;
    }
  }
  { #printf "Number of members: "length(member_array);
    if (length(member_array) != 0 && pool_name_var!= "empty") {
      for (member_index in member_array) {
       print pool_name_var, description_var, load_balancing_mode_var, member_array[member_index], monitor_var, partition_var, FILENAME;
      }
    } else if (pool_name_var!= "empty") {
      print pool_name_var, description_var, load_balancing_mode_var, pool_member_var, monitor_var, partition_var, FILENAME;
    } else {
      #else place holder
    }
  #print "END of Record";
  }
}

END {
  print "\n------------------------END------------------------\n";
}
