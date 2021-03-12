# !/bin/awk -f
# HS 12Mar21
# https://www.grymoire.com/Unix/Awk.html
# https://www.cyberciti.biz/faq/how-to-print-filename-with-awk-on-linux-unix/


BEGIN {
  RS="\n}\n"; FS="\n"; OFS=",";
  print "\n\n------------------------START------------------------\n";
  print "ssl_profile_name_var,cert_var,chain_var,key_var,FILENAME";
}

{
  { #print "START of Record";
    ssl_profile_name_var = "empty";
    cert_var = "empty";
    chain_var = "empty";
    key_var = "empty";
  }
  for(i=1;i<=NF;i++){
    if ($i ~ /ltm profile client-ssl/) {
      ssl_profile_name_var=$i;
    } else if ($i ~ /^            cert/) {
      cert_var=$i;
    } else if ($i ~ /^            chain/) {
      chain_var = $i;
    } else if ($i ~ /^            key/) {
      key_var=$i;
    }
  }
  { if (vs_name_var != "empty") {
    print ssl_profile_name_var, cert_var, chain_var, key_var, FILENAME;
  }
  #print "END of Record";
  }
}

END {
  print "\n------------------------END------------------------\n";
}
