#!/bin/bash
curl -s  http://safar.tropmet.res.in/safar-apps-backend/json/station_list_multi1.php?action=station_list  | jq " .languages | .[0] | .Cities | .[1] | .stations | .[0] "
