# !/bin/awk -f
# HS 22Jan21
# https://www.grymoire.com/Unix/Awk.html
# https://www.cyberciti.biz/faq/how-to-print-filename-with-awk-on-linux-unix/


BEGIN {
  RS="\n}\n"; FS="\n"; OFS=",";
  print "\n\n------------------------START------------------------\n";
  print "vs_name_var,description_var,destination_var,partition_var,pool_name_var,vs_snat_var,FILENAME";
}

{
  { #print "START of Record";
    vs_name_var = "empty";
    description_var = "empty";
    destination_var = "empty";
    partition_var = "empty";
    pool_name_var = "empty";
    vs_snat_var = "no_snat";
  }
  for(i=1;i<=NF;i++){
    if ($i ~ /ltm virtual /) {
      #find virtual server name line
      vs_name_var=$i;
    } else if ($i ~ /destination/) {
      destination_var=$i;
    #find description line
    } else if ($i ~ /description/) {
      description_var = $i;
    } else if ($i ~ /^    pool/) {
      pool_name_var=$i;
    } else if ($i ~ /partition/) {
      partition_var = $i;
    } else if ($i ~ /type snat/ || $i ~ /type automap/) {
      vs_snat_var = $i;
    }
  }
  { if (vs_name_var != "empty") {
    print vs_name_var, description_var, destination_var, partition_var, pool_name_var, vs_snat_var, FILENAME;
  }
  #print "END of Record";
  }
}

END {
  print "\n------------------------END------------------------\n";
}
