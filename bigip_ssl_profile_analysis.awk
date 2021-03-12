#!/bin/awk -f
#HS 22Jan21
#https://www.grymoire.com/Unix/Awk.html
#https://www.cyberciti.biz/faq/how-to-print-filename-with-awk-on-linux-unix/


BEGIN {
  RS="\n}\n"; FS="\n"; OFS=",";
  print "\n\n------------------------START------------------------\n";
  print "vs_name_var,description_var,destination_var,partition_var,pool_name_var,vs_snat_var,FILENAME";
}

{
  { #print "START of Record";
    ssl_client_profile_name_var = "empty";
    cert_var = "empty";
    chain_var = "empty";
    key_var = "empty";
    pool_name_var = "empty";
    vs_snat_var = "no_snat";
  }
  for(i=1;i<=NF;i++){
    if ($i ~ /ltm profile client-ssl/) {
      ssl_client_profile_name_var = $i;
    } else if ($i ~ /^            cert/) {
      cert_var = $i;
    } else if ($i ~ /^            chain/) {
      chain_var = $i;
    } else if ($i ~ /^            key/) {
      key_name_var=$i;
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
