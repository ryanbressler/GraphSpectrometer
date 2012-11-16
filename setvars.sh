export NGSPECCORES=4
export NGSPECPLOTINGCORES=2
export RFACE=/titan/cancerregulome9/ITMI_PTB/bin/rf-ace-read-only/bin/rf-ace
export GSPEC=/titan/cancerregulome9/ITMI_PTB/bin/GraphSpectrometer
export LCOUNT=/titan/cancerregulome9/ITMI_PTB/bin/go/src/github.com/ryanbressler/CloudForest/leafcount/leafcount
export BLACKLIST=/titan/cancerregulome9/ITMI_PTB/public/analysis/blacklists/blackListTemplate.txt



function RMEMPTY {
	if [ "$(ls -A $1)" ]; then
	     echo "$1 is not Empty"
	else
	    echo "$1 is Empty. Removeing."
	    rm -r $1
	fi
}

export -f RMEMPTY 